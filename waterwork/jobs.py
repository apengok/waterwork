# -*- coding: utf-8 -*-
import random
import time

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
        last_readtime = zncb_last.readtime
        # 取歙县服务器该条数据记录对比
        sx_last = HdbFlowData.objects.using("shexian").filter(commaddr=commaddr).filter(readtime=last_readtime).first()
        # 取出上次最后一条数据记录之后增加的记录
        added = HdbFlowData.objects.using("shexian").filter(commaddr=commaddr).filter(id__gt=sx_last.id).all()
        
        for d in added:
            d.save(using='zncb')
    # raise ValueError("Olala!")


register_events(scheduler)

scheduler.start()
print("Scheduler started!")