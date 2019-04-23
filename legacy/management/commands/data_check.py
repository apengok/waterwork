from django.core.management.base import BaseCommand, CommandError
from django.db import connections

from legacy.models import (HdbFlowData,HdbFlowDataDay,HdbFlowDataHour,HdbFlowDataMonth,HdbPressureData,Bigmeter,
    Watermeter,HdbWatermeterDay,HdbWatermeterMonth,Concentrator,Community,SecondWater,
    HdbFlowDataMonth)

import time
import datetime
import logging
import threading
# import Queue
from dmam.models import VConcentrator,VWatermeter,VCommunity,VSecondWater
from entm.models import Organizations


from functools import wraps
from django.db import connection

def db_auto_reconnect(func):
    """Auto reconnect db when mysql has gone away."""
    @wraps(func)
    def wrapper(*args, **kwagrs):
        try:
            connection.connection.ping()
        except Exception:
            connection.close()
        return func(*args, **kwagrs)
    return wrapper

logger_info = logging.getLogger('info_logger')


def close_old_connections():
    for conn in connections.all():
        conn.close_if_unusable_or_obsolete()




class Command(BaseCommand):
    help = 'import data from A to B'

    def add_arguments(self, parser):
        # parser.add_argument('sTime', type=str)

        parser.add_argument(
            '--watermeter',
            action='store_true',
            dest='watermeter',
            default=False,
            help='check watermeter data'
        )        

        parser.add_argument(
            '--bigmeter',
            action='store_true',
            dest='bigmeter',
            default=False,
            help='check bigmeter data'
        )        

        parser.add_argument(
            '--delete',
            action='store_true',
            dest='delete',
            default=False,
            help='delete repeted data'
        )        

    def handle(self, *args, **options):
        
        t1=time.time()
        count = 0
        if options['watermeter']:
            watermeter_check(**options)

        if options['bigmeter']:
            bigmeter_check(**options)
             

# unique_together = (('communityid', 'nodeaddr', 'wateraddr'),)
def watermeter_check(**options):
    print("watermeter checking...")
    sx_watermeters = Watermeter.objects.using("shexian").values("id","communityid","nodeaddr","wateraddr","serialnumber","numbersth","buildingname","roomname")
    amrs_watermeters = Watermeter.objects.values("id","communityid","nodeaddr","wateraddr","serialnumber","numbersth","buildingname","roomname")
    v_watermeters = VWatermeter.objects.values("id","name","serialnumber","nodeaddr","wateraddr","numbersth","buildingname","roomname","communityid__id")

    print('sx_count:',sx_watermeters.count())
    print('amrs_cnt:',amrs_watermeters.count())
    print('vir_cout:',v_watermeters.count())

    repete_dict = {}
    v_should_dict = {}
    delete_id_list = []
    for v in v_watermeters:
        k = '{}_{}_{}'.format(v['communityid__id'],v['nodeaddr'],v['wateraddr'])
        n = '{},{},{}'.format(v['serialnumber'],v['buildingname'],v['roomname'])
        if k not in v_should_dict:
            v_should_dict[k] = n
        else:
            if k not in repete_dict:
                repete_dict[k] = n
                delete_id_list.append(v['id'])
                # print(k,v)
            else:
                print("more than one repete",k,v)

    print('repete watermeter count:',len(repete_dict))
    print ('real data count',len(v_should_dict))
    print('delete_id_list count:',len(delete_id_list))
    print('\r\n\r\n')

    if options['delete']:
        md = VWatermeter.objects.filter(id__in=delete_id_list)
        print('dletecoutn',md.count())
        for m in md:
            m.delete()


def bigmeter_check(**options):

    sx_bigmeters = Bigmeter.objects.using("shexian").values('commaddr','username')
    sx_commaddr = []
    for s in sx_bigmeters:
        sx_commaddr.append(s["commaddr"])
    amrs_bigmeters = Bigmeter.objects.using("zncb").filter(commaddr__in=sx_commaddr).values('commaddr','username')

    print("sx_bigmeters count:",len(sx_bigmeters))
    print("amrs_bigmeters count:",len(amrs_bigmeters))
    # 黄山市苏扬置业有限公司(文欣苑)监控表 18255954864
    # sx_flow = HdbFlowDataMonth.objects.using("shexian").filter(commaddr='18255954864',hdate__range=['2018-10','2019-04']).values('hdate','dosage')
    # for s in sx_flow:
    #     hdate=s['hdate']
    #     dosage = s['dosage']
        
    #     v = HdbFlowDataMonth.objects.filter(commaddr='18255954864',hdate=hdate)
    #     # print(hdate,dosage,v)
    #     if v :
    #         v = v.first()
    #         if v.dosage != dosage:
    #             print (v.hdate,v.dosage,"(",dosage,")")
    #             v.dosage = dosage
    #             v.save()

    #     else:
    #         HdbFlowDataMonth.objects.create(commaddr='18255954864',hdate=hdate,dosage=dosage)
    