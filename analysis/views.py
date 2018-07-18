# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404,render,redirect
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.contrib import messages

import json
import random
import datetime

from django.template.loader import render_to_string
from django.shortcuts import render,HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView,DeleteView,FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import admin
from django.contrib.auth.models import Permission
from django.utils.safestring import mark_safe
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.models import User,MyRoles
from legacy.models import District,Bigmeter,HdbFlowData,HdbFlowDataDay,HdbFlowDataMonth
from dmam.models import DMABaseinfo,DmaStations
from entm.models import Organizations

# from django.core.urlresolvers import reverse_lazy


        
class MnfView(TemplateView):
    template_name = "analysis/mnf.html"

    def get_context_data(self, *args, **kwargs):
        context = super(MnfView, self).get_context_data(*args, **kwargs)
        context["page_menu"] = "数据监控"
        # context["page_submenu"] = "组织和用户管理"
        context["page_title"] = "最小夜间流量分析（MNF）"

        bigmeter = Bigmeter.objects.first()
        dma = DMABaseinfo.objects.first()
        context["station"] = dma.dma_name
        context["organ"] = dma.belongto
        

        return context                  


def flowdata_mnf(request):

    print("flowdata_mnf:",request.POST)

    stationid = request.POST.get("station") # DMABaseinfo pk
    startTime = request.POST.get("startTime")
    endTime = request.POST.get("endTime")

    if stationid != '':
        # distict = District.objects.get(id=int(stationid))
        # bigmeter = distict.bigmeter.first()
        dma = DMABaseinfo.objects.get(pk=int(stationid))
        print('DMA',dma,dma.dmastation)
        dmastation = dma.dmastation.first()
        comaddr = dmastation.station_id
    else:
        dma = DMABaseinfo.objects.first()
        dmastation = dma.dmastation.first()
        comaddr = dmastation.station_id
    # print('bigmeter',bigmeter)

    # qmonth = request.POST.get("qmonth")
    
    # if qmonth == '-2':
    #     qdays = 60
    # elif qmonth == '-3':
    #     qdays = 90
    # else:
    #     qdays = 7

    if comaddr == '':
        comaddr = '4892354820'
    
    
    data = []
    # if comaddr:
        # comaddr = bigmeter.commaddr
    flowday_stastic = HdbFlowDataDay.objects.filter(commaddr=comaddr)
    flowday = HdbFlowData.objects.filter(commaddr=comaddr).filter(readtime__range=[startTime,endTime])

    #pressure
    # pressures = HdbPressureData.objects.filter(commaddr=comaddr)

    flows = [f.flux for f in flowday]
    hdates = [f.readtime for f in flowday]



    flows_float = [round(float(f),2) for f in flows]
    flows_float = flows_float[::-1]
    

    #参考MNF
    ref_mnf = 4.46
    #MNF
    mnf = 8.63
    #表具信息
    
    #MNF/ADD
    mnf_add = 51
    #背景漏损
    back_leak = 4.46
    
    #设定报警
    alarm_set = 12

    #staticstic data
    #当天用水量
    today_use = 0
    #昨日用水量
    yestoday_use = 0
    #去年同期用水量
    last_year_same = 0
    #同比增长
    tongbi = 0
    #环比增长
    huanbi = 0
    #最大值
    maxflow = 0
    #最小值
    minflow = 0
    #平均值
    average = 0

    maxflow = max(flows_float)
    minflow = min(flows_float)
    average = sum(flows_float)/len(flows)
    mnf = minflow
    ref_mnf = mnf/2
    back_leak = ref_mnf * 0.8

    for i in range(len(flows_float)):
        data.append({
            "hdate":hdates[i],
            "dosage":flows_float[i],
            "assignmentName":dma.dma_name,
            "color":"红色",
            "ratio":"null",
            "maxflow":maxflow,
            "average":average,
            "mnf":mnf,
            "ref_mnf":ref_mnf
            })
            
    

    today = datetime.date.today()
    today_str = today.strftime("%Y-%m-%d")
    today_flow = HdbFlowDataDay.objects.filter(hdate=today_str)
    
    if today_flow.exists():
        today_use = today_flow.first().dosage

    yestoday = today - datetime.timedelta(days=1)
    yestoday_str = yestoday.strftime("%Y-%m-%d")
    yestoday_flow = HdbFlowDataDay.objects.filter(hdate=yestoday_str)
    if yestoday_flow.exists():
        yestoday_use = yestoday_flow.first().dosage

    lastyear = datetime.datetime(year=today.year-1,month=today.month,day=today.day)
    lastyear_str = lastyear.strftime("%Y-%m-%d")
    lastyear_flow = HdbFlowDataDay.objects.filter(hdate=lastyear_str)
    if lastyear_flow.exists():
        last_year_same = lastyear_flow.first().dosage
    tongbi = float(today_use) - float(last_year_same)
    huanbi = float(today_use) - float(yestoday_use)
    



    ret = {"exceptionDetailMsg":"null",
            "msg":"null",
            "obj":{
                "online":data, #reverse
                "today_use":round(float(today_use),2),
                "yestoday_use":round(float(yestoday_use),2),
                "last_year_same":round(float(last_year_same),2),
                "tongbi":round(tongbi,2),
                "huanbi":round(huanbi,2),
                "maxflow":round(maxflow,2),
                "minflow":round(minflow,2),
                "average":round(average,2),
                "mnf":round(mnf,2),
                "mnf_add":round(mnf_add,2),
                "ref_mnf":round(ref_mnf,2),
                "back_leak":round(back_leak,2),
                "alarm_set":round(alarm_set,2),


            },
            "success":1}

    
    
    return HttpResponse(json.dumps(ret))
        # LoginRequiredMixin,
class CXCView(TemplateView):
    template_name = "analysis/dmacxc.html"

    def get_context_data(self, *args, **kwargs):
        context = super(CXCView, self).get_context_data(*args, **kwargs)
        context["page_menu"] = "数据监控"
        # context["page_submenu"] = "组织和用户管理"
        context["page_title"] = "DMA产销差综合统计"

        bigmeter = Bigmeter.objects.first()
        context["station"] = bigmeter.username
        context["organ"] = "歙县自来水公司"

        # dmastations = DmaStations.objects.all()
        

        return context                  


def flowdata_cxc(request):

    print("flowdata_cxc:",request.POST)

    stationid = request.POST.get("station") # DMABaseinfo pk
    endTime = request.POST.get("endTime")
    treetype = request.POST.get("treetype")

    today = datetime.date.today()
    endTime = today.strftime("%Y-%m")
    
    lastyear = datetime.datetime(year=today.year-1,month=today.month,day=today.day)
    startTime = lastyear.strftime("%Y-%m")

    data = []
    sub_dma_list = []
    # etime = datetime.datetime.strptime(endTime.strip(),"%Y-%m-%d")
    # stime = etime - datetime.timedelta(days=10)
    # startTime = stime.strftime("%Y-%m-%d")

    if treetype == 'dma':
        # distict = District.objects.get(id=int(stationid))
        # bigmeter = distict.bigmeter.first()
        dmas = DMABaseinfo.objects.filter(pk=int(stationid))
        print('DMA',dma,dma.dmastation)
        
    else:
        # dma = DMABaseinfo.objects.first()
        # dmastation = dma.dmastation.first()
        # comaddr = dmastation.station_id

        if treetype == '':
            organ = Organizations.objects.first()

        if treetype == 'group':
            organ = Organizations.objects.get(cid=stationid)

        organs = organ.get_descendants(include_self=True)

        for o in organs:
            dmas = o.dma.all()

    
    
    for dma in dmas:
        dmastation = dma.dmastation.first()
        comaddr = dmastation.station_id

        if comaddr == '':
            comaddr = '4892354820'
        
        
        
        # if comaddr:
            # comaddr = bigmeter.commaddr
        flowday = HdbFlowDataMonth.objects.filter(commaddr=comaddr).filter(hdate__range=[startTime,endTime])
        
        # flowday = HdbFlowData.objects.filter(commaddr=comaddr).filter(readtime__range=[startTime,endTime])

        #pressure
        # pressures = HdbPressureData.objects.filter(commaddr=comaddr)

        # flows = [f.flux for f in flowday]
        # hdates = [f.readtime for f in flowday]

        flows = [f.dosage for f in flowday]
        hdates = [f.hdate[-2:] for f in flowday]
        hdates = hdates[::-1]

        flows_float = [float(f) for f in flows]
        flows_float = flows_float[::-1]
        flows_leak = [random.uniform(float(f)/20,float(f)/10 ) for f in flows]
        uncharged =[random.uniform(float(f)/20,float(f)/10 ) for f in flows]

        #表具信息
        influx = sum(flows_float)/1.8
        total = sum(flows_float)
        leak = sum(flows_leak)
        uncharg = sum(uncharged)
        sale = total - leak - uncharg
        cxc = cxc_percent = sale / total
        leak_percent = (leak * 100)/total
        broken_pipe=0
        mnf=1.2
        back_leak=1.8
        

        for i in range(len(flows_float)):
            data.append({
                "hdate":hdates[i],
                "dosage":flows_float[i],
                "assignmentName":dma.dma_name,
                "color":"红色",
                "ratio":"null",
                "leak":flows_leak[i],
                "uncharged":uncharged[i]
                })
            
    

    print('leak_percent:',leak_percent)



    ret = {"exceptionDetailMsg":"null",
            "msg":"null",
            "obj":{
                "online":data, #reverse
                "influx":round(influx,2),
                "total":round(total,2),
                "leak":round(leak,2),
                "uncharg":round(uncharg,2),
                "sale":round(sale,2),
                "cxc":round(cxc,2),
                "cxc_percent":round(cxc_percent,2),
                "broken_pipe":broken_pipe,
                "back_leak":back_leak,
                "mnf":mnf,
                "leak_percent":round(leak_percent,2)

            },
            "success":1}

    
    
    return HttpResponse(json.dumps(ret))



def dmastations(request):
    print('dmastations:',request,request.POST)
    stationid = request.POST.get("station") # DMABaseinfo pk
    startTime = request.POST.get("startTime")
    endTime = request.POST.get("endTime")

    treetype = request.POST.get("treetype")


    data = []

    if treetype == 'dma':
        # distict = District.objects.get(id=int(stationid))
        # bigmeter = distict.bigmeter.first()
        dma = DMABaseinfo.objects.get(pk=int(stationid))
        print('DMA',dma,dma.dmastation)
        dmastation = dma.dmastation.first()
        comaddr = dmastation.station_id
        data.append({
                    "organ":dma.dma_name,
                    # "influx":round(influx,2),
                    "total":12345,
                    "sale":9866,
                    "uncharg":123,
                    "leak":32,
                    "cxc":12,
                    "cxc_percent":11,
                    "huanbi":12,
                    "leak_percent":3,
                    "tongbi":32,
                    "mnf":4.5,
                    "back_leak":1.2,
                    "other_leak":0,
                    "statis_date":'2018-07-17',
                })
    else:
        if treetype == '':
            organ = Organizations.objects.first()

        if treetype == 'group':
            organ = Organizations.objects.get(cid=stationid)

        organs = organ.get_descendants(include_self=True)
        # print('organs:',organs)

        

        for o in organs:
            print(o)
            dmas = o.dma.all()
            if dmas.exists():
                for d in dmas:
                    data.append({
                    "organ":d.dma_name,
                    # "influx":round(influx,2),
                    "total":12345,
                    "sale":9866,
                    "uncharg":123,
                    "leak":32,
                    "cxc":12,
                    "cxc_percent":11,
                    "huanbi":12,
                    "leak_percent":3,
                    "tongbi":32,
                    "mnf":4.5,
                    "back_leak":1.2,
                    "other_leak":0,
                    "statis_date":'2018-07-17',
                })

    
    # for i in range(1):
    #     data.append({
    #         "organ":'test',
    #         # "influx":round(influx,2),
    #         "total":12345,
    #         "sale":9866,
    #         "uncharg":123,
    #         "leak":32,
    #         "cxc":12,
    #         "cxc_percent":11,
    #         "huanbi":12,
    #         "leak_percent":3,
    #         "tongbi":32,
    #         "mnf":4.5,
    #         "back_leak":1.2,
    #         "other_leak":0,
    #         "statis_date":'2018-07-17',
    #     })

    ret = {"exceptionDetailMsg":"null",
            "msg":"null",
            "obj":data,
            "success":1}

    
    
    return HttpResponse(json.dumps(ret))