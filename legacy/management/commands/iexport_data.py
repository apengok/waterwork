from django.core.management.base import BaseCommand, CommandError


from legacy.models import (HdbFlowData,HdbFlowDataDay,HdbFlowDataHour,HdbFlowDataMonth,HdbPressureData,Bigmeter,
    Watermeter,HdbWatermeterDay,HdbWatermeterMonth,Concentrator,Community,SecondWater,
    HdbFlowDataMonth)

import time
import datetime
import logging

from dmam.models import VConcentrator,VWatermeter,VCommunity,VSecondWater
from entm.models import Organizations

logger_info = logging.getLogger('info_logger')

def update_watermeterday():
    waterid = 36545
    communityid = 105
    count = 0
    # hdb_watermeter_day
    # 威尔沃数据库最后一条数据记录
    zncb_last = HdbWatermeterDay.objects.using("shexian").values()
    print("zncb all count:",zncb_last.count())
    logger_info.info("shexian waterterday records :{}".format(zncb_last.count()))
    # virvo_last = HdbWatermeterDay.objects.using("zncb").filter(waterid=waterid).order_by("hdate").values()
    # print("virvo all count:",virvo_last.count())
    for z in zncb_last:
        waid = z["waterid"]
        hdate = z["hdate"]
        coid = z["communityid"]

        vs = HdbWatermeterDay.objects.filter(waterid=waid,hdate=hdate,communityid=coid)
        if vs.exists():
            pass
            # vs.first().update(
            # rvalue = z["rvalue"],
            # fvalue = z["fvalue"],
            # meterstate = z["meterstate"],
            # commstate = z["commstate"],
            # rtime = z["rtime"],
            # dosage = z["dosage"])
        else:
            logger_info.info("{},{},{} not exist".format(waid,hdate,coid))
        # print(vs)
        # if vs.exists():
        #     v = vs.first()
        #     v.rvalue = z["rvalue"]
        #     v.fvalue = z["fvalue"]
        #     v.meterstate = z["meterstate"]
        #     v.commstate = z["commstate"]
        #     v.rtime = z["rtime"]
        #     v.dosage = z["dosage"]

        #     # v.save(using="zncb")
        # else:
        #     print(vs,"exists ?")
            # HdbWatermeterDay.objects.using("zncb").create(z)

def update_watermetermonth():
    waterid = 15666
    count = 0
    communityid = 105
    # hdb_watermeter_month
    # 威尔沃数据库最后一条数据记录
    zncb_last = HdbWatermeterMonth.objects.using("shexian").values()
    print("zncb all count:",zncb_last.count())
    logger_info.info("shexian watertermonth records :{}".format(zncb_last.count()))

    virvo_last = HdbWatermeterMonth.objects.values()
    print("virvo all count:",virvo_last.count())
    logger_info.info("virvo watertermonth records :{}".format(virvo_last.count()))
    for z in zncb_last:
        waid = z["waterid"]
        hdate = z["hdate"]
        coid = z["communityid"]

        vs = HdbWatermeterMonth.objects.filter(waterid=waid,hdate=hdate,communityid=coid)
        if vs.exists():
            pass
            # vs.first().update(
            # rvalue = z["rvalue"],
            # fvalue = z["fvalue"],
            # meterstate = z["meterstate"],
            # commstate = z["commstate"],
            # rtime = z["rtime"],
            # dosage = z["dosage"])
        else:
            logger_info.info("{},{},{} not exist in watertermonthr".format(waid,hdate,coid))


def test_manager():
    hdd = HdbFlowDataMonth.objects.using("shexian").history('64892354861',4).values()
    print (hdd.count())
    for h in hdd:
        print(h)
    
def test_hdb_watermeter_month():
    hdd = HdbWatermeterMonth.community_use("105",4)
    print(hdd)

def test_community():
    count = 0
    sx_community = Community.objects.using("shexian").values()
    print("shexian:commuinity count:",sx_community.count())
    v_community = VCommunity.objects.values()
    print("virvo vcommunity count:",v_community.count())
    organ = Organizations.objects.get(name="歙县自来水公司")
    for d in sx_community:
        name = d["name"]
        address = d["address"]
        commutid = d["id"]
        
        d2=VCommunity.objects.filter(commutid=commutid)
        
        if not d2.exists():
            count += 1
            instance = VCommunity.objects.create(name=name,address=address,belongto=organ,commutid=commutid,outter="歙县")
        else:
            d2i = d2.first()
            if d2i.name != name:
                print(d2i.name,name)
            d2i.name = name
            # d2.update(name=name,outter="歙县")
            d2i.outter = "歙县"
            d2i.save()


    print("{} added".format(count))

def test_watermeter():
    count = 0
    sx_watermeter = Watermeter.objects.using("shexian").values()
    print("shexian watermeter counter:",sx_watermeter.count())
    v_watermeter =VWatermeter.objects.values()
    print("Virvo watermeter counter:",v_watermeter.count())

    organ = Organizations.objects.get(name="歙县自来水公司")
    for d in sx_watermeter:
        name = d["roomname"]
        waterid = d["id"]
        wateraddr = d["wateraddr"]
        commutid = d["communityid"]

        numbersth = d["numbersth"]
        buildingname = d["buildingname"]
        roomname = d["roomname"]
        nodeaddr = d["nodeaddr"]
        username = d["username"]
        usertel = d["usertel"]
        dn = d['dn']
        serialnumber = d["serialnumber"]
        manufacturer = d["manufacturer"]
        madedate = d["madedate"]
        installationsite=d["installationsite"]

        rvalue = d["rvalue"],
        fvalue = d["fvalue"],
        meterstate = d["meterstate"],
        commstate = d["commstate"],
        rtime = d["rtime"],
        lastrvalue = d["lastrvalue"],
        lastrtime = d["lastrtime"],
        dosage = d["dosage"],
        valvestate = d["valvestate"],
        lastwritedate = d["lastwritedate"],
        lastwritevalue = d["lastwritevalue"],
        meterv = d["meterv"]

        Vcomut = VCommunity.objects.get(commutid=commutid) #所属小区
        
        d2=VWatermeter.objects.filter(wateraddr=wateraddr)
        
        if not d2.exists():
            print("{} VWatermeter not exists".format(waterid))
            count += 1
        else:
            amrs_d = Watermeter.objects.filter(id=waterid)
            if amrs_d.exists():
                if amrs_d.count()>1:
                    for a in amrs_d:
                        print("\t&*^&%&--{} {}".format(a.id,a.wateraddr))
                else:
                    d2.update(amrs_waterid=amrs_d[0].id)

        if d2.count() > 1:
            for x in d2:
                print("\t\t {} {} {} repeat?".format(x.waterid,x.wateraddr,x.nodeaddr))
                if x.waterid != waterid:
                    x.delete()
        # 
        # if not amrs_d.exists():
        #     print("{} Watermeter not exists".format(waterid))

    print("not exists,",count)
        



    print("{} watermeter added".format(count))

# 先执行小区和小表的同步，保证waterid和communityid都存在
def test_hdb_watermeter_data_month():
    count = 0
    updated = 0
    sx_wmdm = HdbWatermeterMonth.objects.using("shexian").values()
    print("shexian HdbWatermeterMonth count:",sx_wmdm.count())
    v_community = VCommunity.objects.values_list("commutid","pk")
    v_community_dict = dict(v_community)
    v_watermeter = VWatermeter.objects.values_list("waterid","pk")
    v_watermeter_dict = dict(v_watermeter)

    for d in sx_wmdm:
        sx_waterid = d["waterid"]
        sx_communityid = d["communityid"]
        sx_hdate = d["hdate"]
        dosage = d["dosage"]
        v_waterid = v_watermeter_dict.get(sx_waterid) or None
        v_communityid = v_community_dict.get(sx_communityid) or None

        if v_waterid is None:
            continue
        if v_communityid is None:
            continue

        # s_wmdm = HdbWatermeterMonth.objects.filter(waterid=sx_waterid,hdate=sx_hdate,communityid=sx_communityid)

        # # 1.查询歙县的waterid和communityid
        # if s_wmdm.exists():
        #     # jango.db.utils.IntegrityError: (1062, "Duplicate entry '1-2018-05-3' for key 'PRIMARY'")
        #     # 因为存在 "{}_{}_{}".format(v_waterid,hdate,v_communityid)
        #     # 应该直接用实际应该的id覆盖掉
        #     s_wmdm.update(waterid=v_waterid,communityid=v_communityid,dosage=dosage)
        #     updated += 1
        # else:
            # 2.如果不存在再用VWatermeter和VCommunity实际的id查询,纠正错误
        v_wmdm = HdbWatermeterMonth.objects.filter(waterid=v_waterid,hdate=sx_hdate,communityid=v_communityid)
        if v_wmdm.exists():
            v_wmdm.update(waterid=v_waterid,communityid=v_communityid,dosage=dosage)
            updated += 1
        else:
            HdbWatermeterMonth.objects.create(waterid=v_waterid,communityid=v_communityid,hdate=sx_hdate,dosage=dosage)
            count += 1

    print("added {} , updated {}".format(count,updated))


def test_hdb_watermeter_data_day():
    count = 0
    updated = 0
    sx_wmdm = HdbWatermeterDay.objects.using("shexian").values()
    print("shexian HdbWatermeterMonth count:",sx_wmdm.count())
    v_community = VCommunity.objects.values_list("commutid","pk")
    v_community_dict = dict(v_community)
    v_watermeter = VWatermeter.objects.values_list("waterid","pk")
    v_watermeter_dict = dict(v_watermeter)

    for d in sx_wmdm:
        sx_waterid = d["waterid"]
        sx_communityid = d["communityid"]
        sx_hdate = d["hdate"]
        dosage = d["dosage"]
        rtime = d["rtime"]
        commstate= d["commstate"]
        rvalue = d["rvalue"]
        fvalue = d["fvalue"]
        v_waterid = v_watermeter_dict.get(sx_waterid) or None
        v_communityid = v_community_dict.get(sx_communityid) or None

        if v_waterid is None:
            continue
        if v_communityid is None:
            continue

        
            # 2.如果不存在再用VWatermeter和VCommunity实际的id查询,纠正错误
        v_wmdm = HdbWatermeterDay.objects.filter(waterid=v_waterid,hdate=sx_hdate,communityid=v_communityid)
        if v_wmdm.exists():
            v_wmdm.update(waterid=v_waterid,communityid=v_communityid,dosage=dosage,rtime=rtime,rvalue=rvalue,fvalue=fvalue,commstate=commstate)
            updated += 1
        else:
            HdbWatermeterDay.objects.create(waterid=v_waterid,communityid=v_communityid,hdate=sx_hdate,dosage=dosage,rtime=rtime,rvalue=rvalue,fvalue=fvalue,commstate=commstate)
            count += 1

    print("added {} , updated {}".format(count,updated))


def test_pwl():
    # return test_hdb_watermeter_data_day()
    # return test_hdb_watermeter_data_month()
    return test_watermeter()
    return test_community()
    return test_hdb_watermeter_month()
    return test_manager()
    # return update_watermeterday()
    return update_watermetermonth()
    waterid = 36544
    communityid = 105
    count = 0
    # hdb_watermeter_day
    # 威尔沃数据库最后一条数据记录
    zncb_last = HdbWatermeterDay.objects.using("zncb").filter(waterid=waterid).order_by("hdate").last()
    # print("zncb count",zncb_last.count())
    print('zncb_last',zncb_last.waterid,zncb_last.hdate,zncb_last.communityid)
    if zncb_last:
        last_readtime = zncb_last.rtime
        print("last_readtime:",last_readtime)
        if last_readtime is None:
            print("lastreadtime none/")
        # 取歙县服务器该条数据记录对比
        sx_last = HdbWatermeterDay.objects.using("shexian").filter(waterid=waterid).filter(rtime=last_readtime).first()
        # 取出上次最后一条数据记录之后增加的记录
        print('sx_last',sx_last.waterid,sx_last.hdate,sx_last.communityid)
        if sx_last:
            # print('last_readtime',last_readtime,zncb_last)
            # print('sx_last',sx_last)
            added = HdbWatermeterDay.objects.using("shexian").filter(waterid=waterid).filter(rtime__gt=datetime.datetime.strptime(last_readtime.strip(),"%Y-%m-%d %H:%M:%S")).all()
            if added.exists():
                print("added count:",added.count())
                count += added.count()
                added_list = []
                for d in added:
                    print(d)
                    added_list.append(HdbWatermeterDay(waterid=d.waterid,rvalue=d.rvalue,fvalue=d.fvalue,rtime=d.rtime,hdate=d.hdate,
                            meterstate=d.meterstate,commstate=d.commstate,dosage=d.dosage,communityid=d.communityid) )
                try:
                    # HdbWatermeterDay.objects.bulk_create(added_list)
                    print("added list count:",len(added_list))
                except Exception as e:
                    print("1.",e)


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

        parser.add_argument(
            '--vwatermeter',
            action='store_true',
            dest='vwatermeter',
            default=False,
            help='import vwatermeter to new db'
        )

        parser.add_argument(
            '--community',
            action='store_true',
            dest='community',
            default=False,
            help='import community to new db'
        )


        parser.add_argument(
            '--update_hdb_flow_month',
            action='store_true',
            dest='update_hdb_flow_month',
            default=False,
            help='import update_hdb_flow_month to new db'
        )

        parser.add_argument(
            '--secondwater',
            action='store_true',
            dest='secondwater',
            default=False,
            help='import secondwater to new db'
        )


    def handle(self, *args, **options):
        # sTime = options['sTime']
        t1=time.time()
        count = 0
        if options['test']:
            
            # test_job()
            test_pwl()
            # update_pwl()
            # 

        if options['secondwater']:
            organ = Organizations.objects.get(name="歙县自来水公司")
            zncb_sw = SecondWater.objects.values()
            for z in zncb_sw:
                name = z['name']
                address = z['address']
                lng = z['lng']
                lat = z['lat']
                coortype = z['coortype']
                
                VSecondWater.objects.create(name=name,address=address,lng=lng,lat=lat,coortype=coortype,belongto=organ)

        if options['update_hdb_flow_month']:
            today = datetime.date.today()
            current_month = today.strftime("%Y-%m")
            bigmeters_qset = Bigmeter.objects.using("shexian").only('commaddr')
            print('bigmeter count',bigmeters_qset.count())
            # current_month = '2018-09'
            for b in bigmeters_qset:
                commaddr = b.commaddr
                sx_flow_month = HdbFlowDataMonth.objects.using("shexian").filter(commaddr=commaddr,hdate=current_month).all()
                if sx_flow_month.exists():
                    vx_flow_month = HdbFlowDataMonth.objects.using("zncb").filter(commaddr=commaddr,hdate=current_month).all()
                    if vx_flow_month.exists():
                        sx = sx_flow_month.first()
                        vx = vx_flow_month.first()
                        sx_flow = sx.dosage
                        vx_flow = vx.dosage
                        if sx_flow != vx_flow:
                            print("month:",sx_flow,vx_flow)
                            vx.dosage = sx_flow
                            vx.save()


                # 歙县数据库当日日统 dosage
                sx_dosage = HdbFlowDataDay.objects.using("shexian").filter(commaddr=commaddr,hdate=current_day)
                if sx_dosage.exists():
                    v_dosage = HdbFlowDataDay.objects.using("zncb").filter(commaddr=commaddr,hdate=current_day)
                    if v_dosage.exists():
                        sx = sx_dosage[0].dosage
                        vx = v_dosage[0].dosage
                        if sx != vx:
                            print('day:virvo sx:',commaddr,sx,vx)
                            count += 1




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
            data_qset=Bigmeter.objects.using("shexian").values('commaddr','commstate','meterstate','gprsv','meterv',
                'signlen','lastonlinetime','pressure','plustotalflux','reversetotalflux','flux','totalflux','pressurereadtime',
                'fluxreadtime','username')
            for d in data_qset:
                commaddr = d["commaddr"]
                username = d["username"]
                print("shexian:",username,commaddr)
                try:
                    dt=Bigmeter.objects.using("zncb").filter(commaddr=commaddr)
                except:
                    print("{} {} not exists in virovo db".format(d["username"],d["commaddr"]))
                    continue
                if dt.exists():
                    for d2 in dt:
                        print(" &*^*%&*---virvo:",d2.username,d2.commaddr)
                        d2.commstate = d["commstate"]
                        d2.meterstate = d["meterstate"]
                        d2.gprsv = d["gprsv"]
                        d2.meterv = d["meterv"]
                        d2.signlen = d["signlen"]
                        d2.lastonlinetime = d["lastonlinetime"]
                        d2.pressure = d["pressure"]
                        d2.plustotalflux = d["plustotalflux"]
                        d2.reversetotalflux = d["reversetotalflux"]
                        d2.flux = d["flux"]
                        d2.totalflux = d["totalflux"]
                        d2.pressurereadtime = d["pressurereadtime"]
                        d2.fluxreadtime = d["fluxreadtime"]
                        
                        d2.save(using='zncb')
                    

        if options['watermeter']:
            
            wmeters_qset = Watermeter.objects.using("shexian").values("id","communityid","rvalue","fvalue","meterstate","commstate",
                "rtime","lastrvalue","lastrtime","dosage","valvestate","lastwritedate","lastwritevalue","meterv","wateraddr")
            print("watermeter count",wmeters_qset.count())
            cnt = 0
            cnt2 = 0
            for w in wmeters_qset:
                waterid = w["id"]
                communityid = w["communityid"]
                wateraddr = w["wateraddr"]
                # watermeter data
                try:

                    Watermeter.objects.using("zncb").filter(wateraddr=wateraddr).update(
                        rvalue = w["rvalue"],
                        fvalue = w["fvalue"],
                        meterstate = w["meterstate"],
                        commstate = w["commstate"],
                        rtime = w["rtime"],
                        lastrvalue = w["lastrvalue"],
                        lastrtime = w["lastrtime"],
                        dosage = w["dosage"],
                        valvestate = w["valvestate"],
                        lastwritedate = w["lastwritedate"],
                        lastwritevalue = w["lastwritevalue"],
                        meterv = w["meterv"])
                except Exception as e:
                    # print("{} not exists in bsc2000".format(waterid))
                    print("0.",e)
                    continue

                


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
                            added_list = []
                            for d in added:
                                added_list.append(HdbWatermeterDay(waterid=d.waterid,rvalue=d.rvalue,fvalue=d.fvalue,rtime=d.rtime,hdate=d.hdate,
                                        meterstate=d.meterstate,commstate=d.commstate,dosage=d.dosage,communityid=d.communityid) )
                            try:
                                HdbWatermeterDay.objects.bulk_create(added_list)
                            except Exception as e:
                                print("1.",e)

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
                            added_list = []
                            for d in added:
                                added_list.append(HdbWatermeterMonth(waterid=d.waterid,hdate=d.hdate,
                                    dosage=d.dosage,communityid=d.communityid) )
                            try:
                                HdbWatermeterMonth.objects.bulk_create(added_list)
                            except Exception as e:
                                print("2.",e)

        if options['concentrator']:
            
            
            # data_qset=HdbFlowData.objects.using("virvo").filter(readtime__range=[sTime,'2018-09-20'])
            data_qset=Concentrator.objects.using("zncb").values_list('name','commaddr')
            organ = Organizations.objects.get(name="歙县自来水公司")
            for d in data_qset:
                name = d[0]
                commaddr = d[1]
                
                d2=VConcentrator.objects.filter(name=name)
                
                if not d2.exists():
                    VConcentrator.objects.create(name=name,commaddr=commaddr,belongto=organ)
                    

        if options['community']:
            
            
            # data_qset=HdbFlowData.objects.using("virvo").filter(readtime__range=[sTime,'2018-09-20'])
            data_qset=Community.objects.using("zncb").all()
            organ = Organizations.objects.get(name="歙县自来水公司")
            for d in data_qset:
                name = d.name
                address = d.address
                
                d2=VCommunity.objects.filter(name=name)
                
                if not d2.exists():
                    count += 1
                    VCommunity.objects.create(name=name,address=address,belongto=organ,commutid=d.id)


        # 在waterwork数据库中创建zncb对应的小表
        if options['vwatermeter']:
            
            
            # data_qset=HdbFlowData.objects.using("virvo").filter(readtime__range=[sTime,'2018-09-20'])
            data_qset=Watermeter.objects.using("zncb").all()
            print("watermeter count",data_qset.count())
            organ = Organizations.objects.get(name="歙县自来水公司")
            for d in data_qset:
                name = d.roomname
                waterid = d.id
                wateraddr = d.wateraddr
                commutid = d.communityid
                Vcomut = VCommunity.objects.get(commutid=commutid)
                
                d2=VWatermeter.objects.filter(waterid=waterid)
                
                if not d2.exists():
                    count += 1
                    VWatermeter.objects.create(name=name,waterid=waterid,wateraddr=wateraddr,belongto=organ,communityid=Vcomut)
                    
                
        
        # print('cnt=',cnt,cnt2)
        t2 = time.time() - t1
        self.stdout.write(self.style.SUCCESS(f'total {count}  Affected {aft} row(s)!,elapsed {t2}'))
