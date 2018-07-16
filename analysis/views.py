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
from legacy.models import District,Bigmeter,HdbFlowData,HdbFlowDataDay

# from django.core.urlresolvers import reverse_lazy


        
class MnfView(LoginRequiredMixin,TemplateView):
    template_name = "analysis/mnf.html"

    def get_context_data(self, *args, **kwargs):
        context = super(MnfView, self).get_context_data(*args, **kwargs)
        context["page_menu"] = "数据监控"
        # context["page_submenu"] = "组织和用户管理"
        context["page_title"] = "最小夜间流量分析（MNF）"

        bigmeter = Bigmeter.objects.first()
        context["station"] = bigmeter.username
        context["organ"] = "威尔沃"
        

        return context                  


        
class CXCView(LoginRequiredMixin,TemplateView):
    template_name = "analysis/dmacxc.html"

    def get_context_data(self, *args, **kwargs):
        context = super(CXCView, self).get_context_data(*args, **kwargs)
        context["page_menu"] = "数据监控"
        # context["page_submenu"] = "组织和用户管理"
        context["page_title"] = "DMA产销差综合统计"

        bigmeter = Bigmeter.objects.first()
        context["station"] = bigmeter.username
        context["organ"] = "威尔沃"
        

        return context                  


def flowdata_mnf(request):

    print("flowdata_mnf:",request.POST)

    stationid = request.POST.get("station") # districtid
    startTime = request.POST.get("startTime")
    endTime = request.POST.get("endTime")

    if stationid != '':
        distict = District.objects.get(id=int(stationid))
        print('District',distict,distict.bigmeter)
        bigmeter = distict.bigmeter.first()
    else:
        bigmeter = Bigmeter.objects.first()
    print('bigmeter',bigmeter)

    # qmonth = request.POST.get("qmonth")
    
    # if qmonth == '-2':
    #     qdays = 60
    # elif qmonth == '-3':
    #     qdays = 90
    # else:
    #     qdays = 7

    
    
    
    data = []
    if bigmeter:
        comaddr = bigmeter.commaddr
        flowday_stastic = HdbFlowDataDay.objects.filter(commaddr=comaddr)
        flowday = HdbFlowData.objects.filter(commaddr=comaddr).filter(readtime__range=[startTime,endTime])

        #pressure
        # pressures = HdbPressureData.objects.filter(commaddr=comaddr)

        flows = [f.flux for f in flowday]
        hdates = [f.readtime for f in flowday]


 
        flows_float = [float(f) for f in flows]
        maxflow = max(flows_float)
        average = sum(flows_float)/len(flows)

        for i in range(len(flows)):
            data.append({
                "hdate":hdates[i],
                "dosage":flows[i],
                "assignmentName":bigmeter.username,
                "color":"红色",
                "ratio":"null",
                "maxflow":maxflow,
                "average":average
                })
            
    #表具信息
    #MNF
    mnf = 0
    #MNF/ADD
    mnf_add = 0
    #背景漏损
    back_leak = 0
    #参考MNF
    ref_mnf = 0
    #设定报警
    alarm_set = 0

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
    maxflow = max(flows_float)
    minflow = min(flows_float)
    average = sum(flows_float)/len(flows)



    ret = {"exceptionDetailMsg":"null",
            "msg":"null",
            "obj":{
                "online":data[::-1], #reverse
                "today_use":today_use,
                "yestoday_use":yestoday_use,
                "last_year_same":last_year_same,
                "tongbi":tongbi,
                "huanbi":huanbi,
                "maxflow":maxflow,
                "minflow":minflow,
                "average":average,
                "mnf":mnf,
                "mnf_add":mnf_add,
                "ref_mnf":ref_mnf,
                "back_leak":back_leak,
                "alarm_set":alarm_set,


            },
            "success":1}

    
    
    return HttpResponse(json.dumps(ret))