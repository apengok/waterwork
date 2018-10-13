# -*- coding: utf-8 -*-
import random
import time
import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

from legacy.models import HdbFlowData,HdbFlowDataDay,HdbFlowDataHour,HdbFlowDataMonth,HdbPressureData,Bigmeter

import logging

logger_info = logging.getLogger('info_logger')


scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


# 大表数据 从歙县服务器数据库同步到威尔沃服务器数据库
@register_job(scheduler, "interval", seconds=300, replace_existing=True)
def test_job():
    time.sleep(random.randrange(1, 100, 1)/100.)
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


register_events(scheduler)

scheduler.start()
print("Scheduler started!")