from django.core.management.base import BaseCommand, CommandError


from legacy.models import (HdbFlowData,HdbFlowDataDay,HdbFlowDataHour,HdbFlowDataMonth,HdbPressureData,Bigmeter,
    Watermeter,HdbWatermeterDay,HdbWatermeterMonth,Concentrator,Community,
    HdbFlowDataMonth)

import time
import datetime
import logging
import string
import itertools

from dmam.models import VConcentrator,VWatermeter,VCommunity,Station,Meter,SimCard,DMABaseinfo,DmaStation
from entm.models import Organizations

from gis.models import FenceDistrict,Polygon,FenceShape

logger_info = logging.getLogger('info_logger')


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


"""
When you call values() on a queryset where the Model has a ManyToManyField
and there are multiple related items, it returns a separate dictionary for each
related item. This function merges the dictionaries so that there is only
one dictionary per id at the end, with lists of related items for each.
"""
def merge_values(values):
    grouped_results = itertools.groupby(values, key=lambda value: value['id'])
    print(grouped_results)
    merged_values = []
    for k, g in grouped_results:
        print( k)
        groups = list(g)
        merged_value = {}
        for group in groups:
            for key, val in group.items():
                if not merged_value.get(key):
                    merged_value[key] = val
                elif val != merged_value[key]:
                    if isinstance(merged_value[key], list):
                        if val not in merged_value[key]:
                            merged_value[key].append(val)
                    else:
                        old_val = merged_value[key]
                        merged_value[key] = [old_val, val]
        merged_values.append(merged_value)
    return merged_values

class Command(BaseCommand):
    help = 'import data from A to B'

    def add_arguments(self, parser):
        # parser.add_argument('sTime', type=str)

        

        parser.add_argument(
            '--dmastation',
            action='store_true',
            dest='dmastation',
            default=False,
            help='import dmastation to new db'
        )


        parser.add_argument(
            '--station-bigmeter',
            action='store_true',
            dest='station-bigmeter',
            default=False,
            help='import station-bigmeter to new db'
        )

        parser.add_argument(
            '--listname',
            action='store_true',
            dest='listname',
            default=False,
            help='import listname to new db'
        )

        parser.add_argument(
            '--gisupdate',
            action='store_true',
            dest='gisupdate',
            default=False,
            help='import gisupdate to new db'
        )

        parser.add_argument(
            '--vwatermeter',
            action='store_true',
            dest='vwatermeter',
            default=False,
            help='import vwatermeter to new db'
        )


        parser.add_argument(
            '--mergetest',
            action='store_true',
            dest='mergetest',
            default=False,
            help='import mergetest to new db'
        )



    def handle(self, *args, **options):
        # sTime = options['sTime']
        t1=time.time()
        count = 0
        aft = 0

        if options['mergetest']:
            organ_info = merge_values(Organizations.objects.all().values("id","name","cid","pId","uuid","station","station__username"))
            results = [
                        {'universities': 1, 'name': u'Course Name', 'categories': 1, 'id': 2}, 
                        {'universities': 2, 'name': u'Course Name', 'categories': 1, 'id': 2}, 
                        {'universities': 1, 'name': u'Course Name', 'categories': 5, 'id': 2}, 
                        {'universities': 2, 'name': u'Course Name', 'categories': 5, 'id': 2}, 
                        {'universities': 1, 'name': u'Course Name', 'categories': 6, 'id': 2}, 
                        {'universities': 2, 'name': u'Course Name', 'categories': 6, 'id': 2}
                    ]
            # organ_info=merge_values(results)
            print(organ_info)

        if options['gisupdate']:
            fds = FenceDistrict.objects.exclude(cid__startswith='zw_m').all()
            polys = Polygon.objects.all()

            for fence in fds:
                cid = fence.cid
                shap = FenceShape.objects.filter(shapeId=cid)
                if not shap.exists():
                    pol = Polygon.objects.filter(polygonId=cid)
                    if pol.exists():
                        p = pol.first()
                        name = p.name
                        shape = p.shape
                        pointSeqs = p.pointSeqs
                        longitudes = p.longitudes
                        latitudes = p.latitudes
                        ftype = p.ftype
                        dma_no = p.dma_no
                        FenceShape.objects.create(shapeId=cid,name=name,zonetype=ftype,shape=shape,pointSeqs=pointSeqs,longitudes=longitudes,latitudes=latitudes,dma_no=dma_no)

        

        if options['station-bigmeter']:
            
            organ = Organizations.objects.get(name="歙县自来水公司")
            # data_qset=HdbFlowData.objects.using("virvo").filter(readtime__range=[sTime,'2018-09-20'])
            data_qset=Bigmeter.objects.using("zncb").values_list('commaddr','commstate','meterstate','gprsv','meterv',
                'signlen','lastonlinetime','pressure','plustotalflux','reversetotalflux','flux','totalflux','pressurereadtime',
                'fluxreadtime','username')
            
            for d in data_qset:
                commaddr = d[0]
                username = d[14]

                # query station find if commaddr exist
                stations=Station.objects.filter(username=username)
                if not stations.exists():
                    print(" {} {} not in station list".format(username,commaddr))

                    # check if commaddr exist in meter
                    meters=Meter.objects.filter(simid__simcardNumber=commaddr)
                    if not meters.exists():
                        print(" {} {} not in meters list".format(username,commaddr))
                        
                        # check if commaddr exist in simcards
                        simcards = SimCard.objects.filter(simcardNumber=commaddr)
                        if not simcards.exists():
                            print(" {} {} not in simcards list".format(username,commaddr))
                            count += 1
                            sd = SimCard.objects.create(simcardNumber=commaddr,belongto=organ)
                        else:
                            sd =SimCard.objects.get(simcardNumber=commaddr)
                        
                        m = Meter.objects.create(serialnumber=commaddr,simid=sd,belongto=organ)

                    else:
                        m = Meter.objects.get(simid__simcardNumber=commaddr)

                    # and then add to Station
                    try:
                        s = Station.objects.create(username=username,belongto=organ,meter=m)
                    except:
                        print("-------------{} {} may duplication".format(username,commaddr))

        if options['listname']                :
            organ = Organizations.objects.get(name="歙县自来水公司")
            # data_qset=HdbFlowData.objects.using("virvo").filter(readtime__range=[sTime,'2018-09-20'])
            data_qset=Bigmeter.objects.using("zncb").values_list('commaddr','commstate','meterstate','gprsv','meterv',
                'signlen','lastonlinetime','pressure','plustotalflux','reversetotalflux','flux','totalflux','pressurereadtime',
                'fluxreadtime','username')
            
            for d in data_qset:
                commaddr = d[0]
                username = d[14]

                sb = Station.objects.filter(meter__simid__simcardNumber=commaddr)
                s=sb.first()
                if sb. count() > 1:
                    print("----------multiple station {} {}".format(sb.count(),commaddr),sb)
                # if s.username != username:
                #     print("{} {}".format(s.username,username))
                
                    

        

        if options['dmastation']:
            
            dmabs = DMABaseinfo.objects.all()
            for d in dmabs:
                print(d.dma_name)
                stations = d.station_set.all()
                # print(stations.count(),stations)
                for s in stations:
                    station_id = s.meter.simid.simcardNumber
                    meter_type = s.dmametertype
                    station_type = 1
                    print(d.dma_name,station_id,meter_type,station_type)
                    DmaStation.objects.create(dmaid=d,station_id=station_id,meter_type=meter_type,station_type=station_type)
                    

        if options['vwatermeter']:
            
            zncb_watermeters = Watermeter.objects.values()
            for w in zncb_watermeters:
                waterid = w["id"]
                v = VWatermeter.objects.filter(waterid=waterid)
                if not v.exists():
                    print(waterid," not in virvo vwatermeter")
                    continue

                v = VWatermeter.objects.get(waterid=waterid)
                v.wateraddr = w["wateraddr"]
                v.numbersth = w["numbersth"]
                v.buildingname = w["buildingname"]
                v.roomname = w["roomname"]
                v.nodeaddr = w["nodeaddr"]
                v.username = w["username"]
                v.usertel = w["usertel"]
                v.dn = w["dn"]
                v.serialnumber = w["serialnumber"]
                v.manufacturer = w["manufacturer"]
                v.madedate = w["madedate"]
                # v.ValveMeter = w["ValveMeter"]
                v.installationsite = w["installationsite"]

                v.save()
                

        
                    
                
        
        # print('cnt=',cnt,cnt2)
        t2 = time.time() - t1
        self.stdout.write(self.style.SUCCESS(f'total {count}  Affected {aft} row(s)!,elapsed {t2}'))
