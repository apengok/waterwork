from django.core.management.base import BaseCommand, CommandError
from django.db import connections

from legacy.models import (HdbFlowData,HdbFlowDataDay,HdbFlowDataHour,HdbFlowDataMonth,HdbPressureData,Bigmeter,
    Watermeter,HdbWatermeterDay,HdbWatermeterMonth,Concentrator,Community,SecondWater,
    HdbFlowDataMonth)

import time
import datetime
import logging

from dmam.models import VConcentrator,VWatermeter,VCommunity,VSecondWater
from entm.models import Organizations

logger_info = logging.getLogger('info_logger')


def close_old_connections():
    for conn in connections.all():
        conn.close_if_unusable_or_obsolete()

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
    # VCommunity.objects.all().delete()

    sx_community = Community.objects.using("shexian").values()
    s_list = [(x["name"],x["id"]) for x in sx_community]
    print("shexian:commuinity count:",sx_community.count())
    a_community = Community.objects.values()
    a_list = [(x["name"],x["id"]) for x in a_community]

    s_dict = dict(s_list)
    a_dict = dict(a_list)
    addr_dict = dict([(x["name"],x["address"]) for x in sx_community])


    
    organ = Organizations.objects.get(name="歙县自来水公司")
    comuterewlist = []
    for k,v in s_dict.items():
        # k=name,v=id
        address = addr_dict.get(k)
        commutid = v
        amrs_commutid = a_dict.get(k)
    #     t=VCommunity(belongto=organ,name=k,address=address,commutid=commutid,amrs_commutid=amrs_commutid)
    #     comuterewlist.append(t)
    # VCommunity.objects.bulk_create(comuterewlist)
        
        

    print("{} added".format(len(s_dict)))

def test_watermeter():
    count = 0
    # VWatermeter.objects.all().delete()

    # HdbWatermeterDay.objects.filter(waterid=0).update(waterid=60423)
    # HdbWatermeterMonth.objects.filter(waterid=0).update(waterid=60423)
    # return

    sx_watermeter = Watermeter.objects.using("shexian").values()
    print("shexian watermeter counter:",sx_watermeter.count())
    vamrs_watermeter =Watermeter.objects.values()
    # wwork_watermeter = VWatermeter.objects.values()
    
    print("Virvo watermeter counter:",vamrs_watermeter.count())
    sx_waterids = [x["id"] for x in sx_watermeter]
    v_waterids = [x["id"] for x in vamrs_watermeter]
    sx_tmpkeys = [("{}_{}".format(x["nodeaddr"],x["wateraddr"]),x["id"] ) for x in sx_watermeter]
    ns_tmpkeys = [("{}_{}".format(x["nodeaddr"],x["wateraddr"]),x["numbersth"] ) for x in sx_watermeter]
    bn_tmpkeys = [("{}_{}".format(x["nodeaddr"],x["wateraddr"]),x["buildingname"] ) for x in sx_watermeter]
    rm_tmpkeys = [("{}_{}".format(x["nodeaddr"],x["wateraddr"]),x["roomname"] ) for x in sx_watermeter]
    c_tmpkeys = [("{}_{}".format(x["nodeaddr"],x["wateraddr"]),x["communityid"] ) for x in sx_watermeter]
    v_tmpkeys = [("{}_{}".format(x["nodeaddr"],x["wateraddr"]),x["id"] ) for x in vamrs_watermeter]
    # w_tmpkeys = [("{}_{}".format(x["nodeaddr"],x["wateraddr"]),x["waterid"] ) for x in wwork_watermeter]
    
    sx_dicts = dict(sx_tmpkeys)
    v_dicts = dict(v_tmpkeys)
    n_dicts = dict(ns_tmpkeys)
    b_dicts = dict(bn_tmpkeys)
    r_dicts = dict(rm_tmpkeys)
    c_dicts = dict(c_tmpkeys)
    # w_dicts = dict(w_tmpkeys)
    v_workmeterlist=[]
    organ = Organizations.objects.get(name="歙县自来水公司")
    for k,v in sx_dicts.items():
        vv = v_dicts.get(k)
        # ww = w_dicts.get(k)
        if v != vv:
            print(k,v,'<->',k,vv)
        naddr,waddr = k.split("_")
        numbersth = n_dicts.get(k)
        buildingname = b_dicts.get(k)
        roomname = r_dicts.get(k)
        c_commutid = c_dicts.get(k)
        
        communityid = VCommunity.objects.get(commutid=c_commutid)
        t = VWatermeter.objects.create(belongto=organ,nodeaddr=naddr,wateraddr=waddr,waterid=v,amrs_waterid=vv,
            numbersth=numbersth,buildingname=buildingname,roomname=roomname,communityid=communityid)
        v_workmeterlist.append(t)
        
    # VWatermeter.objects.bulk_create(v_workmeterlist)
    return
    
    


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

def test_sync_watermeter(day):
    nocnt = 0
    
    today = datetime.datetime.today()
    t1=time.time()

    logger_info.info("sync Watermeter data and flow data from shexian")

    sx_wms = Watermeter.objects.using("shexian").values("id","communityid","rvalue","fvalue","meterstate","commstate",
                "rtime","lastrvalue","lastrtime","dosage","valvestate","lastwritedate","lastwritevalue","meterv","wateraddr")
    # bool(sx_wms)
    v_community = VCommunity.objects.values_list("commutid","amrs_commutid")
    v_community_dict = dict(v_community)
    v_watermeter = VWatermeter.objects.values_list("waterid","amrs_waterid")
    v_watermeter_dict = dict(v_watermeter)

    for w in sx_wms:
        waterid = w["id"] #歙县watermeter id
        communityid = w["communityid"]
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
        meterv = w["meterv"]
        v_ww_waterid = v_watermeter_dict.get(waterid) or None

        


        if v_ww_waterid is not None:
            v_ww_commutid = v_community_dict.get(communityid)
            if v_ww_commutid is None:
                logger_info("community id {} is None ".format(v_ww_commutid))
                continue

            Watermeter.objects.filter(id=v_ww_waterid).update(
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

            # update flow data day and month
            # for i in range(2):
            #     day = today - datetime.timedelta(days=i)
            #     day_str = day.strftime("%Y-%m-%d")
            #     test_sync_wm_day(waterid,day_str,v_ww_commutid)
            test_sync_wm_day(waterid,day,v_ww_commutid)
            test_sync_wm_month(waterid,day[:7],v_ww_commutid)

        else:
            nocnt += 1
            logger_info.info("{} not in virvo DB".format(waterid))

    if nocnt > 0:
        logger_info.info("total {} not in virvo DB".format(nocnt))
    
    t2 = time.time() - t1
    logger_info.info("time last{}:".format(t2))  


def test_sync_wm_day(waterid,day,communityid):
    wm_flow_day = HdbWatermeterDay.objects.using("shexian").filter(waterid=waterid,hdate=day).values()
    added_list = []
    for wd in wm_flow_day:
        rvalue = wd["rvalue"]
        fvalue = wd["fvalue"]
        meterstate = wd["meterstate"]
        commstate = wd["commstate"]
        rtime = wd["rtime"]
        dosage = wd["dosage"]
        communityid= wd["communityid"]

        vd = HdbWatermeterDay.objects.filter(waterid=waterid,hdate=day)
        if vd.exists():
            vd.update(rvalue=rvalue,fvalue=fvalue,meterstate=meterstate,commstate=commstate,rtime=rtime,dosage=dosage)
        else:
            t=HdbWatermeterDay(waterid=waterid,hdate=day,rvalue=rvalue,fvalue=fvalue,meterstate=meterstate,
                commstate=commstate,rtime=rtime,communityid=communityid)
            added_list.append(t)

    if len(added_list) > 0:
        HdbWatermeterDay.objects.bulk_create(added_list)


def test_sync_wm_month(waterid,ymon,communityid):
    wm_flow_day = HdbWatermeterMonth.objects.using("shexian").filter(waterid=waterid,hdate=ymon).values()
    added_list = []
    for wd in wm_flow_day:
        dosage = wd["dosage"]
        communityid= wd["communityid"]

        vd = HdbWatermeterMonth.objects.filter(waterid=waterid,hdate=ymon)
        if vd.exists():
            vd.update(dosage=dosage)
        else:
            t=HdbWatermeterMonth(waterid=waterid,hdate=ymon,dosage=dosage,communityid=communityid)
            added_list.append(t)

    if len(added_list) > 0:
        HdbWatermeterMonth.objects.bulk_create(added_list)


def test_sync_bigmeter():
    nocnt = 0
    today = datetime.datetime.today()
    # day = today.strftime("%Y-%m-%d")
    logger_info.info("sync Bigmeter data and flow data:")
    sx_bms = Bigmeter.objects.using("shexian").values('commaddr','commstate','meterstate','gprsv','meterv',
                'signlen','lastonlinetime','pressure','plustotalflux','reversetotalflux','flux','totalflux','pressurereadtime',
                'fluxreadtime','username')
    for sb in sx_bms:
        commaddr = sb["commaddr"]
        name = sb["username"]

        fluxreadtime = sb["fluxreadtime"]
        flux = sb["flux"]
        totalflux = sb["totalflux"]
        plustotalflux = sb["plustotalflux"]
        reversetotalflux = sb["reversetotalflux"]
        pressurereadtime = sb["pressurereadtime"]
        pressure = sb["pressure"]
        gprsv = sb["gprsv"]
        meterv = sb["meterv"]
        signlen = sb["signlen"]
        lastonlinetime = sb["lastonlinetime"]
        commstate = sb["commstate"]
        meterstate = sb["meterstate"]
        vb = Bigmeter.objects.filter(commaddr=commaddr)
        if vb.exists():
            vb.update(fluxreadtime=fluxreadtime,flux=flux,totalflux=totalflux,plustotalflux=plustotalflux,reversetotalflux=reversetotalflux,
                pressurereadtime=pressurereadtime,pressure=pressure,gprsv=gprsv,meterv=meterv,signlen=signlen,lastonlinetime=lastonlinetime,
                commstate=commstate,meterstate=meterstate,)
            logger_info.info("{}({}):".format(name,commaddr))
            # sync flow history data
            for i in range(3):
                day = today - datetime.timedelta(days=i)
                day_str = day.strftime("%Y-%m-%d")
                logger_info.info("\t\t{}".format(day_str))
                test_sync_bgm_flows(commaddr,day_str)
                test_sync_bgm_flow_hour(commaddr,day_str)
                test_sync_bgm_flow_daily(commaddr,day_str)
        else:
            nocnt+=1
            logger_info.info("{}({}) not in Virvo DB".format(name,commaddr))

    logger_info.info("all cnt is {} ,{} not exists".format(sx_bms.count(),nocnt))

def test_sync_bgm_flows(commaddr,day):
    
    flow_day = HdbFlowData.objects.using("shexian").filter(commaddr=commaddr,readtime__startswith=day).values()
    
    added_list = []
    for fd in flow_day:
        readtime=fd["readtime"]
        flux = fd["flux"]
        plustotalflux = fd["plustotalflux"]
        reversetotalflux = fd["reversetotalflux"]
        totalflux = fd["totalflux"]
        gprsv = fd["gprsv"]
        meterv = fd["meterv"]
        meterstate = fd["meterstate"]
        
        vd = HdbFlowData.objects.filter(commaddr=commaddr,readtime=readtime)
        if vd.exists():
            vd.update(flux=flux,plustotalflux=plustotalflux,reversetotalflux=reversetotalflux,
                totalflux=totalflux,gprsv=gprsv,meterv=meterv,meterstate=meterstate)
        else:
            d = HdbFlowData(commaddr=commaddr,readtime=readtime,flux=flux,plustotalflux=plustotalflux,reversetotalflux=reversetotalflux,
                totalflux=totalflux,gprsv=gprsv,meterv=meterv,meterstate=meterstate)
            added_list.append(d)

    if len(added_list)>0:
        try:
            added=HdbFlowData.objects.bulk_create(added_list)
            
        except Exception as e:
            logger_info.info("sync flow  error,reason :",e)
        

def test_sync_bgm_flow_hour(commaddr,day):
    
    flow_day = HdbFlowDataHour.objects.using("shexian").filter(commaddr=commaddr,hdate__startswith=day).values()
    
    added_list = []
    for fd in flow_day:
        hdate=fd["hdate"]
        dosage = fd["dosage"]
        vd = HdbFlowDataHour.objects.filter(commaddr=commaddr,hdate=hdate)
        if vd.exists():
            vd.update(dosage=dosage)
        else:
            d = HdbFlowDataHour(commaddr=commaddr,hdate=hdate,dosage=dosage)
            added_list.append(d)

    if len(added_list)>0:
        try:
            added=HdbFlowDataHour.objects.bulk_create(added_list)
            
        except Exception as e:
            logger_info.info("sync flow hour error,reason :",e)

def test_sync_bgm_flow_daily(commaddr,day):
    
    flow_day = HdbFlowDataDay.objects.using("shexian").filter(commaddr=commaddr,hdate=day).values()
    
    added_list = []
    for fd in flow_day:
        dosage = fd["dosage"]
        vd = HdbFlowDataDay.objects.filter(commaddr=commaddr,hdate=day)
        if vd.exists():
            vd.update(dosage=dosage)
        else:
            d = HdbFlowDataDay(commaddr=commaddr,hdate=day,dosage=dosage)
            added_list.append(d)

    if len(added_list)>0:
        try:
            added=HdbFlowDataDay.objects.bulk_create(added_list)
            
        except Exception as e:
            logger_info.info("sync flow day error,reason :",e)

def test_sync_bgm_flow_month(commaddr,ymon):
    
    flow_day = HdbFlowDataMonth.objects.using("shexian").filter(commaddr=commaddr,hdate=ymon).values()
    # print("{} count:",flow_day.count())
    added_list = []
    for fd in flow_day:
        dosage = fd["dosage"]
        vd = HdbFlowDataMonth.objects.filter(commaddr=commaddr,hdate=ymon)
        if vd.exists():
            vd.update(dosage=dosage)
        else:
            d = HdbFlowDataMonth(commaddr=commaddr,hdate=ymon,dosage=dosage)
            added_list.append(d)

    if len(added_list)>0:
        try:
            added=HdbFlowDataMonth.objects.bulk_create(added_list)
            
        except Exception as e:
            logger_info.info("sync flow month error,reason :",e)


# WaterMeter

def test_pwl(**options):
    if options["d"]:
        day = options["d"][0]
    else:
        today = datetime.datetime.today()
        day = today.strftime("%Y-%m-%d")

    close_old_connections()
    return
    # return test_hdb_watermeter_data_day()
    # return test_hdb_watermeter_data_month()
    # return test_sync_bgm_flows("15755950621")
    # return test_sync_bgm_flow_hour("15755950621")
    # return test_sync_bgm_flow_daily("15755950621")
    # return test_sync_bgm_flow_month("15755950621","2019-01")
    return test_sync_watermeter(day)
    return test_sync_bigmeter()
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

        parser.add_argument(
            '-d',
            action='append',
            dest='d',
            default=None,
            help='update certain day'
        )


    def handle(self, *args, **options):
        # sTime = options['sTime']
        t1=time.time()
        count = 0
        if options['test']:
            
            # test_job()
            print(args)
            print(options["d"])
            # return
            test_pwl(**options)
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
