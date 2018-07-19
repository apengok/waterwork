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
from legacy.models import District,Bigmeter,HdbFlowData,HdbFlowDataDay,HdbFlowDataMonth,HdbPressureData
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

class MnfView2(TemplateView):
    template_name = "analysis/mnf2.html"

    def get_context_data(self, *args, **kwargs):
        context = super(MnfView2, self).get_context_data(*args, **kwargs)
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
    treetype = request.POST.get("treetype")
    startTime = request.POST.get("startTime")
    endTime = request.POST.get("endTime")

    data = []

    if treetype == 'dma':
        # distict = District.objects.get(id=int(stationid))
        # bigmeter = distict.bigmeter.first()
        dmas = DMABaseinfo.objects.filter(pk=int(stationid))
        
        
    else:
        # dma = DMABaseinfo.objects.first()
        # dmastation = dma.dmastation.first()
        # comaddr = dmastation.station_id

        if treetype == '':
            organ = Organizations.objects.first()

        if treetype == 'group':
            organ = Organizations.objects.get(cid=stationid)

        organs = organ.get_descendants(include_self=True)

        dmas = None
        for o in organs:
            if dmas is None:
                dmas = o.dma.all()
            else:
                dmas |= o.dma.all()
    print('dmas:',dmas)

    if len(dmas) == 0:
        ret = {"exceptionDetailMsg":"null",
            "msg":"没有dma分区信息",
            "obj":{
                "online":data, #reverse
                # "today_use":round(float(today_use),2),
                # "yestoday_use":round(float(yestoday_use),2),
                # "last_year_same":round(float(last_year_same),2),
                # "tongbi":round(tongbi,2),
                # "huanbi":round(huanbi,2),
                # "maxflow":round(maxflow,2),
                # "minflow":round(minflow,2),
                # "average":round(average,2),
                # "mnf":round(mnf,2),
                # "mnf_add":round(mnf_add,2),
                # "ref_mnf":round(ref_mnf,2),
                # "back_leak":round(back_leak,2),
                # "alarm_set":round(alarm_set,2),


            },
            "success":0}

    
    
        return HttpResponse(json.dumps(ret))

    # if stationid != '':
    #     # distict = District.objects.get(id=int(stationid))
    #     # bigmeter = distict.bigmeter.first()
    #     dma = DMABaseinfo.objects.get(pk=int(stationid))
    #     print('DMA',dma,dma.dmastation)
    #     dmastation = dma.dmastation.first()
    #     comaddr = dmastation.station_id
    # else:
    #     dma = DMABaseinfo.objects.first()
    #     dmastation = dma.dmastation.first()
    #     comaddr = dmastation.station_id


    dma = dmas.first()
    dmastation = dma.dmastation.first()
    comaddr = dmastation.station_id
    
    
    
    # if comaddr:
        # comaddr = bigmeter.commaddr
    flowday_stastic = HdbFlowDataDay.objects.filter(commaddr=comaddr)
    flowday = HdbFlowData.objects.filter(commaddr=comaddr).filter(readtime__range=[startTime,endTime])

    #pressure
    pressures = HdbPressureData.objects.filter(commaddr=comaddr).filter(readtime__range=[startTime,endTime])
    press = [round(float(f.pressure),2) for f in pressures]
    # print('pressures:',pressures)

    flows = [f.flux for f in flowday]
    hdates = [f.readtime for f in flowday]

    # print('mnf hdates',hdates)
    show_flag=1
    tmp = ''
    count_cnt = 1
    for i in range(len(hdates)):
        if i == 0:
            continue
        h = hdates[i]
        if tmp != h[:10]:
            tmp = h[:10]
            count_cnt += 1
            if count_cnt == 5:
                hdates[i] = h[:10] + " 00:00:00"
            else:
                hdates[i]=''
        


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
            "ref_mnf":ref_mnf,
            "press":press[i] if len(press)>0 else 0
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
class CXCView2(TemplateView):
    template_name = "analysis/dmacxc2.html"

    def get_context_data(self, *args, **kwargs):
        context = super(CXCView2, self).get_context_data(*args, **kwargs)
        context["page_menu"] = "数据监控"
        # context["page_submenu"] = "组织和用户管理"
        context["page_title"] = "DMA产销差综合统计"

        bigmeter = Bigmeter.objects.first()
        context["station"] = bigmeter.username
        context["organ"] = "歙县自来水公司"

        # dmastations = DmaStations.objects.all()
        

        return context                  


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
    print(startTime,'-',endTime)
    # etime = datetime.datetime.strptime(endTime.strip(),"%Y-%m-%d")
    # stime = etime - datetime.timedelta(days=10)
    # startTime = stime.strftime("%Y-%m-%d")
    echart_data = {}
    def month_year_iter( start_month, start_year, end_month, end_year ):
        ym_start= 12*start_year + start_month
        ym_end= 12*end_year + end_month
        for ym in range( ym_start, ym_end ):
            y, m = divmod( ym, 12 )
            # yield y, m+1
            yield '{}-{:02d}'.format(y,m+1)

    month_list = month_year_iter(lastyear.month,lastyear.year,today.month,today.year)
    print(month_list)
    for m in month_list:
        # print (m)
        if m not in echart_data.keys():
            echart_data[m] = 0
    print('echart_data:',echart_data)

    if treetype == 'dma':
        # distict = District.objects.get(id=int(stationid))
        # bigmeter = distict.bigmeter.first()
        dmas = DMABaseinfo.objects.filter(pk=int(stationid))
        
        
    else:
        # dma = DMABaseinfo.objects.first()
        # dmastation = dma.dmastation.first()
        # comaddr = dmastation.station_id

        if treetype == '':
            organ = Organizations.objects.first()

        if treetype == 'group':
            organ = Organizations.objects.get(cid=stationid)

        organs = organ.get_descendants(include_self=True)

        dmas = None
        for o in organs:
            if dmas is None:
                dmas = o.dma.all()
            else:
                dmas |= o.dma.all()
    print('dmas:',dmas)

    

    total_influx       = 0
    total_total        = 0
    total_leak         = 0
    total_uncharg      = 0
    total_sale         = 0
    total_cxc          = 0
    total_cxc_percent  = 0
    total_leak_percent = 0
    total_broken_pipe  = 0
    total_mnf          = 0
    total_back_leak    = 0
    huanbi=0
    tongbi=0
    mnf=1.2
    back_leak=1.8
    broken_pipe=0
    other_leak = 0

    if len(dmas) == 0:
        ret = {"exceptionDetailMsg":"null",
            "msg":"没有dma分区信息",
            "obj":{
                "online":data, #reverse
                "influx":round(total_influx,2),
                "total":round(total_total,2),
                "leak":round(total_leak,2),
                "uncharg":round(total_uncharg,2),
                "sale":round(total_sale,2),
                "cxc":round(total_cxc,2),
                "cxc_percent":round(total_cxc_percent,2),
                "broken_pipe":broken_pipe,
                "back_leak":back_leak,
                "mnf":mnf,
                "leak_percent":round(total_leak_percent,2),
                "stationsstastic":sub_dma_list

            },
            "success":0}

    
    
        return HttpResponse(json.dumps(ret))
    
    for dma in dmas:
        dmastation = dma.dmastation.first()
        comaddr = dmastation.station_id

        if comaddr == '':
            comaddr = '4892354820'
        
        
        
        # if comaddr:
            # comaddr = bigmeter.commaddr
        flowday = HdbFlowDataMonth.objects.filter(commaddr=comaddr).filter(hdate__range=[startTime,endTime])
        
        #fill echart data
        for de,value in flowday.values_list('hdate','dosage'):
            if de in echart_data.keys():
                o_data = echart_data[de]
                echart_data[de] = o_data + float(value)
        
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
        flows_leak = [random.uniform(float(f)/10,float(f)/5 ) for f in flows]
        uncharged =[random.uniform(float(f)/10,float(f)/5 ) for f in flows]

        #表具信息
        
        total = sum(flows_float)
        influx = sum(flows_float)
        leak = sum(flows_leak)
        uncharg = sum(uncharged)
        sale = total - leak - uncharg
        cxc = total - sale
        cxc_percent = (cxc / total)*100
        huanbi=0
        leak_percent = (leak * 100)/total
        tongbi=0
        mnf=1.2
        back_leak=1.8
        broken_pipe=0
        other_leak = 0

        total_influx += influx
        total_total += total
        total_leak += leak
        total_uncharg += uncharg
        total_sale += sale
        total_cxc += cxc
        total_cxc_percent += cxc_percent
        total_leak_percent += leak_percent

        #记录每个dma分区的统计信息
        sub_dma_list.append({
                    "organ":dma.dma_name,
                    # "influx":round(influx,2),
                    "total":round(total,2),
                    "sale":round(sale,2),
                    "uncharg":round(uncharg,2),
                    "leak":round(leak,2),
                    "cxc":round(cxc,2),
                    "cxc_percent":round(cxc_percent,2),
                    "huanbi":round(huanbi,2),
                    "leak_percent":round(leak_percent,2),
                    "tongbi":round(tongbi,2),
                    "mnf":round(mnf,2),
                    "back_leak":round(back_leak,2),
                    "other_leak":round(other_leak,2),
                    "statis_date":endTime,
                })
        

        
    dma_name = 'shex'
    for k in echart_data:
        v = echart_data[k]
        l = v/5
        u = v/4
        data.append({
            "hdate":k[-2:],
            "dosage":round(v-l-u,2),
            "assignmentName":dma_name,
            "color":"红色",
            "ratio":"null",
            "leak":round(l,2),
            "uncharged":round(u,2)
            })    
    

    
    if total_total != 0:
        total_cxc = total_total - total_sale
        total_cxc_percent = (total_cxc / total_total)*100
        total_leak_percent = (total_leak * 100)/total_total

    ret = {"exceptionDetailMsg":"null",
            "msg":"null",
            "obj":{
                "online":data, #reverse
                "influx":round(total_influx,2),
                "total":round(total_total,2),
                "leak":round(total_leak,2),
                "uncharg":round(total_uncharg,2),
                "sale":round(total_sale,2),
                "cxc":round(total_cxc,2),
                "cxc_percent":round(total_cxc_percent,2),
                "broken_pipe":broken_pipe,
                "back_leak":back_leak,
                "mnf":mnf,
                "leak_percent":round(total_leak_percent,2),
                "stationsstastic":sub_dma_list

            },
            "success":1}

    
    
    return HttpResponse(json.dumps(ret))


