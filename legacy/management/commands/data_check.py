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
import MySQLdb

from functools import wraps
from django.db import connection
from django.db.utils import IntegrityError

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

        parser.add_argument(
            '--realtime',
            action='store_true',
            dest='realtime',
            default=False,
            help='realtime repeted data'
        )        

        parser.add_argument(
            '-d',
            '--day',
            type=str,
            
            help='query by day'
        )

        parser.add_argument(
            '--hour',
            type=str,
            
            help='query by hour'
        )

        parser.add_argument(
            '-m',
            '--month',
            type=str,
            
            help='query by month'
        )

        parser.add_argument(
            '--syncbigmeter',
            action='store_true',
            dest='syncbigmeter',
            default=False,
            help='syncbigmeter  data'
        )  

    def handle(self, *args, **options):
        
        t1=time.time()
        count = 0
        if options['watermeter']:
            watermeter_check(**options)

        if options['bigmeter']:
            bigmeter_check(**options)

        if options['syncbigmeter']:
            syncbigmeter(**options)

# 按月同步数据
def syncbigmeter(**options):
    month = options['month']
    if not month:
        print("should month")
        return

    sx_bigmeters = Bigmeter.objects.using("shexian").values_list('commaddr','username')
    sx_dict = dict(sx_bigmeters)

    for commaddr,name in sx_dict.items():
        check_bigmeter_flowdata_month(commaddr,name,month)
        # t = threading.Thread(target=check_bigmeter_flowdata_month,args=(commaddr,name,month))
        # t.start()
             

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

    month = options['month']
    day = options['day']
    hour = options['hour']
    realtime = options['realtime']

    sx_bigmeters = Bigmeter.objects.using("shexian").values_list('commaddr','username')
    sx_commaddr = []
    for s in sx_bigmeters:
        sx_commaddr.append(s[0])
    amrs_bigmeters = Bigmeter.objects.using("zncb").filter(commaddr__in=sx_commaddr).values_list('commaddr','username')

    sx_dict = dict(sx_bigmeters)
    amrs_dict = dict(amrs_bigmeters)

    print("sx_bigmeters count:",len(sx_bigmeters))
    print("amrs_bigmeters count:",len(amrs_bigmeters))

    # 检查和同步歙县数据库bigmeter是否一致
    for commaddr,name in sx_dict.items():
        amrs_name = amrs_dict.get(commaddr,None)
        if amrs_name is None:
            sb = Bigmeter.objects.using("shexian").filter(commaddr=commaddr).values()[0]
            if "id" in sb:
                del sb["id"]
            am = Bigmeter.objects.create(**sb)
            if hasattr(am,'username'):
                amrs_name = am.username
        # fmt = '{}:{}\t\t\t|{}'.format(commaddr,name,amrs_name)
        # print(fmt)



        if month:
            
            check_bigmeter_flowdata_month(name,commaddr,month)

        if day:
            
            check_bigmeter_flowdata_day(name,commaddr,day)
            

            if hour:
                check_bigmeter_flowdata_hour(name,commaddr,day)

            if realtime:
                check_bigmeter_realtimedata(name,commaddr,day)


def check_bigmeter_flowdata_month(name,commaddr,month):
    sx_flow = HdbFlowDataMonth.objects.using("shexian").filter(commaddr=commaddr,hdate=month).values()
    for s in sx_flow:
        if "id" in s:
            del s["id"]
        hdate=s['hdate']
        dosage = s['dosage']
        
        v = HdbFlowDataMonth.objects.filter(commaddr=commaddr,hdate=hdate)
        # print(hdate,dosage,v)
        if v :
            v0 = v.first()
            fmt = '{}({})\t:{}\t{}'.format(name,commaddr,dosage,v0.dosage)
            if v0.dosage != dosage:
                fmt = '{}({})\t:{}\t{}'.format(name,commaddr,dosage,v0.dosage)
                v.update(**s)
                

        else:
            
            HdbFlowDataMonth.objects.create(**s)
            fmt = '{}({})\t:{}\t{}'.format(name,commaddr,dosage,'None')

        print(fmt)

    # day
    check_bigmeter_flowdata_day(name,commaddr,month)



def check_bigmeter_flowdata_day(name,commaddr,day):
    sx_flow = HdbFlowDataDay.objects.using("shexian").filter(commaddr=commaddr,hdate__startswith=day).values()
    for s in sx_flow:
        if "id" in s:
            del s["id"]
        hdate=s['hdate']
        dosage = s['dosage']
        
        v = HdbFlowDataDay.objects.filter(commaddr=commaddr,hdate=hdate)
        # print(hdate,dosage,v)
        if v :
            v0 = v.first()
            fmt = '{}({})\t:{}\t{}'.format(name,commaddr,dosage,v0.dosage)
            if v0.dosage != dosage:
                fmt = '{}({})\t:{}\t{} noequal ,update'.format(name,commaddr,dosage,v0.dosage)
                v.update(**s)
                

        else:
            fmt = '{}({})\t:{}\t{}'.format(name,commaddr,dosage,'None')
            try:
                HdbFlowDataDay.objects.create(**s)
            except IntegrityError as e: # django.db.utils.IntegrityError: (1062, "Duplicate entry '7865124' for key 'PRIMARY'")
                
                if e.args[0] == 1062:
                    HdbFlowDataDay.objects.filter(commaddr=commaddr,hdate=hdate).update(**s)
                    # print("\t{}".format(e))
                    print("{}--{}".format(v,e,e.args[0]))
            except Exception as e:
                print("=---==qwer30q0er9",type(e),type(e.args),e.args)

        check_bigmeter_flowdata_hour(name,commaddr,hdate)


def check_bigmeter_flowdata_hour(name,commaddr,day):
    sx_flow_hours = HdbFlowDataHour.objects.using("shexian").filter(commaddr=commaddr,hdate__startswith=day).values()
    for s in sx_flow_hours:
        if "id" in s:
            del s["id"]
        hdate = s['hdate']
        dosage = s['dosage']

        v = HdbFlowDataHour.objects.filter(commaddr=commaddr,hdate=hdate)
        if v:
            v0 = v.first()

            if v0.dosage != dosage:
                fmt = '{}({})-{}\t:{}\t|{} noequal ,update'.format(name,commaddr,hdate,dosage,v0.dosage)
                print(fmt)
                v.update(**s)
        else:
            HdbFlowDataHour.objects.create(**s)
            fmt = '{}({})-{}\t:{}\t created'.format(name,commaddr,hdate,dosage)
            print(fmt)
    

def check_bigmeter_realtimedata(name,commaddr,day):

    sx_flow_rt = HdbFlowData.objects.using("shexian").filter(commaddr=commaddr,readtime__startswith=day).values()
    for s in sx_flow_rt:
        if "id" in s:
            del s["id"]
        readtime = s['readtime']
        flux = s['flux']

        v = HdbFlowData.objects.filter(commaddr=commaddr,readtime=readtime)
        if v:
            v0 = v.first()

            if v0.flux != flux:
                fmt = '{}({})-{}\t:{}\t|{} noequal ,update'.format(name,commaddr,readtime,flux,v0.flux)
                print(fmt)
                v.update(**s)
        else:
            HdbFlowData.objects.create(**s)
            fmt = '{}({})-{}\t:{}\t created'.format(name,commaddr,readtime,flux)
            print(fmt)