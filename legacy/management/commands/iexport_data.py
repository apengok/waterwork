from django.core.management.base import BaseCommand, CommandError

from legacy.models import HdbFlowData,HdbFlowDataDay,HdbFlowDataHour,HdbFlowDataMonth,HdbPressureData,Bigmeter,Watermeter,HdbWatermeterDay,HdbWatermeterMonth
import time
import datetime
import logging

logger_info = logging.getLogger('info_logger')

def test_job():
    # time.sleep(random.randrange(1, 100, 1)/100.)
    # print("I'm a test job!")
    logger_info.info("synchronize data from shexian")
    count = 0
    bigmeters_qset = Bigmeter.objects.using("shexian").values_list('commaddr','commstate','meterstate','gprsv','meterv',
                'signlen','lastonlinetime','pressure','plustotalflux','reversetotalflux','flux','totalflux','pressurereadtime',
                'fluxreadtime','username')

    for b in bigmeters_qset:
        commaddr = b[0]

        try:
            d2=Bigmeter.objects.using("zncb").get(commaddr=commaddr)
        except:
            logger_info.info("{} {} not exists in virovo db".format(b[14],b[0]))
            continue
        if d2:
            d2.commstate = b[1]
            d2.meterstate = b[2]
            d2.gprsv = b[3]
            d2.meterv = b[4]
            d2.signlen = b[5]
            d2.lastonlinetime = b[6]
            d2.pressure = b[7]
            d2.plustotalflux = b[8]
            d2.reversetotalflux = b[9]
            d2.flux = b[10]
            d2.totalflux = b[11]
            d2.pressurereadtime = b[12]
            d2.fluxreadtime = b[13]
            
            d2.save(using='zncb')

        # logger_info.info("1.hdb_flow_data")
        # 威尔沃数据库最后一条数据记录
        zncb_last = HdbFlowData.objects.using("zncb").filter(commaddr=commaddr).last()
        if zncb_last:
            last_readtime = zncb_last.readtime

            if last_readtime is None:
                continue
            # 取歙县服务器该条数据记录对比
            sx_last = HdbFlowData.objects.using("shexian").filter(commaddr=commaddr).filter(readtime=last_readtime).first()
            # 取出上次最后一条数据记录之后增加的记录
            if sx_last:
                # print('last_readtime',last_readtime,zncb_last)
                # print('sx_last',sx_last)
                added = HdbFlowData.objects.using("shexian").filter(commaddr=commaddr).filter(readtime__gt=datetime.datetime.strptime(last_readtime.strip(),"%Y-%m-%d %H:%M:%S")).all()
                if added.exists():
                    count += added.count()
                    for d in added:
                        d.save(using='zncb')

        # logger_info.info("2.hdb_flow_data_day")
        zncb_last = HdbFlowDataDay.objects.using("zncb").filter(commaddr=commaddr).last()
        if zncb_last:
            last_readtime = zncb_last.hdate

            if last_readtime is None:
                continue
            # 取歙县服务器该条数据记录对比
            sx_last = HdbFlowDataDay.objects.using("shexian").filter(commaddr=commaddr).filter(hdate=last_readtime).first()
            # 取出上次最后一条数据记录之后增加的记录
            if sx_last:
                added = HdbFlowDataDay.objects.using("shexian").filter(commaddr=commaddr).filter(hdate__gt=datetime.datetime.strptime(last_readtime.strip(),"%Y-%m-%d")).all()
                if added.exists():
                    count += added.count()
                    for d in added:
                        d.save(using='zncb')

        # logger_info.info("3.hdb_flow_data_hour")
        zncb_last = HdbFlowDataHour.objects.using("zncb").filter(commaddr=commaddr).last()
        if zncb_last:
            last_readtime = zncb_last.hdate

            if last_readtime is None:
                continue
            # 取歙县服务器该条数据记录对比
            sx_last = HdbFlowDataHour.objects.using("shexian").filter(commaddr=commaddr).filter(hdate=last_readtime).first()
            # 取出上次最后一条数据记录之后增加的记录
            if sx_last:
                added = HdbFlowDataHour.objects.using("shexian").filter(commaddr=commaddr).filter(hdate__gt=datetime.datetime.strptime(last_readtime.strip(),"%Y-%m-%d %H")).all()
                if added.exists():
                    count += added.count()
                    for d in added:
                        d.save(using='zncb')

        # logger_info.info("4.hdb_flow_data_month")
        zncb_last = HdbFlowDataMonth.objects.using("zncb").filter(commaddr=commaddr).last()
        if zncb_last:
            last_readtime = zncb_last.hdate

            if last_readtime is None:
                continue
            # 取歙县服务器该条数据记录对比
            sx_last = HdbFlowDataMonth.objects.using("shexian").filter(commaddr=commaddr).filter(hdate=last_readtime).first()
            # 取出上次最后一条数据记录之后增加的记录
            if sx_last:
                added = HdbFlowDataMonth.objects.using("shexian").filter(commaddr=commaddr).filter(hdate__gt=datetime.datetime.strptime(last_readtime.strip(),"%Y-%m")).all()
                if added.exists():
                    count += added.count()
                    for d in added:
                        d.save(using='zncb')

        # logger_info.info("5.hdb_pressure_data")
        zncb_last = HdbPressureData.objects.using("zncb").filter(commaddr=commaddr).last()
        if zncb_last:
            last_readtime = zncb_last.readtime

            if last_readtime is None:
                continue
            # 取歙县服务器该条数据记录对比
            sx_last = HdbPressureData.objects.using("shexian").filter(commaddr=commaddr).filter(readtime=last_readtime).first()
            # 取出上次最后一条数据记录之后增加的记录
            if sx_last:
                added = HdbPressureData.objects.using("shexian").filter(commaddr=commaddr).filter(readtime__gt=datetime.datetime.strptime(last_readtime.strip(),"%Y-%m-%d %H:%M:%S")).all()
                if added.exists():
                    count += added.count()
                    for d in added:
                        d.save(using='zncb')
    # raise ValueError("Olala!")

    logger_info.info("added total {}".format(count))


class Command(BaseCommand):
    help = 'import data from A to B'

    def add_arguments(self, parser):
        # parser.add_argument('sTime', type=str)

        parser.add_argument(
            '--hdb_flow_data',
            action='store_true',
            dest='hdb_flow_data',
            default=False,
            help='import hdb_flow_data to new db'
        )

        parser.add_argument(
            '--test',
            action='store_true',
            dest='test',
            default=False,
            help='test'
        )

        parser.add_argument(
            '--hdb_flow_data_day',
            action='store_true',
            dest='hdb_flow_data_day',
            default=False,
            help='import hdb_flow_data_day to new db'
        )

        parser.add_argument(
            '--hdb_flow_data_hour',
            action='store_true',
            dest='hdb_flow_data_hour',
            default=False,
            help='import hdb_flow_data_hour to new db'
        )

        parser.add_argument(
            '--hdb_flow_data_month',
            action='store_true',
            dest='hdb_flow_data_month',
            default=False,
            help='import hdb_flow_data_month to new db'
        )

        parser.add_argument(
            '--hdb_pressure_data',
            action='store_true',
            dest='hdb_pressure_data',
            default=False,
            help='import hdb_pressure_data to new db'
        )

        parser.add_argument(
            '--bigmeter',
            action='store_true',
            dest='bigmeter',
            default=False,
            help='import bigmeter to new db'
        )

        parser.add_argument(
            '--concentrator',
            action='store_true',
            dest='concentrator',
            default=False,
            help='import concentrator to new db'
        )

        parser.add_argument(
            '--hdb_watermeter_day',
            action='store_true',
            dest='hdb_watermeter_day',
            default=False,
            help='import hdb_watermeter_day to new db'
        )

        parser.add_argument(
            '--hdb_watermeter_month',
            action='store_true',
            dest='hdb_watermeter_month',
            default=False,
            help='import hdb_watermeter_month to new db'
        )

        parser.add_argument(
            '--watermeter',
            action='store_true',
            dest='watermeter',
            default=False,
            help='import watermeter to new db'
        )

    def handle(self, *args, **options):
        # sTime = options['sTime']
        t1=time.time()
        count = 0
        if options['test']:
            
            test_job()
            # 

        if options['hdb_pressure_data']:
            
            bigmeters_qset = Bigmeter.objects.using("shexian").only('commaddr')
            print('bigmeters_qset',bigmeters_qset)
            for b in bigmeters_qset:
                commaddr = b.commaddr
                print('commaddr',commaddr)
                # 威尔沃数据库最后一条数据记录
                zncb_last = HdbPressureData.objects.using("zncb").filter(commaddr=commaddr).last()
                if zncb_last:
                    last_readtime = zncb_last.readtime

                    if last_readtime is None:
                        continue
                    # 取歙县服务器该条数据记录对比
                    sx_last = HdbPressureData.objects.using("shexian").filter(commaddr=commaddr).filter(readtime=last_readtime).first()
                    # 取出上次最后一条数据记录之后增加的记录
                    if sx_last:
                        print('last_readtime',last_readtime,zncb_last)
                        print('sx_last',sx_last)
                        added = HdbPressureData.objects.using("shexian").filter(commaddr=commaddr).filter(readtime__gt=datetime.datetime.strptime(last_readtime.strip(),"%Y-%m-%d %H:%M:%S")).all()
                        if added.exists():
                            print(added.count(),b.username,b.commaddr)
                            for d in added:
                                d.save(using='zncb')

        if options['hdb_flow_data']:
            
            bigmeters_qset = Bigmeter.objects.using("shexian").only('commaddr')
            for b in bigmeters_qset:
                commaddr = b.commaddr
                # 威尔沃数据库最后一条数据记录
                zncb_last = HdbFlowData.objects.using("zncb").filter(commaddr=commaddr).last()
                if zncb_last:
                    last_readtime = zncb_last.readtime

                    if last_readtime is None:
                        continue
                    # 取歙县服务器该条数据记录对比
                    sx_last = HdbFlowData.objects.using("shexian").filter(commaddr=commaddr).filter(readtime=last_readtime).first()
                    # 取出上次最后一条数据记录之后增加的记录
                    if sx_last:
                        print('last_readtime',last_readtime,zncb_last)
                        print('sx_last',sx_last)
                        added = HdbFlowData.objects.using("shexian").filter(commaddr=commaddr).filter(readtime__gt=datetime.datetime.strptime(last_readtime.strip(),"%Y-%m-%d %H:%M:%S")).all()
                        if added.exists():
                            print(added.count(),b.username,b.commaddr)
                            for d in added:
                                d.save(using='zncb')
            # data_qset=HdbFlowData.objects.using("virvo").filter(readtime__range=[sTime,'2018-09-20'])
            # data_qset=HdbFlowData.objects.using("zncb").all()
            # count = data_qset.count()
            # for d in data_qset:
            #     d.save(using='zncb2')

        if options['hdb_flow_data_day']:
            
            bigmeters_qset = Bigmeter2.objects.using("shexian").all()
            for b in bigmeters_qset:
                commaddr = b.commaddr
                # 威尔沃数据库最后一条数据记录
                zncb_last = HdbFlowDataDay.objects.using("zncb").filter(commaddr=commaddr).last()
                if zncb_last:
                    last_readtime = zncb_last.hdate

                    if last_readtime is None:
                        continue
                    # 取歙县服务器该条数据记录对比
                    sx_last = HdbFlowDataDay.objects.using("shexian").filter(commaddr=commaddr).filter(hdate=last_readtime).first()
                    # 取出上次最后一条数据记录之后增加的记录
                    if sx_last:
                        print('last_readtime',last_readtime,zncb_last)
                        print('sx_last',sx_last)
                        added = HdbFlowDataDay.objects.using("shexian").filter(commaddr=commaddr).filter(hdate__gt=datetime.datetime.strptime(last_readtime.strip(),"%Y-%m-%d")).all()
                        if added.exists():
                            print(added.count(),b.username,b.commaddr)
                            for d in added:
                                d.save(using='zncb')

            # data_qset=HdbFlowData.objects.using("virvo").filter(readtime__range=[sTime,'2018-09-20'])
            # data_qset=HdbFlowDataDay.objects.using("zncb").all()
            # count = data_qset.count()
            # for d in data_qset:
            #     d.save(using='zncb2')

        if options['hdb_flow_data_hour']:
            
            bigmeters_qset = Bigmeter2.objects.using("shexian").all()
            for b in bigmeters_qset:
                commaddr = b.commaddr
                # 威尔沃数据库最后一条数据记录
                zncb_last = HdbFlowDataHour.objects.using("zncb").filter(commaddr=commaddr).last()
                if zncb_last:
                    last_readtime = zncb_last.hdate

                    if last_readtime is None:
                        continue
                    # 取歙县服务器该条数据记录对比
                    sx_last = HdbFlowDataHour.objects.using("shexian").filter(commaddr=commaddr).filter(hdate=last_readtime).first()
                    # 取出上次最后一条数据记录之后增加的记录
                    if sx_last:
                        print('last_readtime',last_readtime,zncb_last)
                        print('sx_last',sx_last)
                        added = HdbFlowDataHour.objects.using("shexian").filter(commaddr=commaddr).filter(hdate__gt=datetime.datetime.strptime(last_readtime.strip(),"%Y-%m-%d %H")).all()
                        if added.exists():
                            print(added.count(),b.username,b.commaddr)
                            for d in added:
                                d.save(using='zncb')
            # data_qset=HdbFlowData.objects.using("virvo").filter(readtime__range=[sTime,'2018-09-20'])
            # data_qset=HdbFlowDataHour.objects.using("zncb").all()
            # count = data_qset.count()
            # for d in data_qset:
            #     d.save(using='zncb2')

        if options['hdb_flow_data_month']:
            
            bigmeters_qset = Bigmeter2.objects.using("shexian").all()
            for b in bigmeters_qset:
                commaddr = b.commaddr
                # 威尔沃数据库最后一条数据记录
                zncb_last = HdbFlowDataMonth.objects.using("zncb").filter(commaddr=commaddr).last()
                if zncb_last:
                    last_readtime = zncb_last.hdate

                    if last_readtime is None:
                        continue
                    # 取歙县服务器该条数据记录对比
                    sx_last = HdbFlowDataMonth.objects.using("shexian").filter(commaddr=commaddr).filter(hdate=last_readtime).first()
                    # 取出上次最后一条数据记录之后增加的记录
                    if sx_last:
                        print('last_readtime',last_readtime,zncb_last)
                        print('sx_last',sx_last)
                        added = HdbFlowDataMonth.objects.using("shexian").filter(commaddr=commaddr).filter(hdate__gt=datetime.datetime.strptime(last_readtime.strip(),"%Y-%m")).all()
                        if added.exists():
                            print(added.count(),b.username,b.commaddr)
                            for d in added:
                                d.save(using='zncb')
            # data_qset=HdbFlowData.objects.using("virvo").filter(readtime__range=[sTime,'2018-09-20'])
            # data_qset=HdbFlowDataMonth.objects.using("zncb").all()
            # count = data_qset.count()
            # for d in data_qset:
            #     d.save(using='zncb2')

        aft=0
        if options['bigmeter']:
            
            
            # data_qset=HdbFlowData.objects.using("virvo").filter(readtime__range=[sTime,'2018-09-20'])
            data_qset=Bigmeter.objects.using("shexian").values_list('commaddr','commstate','meterstate','gprsv','meterv',
                'signlen','lastonlinetime','pressure','plustotalflux','reversetotalflux','flux','totalflux','pressurereadtime',
                'fluxreadtime','username')
            
            for d in data_qset:
                commaddr = d[0]
                try:
                    d2=Bigmeter.objects.using("zncb").get(commaddr=commaddr)
                except:
                    print("{} {} not exists in virovo db".format(d[14],d[0]))
                    continue
                if d2:
                    d2.commstate = d[1]
                    d2.meterstate = d[2]
                    d2.gprsv = d[3]
                    d2.meterv = d[4]
                    d2.signlen = d[5]
                    d2.lastonlinetime = d[6]
                    d2.pressure = d[7]
                    d2.plustotalflux = d[8]
                    d2.reversetotalflux = d[9]
                    d2.flux = d[10]
                    d2.totalflux = d[11]
                    d2.pressurereadtime = d[12]
                    d2.fluxreadtime = d[13]
                    
                    d2.save(using='zncb')
                    
        if options['watermeter']:
            
            wmeters_qset = Watermeter.objects.using("shexian").values_list("id","communityid","rvalue","fvalue","meterstate","commstate",
                "rtime","lastrvalue","lastrtime","dosage","valvestate","lastwritedate","lastwritevalue","meterv","wateraddr")
            print("watermeter count",wmeters_qset.count())
            cnt = 0
            cnt2 = 0
            for w in wmeters_qset:
                waterid = w[0]
                communityid = w[1]
                wateraddr = w[14]
                # watermeter data
                try:
                    v = Watermeter.objects.using("zncb").get(wateraddr=wateraddr)
                except:
                    # print("{} not exists in bsc2000".format(waterid))
                    cnt += 1
                    continue

                if v:
                    if v.id != w[0]:
                        v.id = w[0]
                        cnt2 += 1
                    v.rvalue = w[2]
                    v.fvalue = w[3]
                    v.meterstate = w[4]
                    v.commstate = w[5]
                    v.rtime = w[6]
                    v.lastrvalue = w[7]
                    v.lastrtime = w[8]
                    v.dosage = w[9]
                    v.valvestate = w[10]
                    v.lastwritedate = w[11]
                    v.lastwritevalue = w[12]
                    v.meterv = w[13]
                    v.save(using='zncb')


                # hdb_watermeter_day
                # 威尔沃数据库最后一条数据记录
                zncb_last = HdbWatermeterDay.objects.using("zncb").filter(waterid=waterid).order_by("hdate").filter(communityid=communityid).last()
                # print('zncb_last',zncb_last.waterid,zncb_last.hdate,zncb_last.communityid)
                if zncb_last:
                    last_readtime = zncb_last.rtime

                    if last_readtime is None:
                        continue
                    # 取歙县服务器该条数据记录对比
                    sx_last = HdbWatermeterDay.objects.using("shexian").filter(waterid=waterid).filter(communityid=communityid).filter(rtime=last_readtime).first()
                    # 取出上次最后一条数据记录之后增加的记录
                    # print('sx_last',sx_last.waterid,sx_last.hdate,sx_last.communityid)
                    if sx_last:
                        # print('last_readtime',last_readtime,zncb_last)
                        # print('sx_last',sx_last)
                        added = HdbWatermeterDay.objects.using("shexian").filter(waterid=waterid).filter(communityid=communityid).filter(rtime__gt=datetime.datetime.strptime(last_readtime.strip(),"%Y-%m-%d %H:%M:%S")).all()
                        if added.exists():
                            # print(added.count(),waterid,communityid)
                            count += added.count()
                            for d in added:
                                try:
                                    HdbWatermeterDay.objects.create(waterid=d.waterid,rvalue=d.rvalue,fvalue=d.fvalue,rtime=d.rtime,hdate=d.hdate,
                                        meterstate=d.meterstate,commstate=d.commstate,dosage=d.dosage,communityid=d.communityid)
                                except:
                                    pass

                # hdb_watermeter_month
                # 威尔沃数据库最后一条数据记录
                zncb_last = HdbWatermeterMonth.objects.using("zncb").filter(waterid=waterid).filter(communityid=communityid).order_by("hdate").last()
                # print('zncb_last',zncb_last.waterid,zncb_last.hdate,zncb_last.communityid)
                if zncb_last:
                    last_readtime = zncb_last.hdate

                    if last_readtime is None:
                        continue
                    # 取歙县服务器该条数据记录对比
                    sx_last = HdbWatermeterMonth.objects.using("shexian").filter(waterid=waterid).filter(communityid=communityid).filter(hdate=last_readtime).first()
                    # 取出上次最后一条数据记录之后增加的记录
                    # print('sx_last',sx_last.waterid,sx_last.hdate,sx_last.communityid)
                    if sx_last:
                        # print('last_readtime',last_readtime,zncb_last)
                        # print('sx_last',sx_last)
                        added = HdbWatermeterMonth.objects.using("shexian").filter(waterid=waterid).filter(communityid=communityid).filter(hdate__gt=datetime.datetime.strptime(last_readtime.strip(),"%Y-%m")).all()
                        if added.exists():
                            # print(added.count(),waterid,communityid)
                            count= added.count()
                            
                            for d in added:
                                try:
                                    HdbWatermeterMonth.objects.create(waterid=d.waterid,hdate=d.hdate,
                                    dosage=d.dosage,communityid=d.communityid)
                                except:
                                    pass
                
        
            print('cnt=',cnt,cnt2)
        t2 = time.time() - t1
        self.stdout.write(self.style.SUCCESS(f'total {count}  Affected {aft} row(s)!,elapsed {t2}'))
