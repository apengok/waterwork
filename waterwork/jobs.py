# -*- coding: utf-8 -*-
import random
import time
import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

from legacy.models import HdbFlowData,HdbFlowDataDay,HdbFlowDataHour,HdbFlowDataMonth,HdbPressureData,Bigmeter

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


# 大表数据 从歙县服务器数据库同步到威尔沃服务器数据库
@register_job(scheduler, "interval", seconds=3600, replace_existing=True)
def test_job():
    time.sleep(random.randrange(1, 100, 1)/100.)
    print("I'm a test job!")
    bigmeters_qset = Bigmeter.objects.using("shexian").all()
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
                # print('last_readtime',last_readtime,zncb_last)
                # print('sx_last',sx_last)
                added = HdbFlowData.objects.using("shexian").filter(commaddr=commaddr).filter(readtime__gt=datetime.datetime.strptime(last_readtime.strip(),"%Y-%m-%d %H:%M:%S")).all()
                if added.exists():
                    print(added.count(),b.username,b.commaddr)
                    for d in added:
                        d.save(using='zncb')
    # raise ValueError("Olala!")


register_events(scheduler)

scheduler.start()
print("Scheduler started!")