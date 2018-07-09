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
from dmam.models import District,Bigmeter,HdbFlowDataDay

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

def flowdata_mnf(request):

    print("flowdata_mnf:",request.POST)

    stationid = request.POST.get("station") # districtid
    if stationid != '':
        distict = District.objects.get(id=int(stationid))
        print('District',distict,distict.bigmeter)
        bigmeter = distict.bigmeter.first()
    else:
        bigmeter = Bigmeter.objects.first()
    print('bigmeter',bigmeter)

    qmonth = request.POST.get("qmonth")
    
    if qmonth == '-2':
        qdays = 60
    elif qmonth == '-3':
        qdays = 90
    else:
        qdays = 30

    
    today = datetime.date.today()
    
    data = []
    if bigmeter:
        comaddr = bigmeter.commaddr
        flowday = HdbFlowDataDay.objects.filter(commaddr=comaddr)

        #pressure
        # pressures = HdbPressureData.objects.filter(commaddr=comaddr)

        flows = []
        hdates = []


        for i in range(qdays):
            qday = today - datetime.timedelta(days=i)
            daystr = qday.strftime("%Y-%m-%d")
            q_by_day = flowday.filter(hdate=daystr)
            if q_by_day.exists():
                f = q_by_day.first()
                flows.append(f.dosage)
            else:
                flows.append(0)
            hdates.append(qday.strftime("%m-%d"))

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
            

    #staticstic data

    ret = {"exceptionDetailMsg":"null",
            "msg":"null",
            "obj":{
                "online":data[::-1] #reverse
            },
            "success":1}

    # data=[
    #             {"activeDays":0,"allDays":3,"assignmentName":"维修机组","carLicense":"粤BV24M6","color":"红色","professionalNames":"","ratio":"null","vehicleId":"34981bff"},
    #             {"activeDays":3,"allDays":3,"assignmentName":"维修机组","carLicense":"粤BV11M6","color":"黑色","professionalNames":"","ratio":"null","vehicleId":"34981bff"},
    #             {"activeDays":2,"allDays":3,"assignmentName":"维修机组","carLicense":"粤BV25M7","color":"黑色","professionalNames":"","ratio":"null","vehicleId":"34981bff"},
    #             {"activeDays":1,"allDays":3,"assignmentName":"维修机组","carLicense":"粤BV21M6","color":"蓝色","professionalNames":"","ratio":"null","vehicleId":"34981bff"},
    #             {"activeDays":9,"allDays":3,"assignmentName":"维修机组","carLicense":"粤BV21M6","color":"黑色","professionalNames":"","ratio":"null","vehicleId":"34981bff"},
    #             {"activeDays":10,"allDays":3,"assignmentName":"维修机组","carLicense":"粤BV21M6","color":"绿色","professionalNames":"","ratio":"null","vehicleId":"34981bff"},
    #             {"activeDays":4,"allDays":3,"assignmentName":"维修机组","carLicense":"粤BV21M6","color":"黑色","professionalNames":"","ratio":"null","vehicleId":"34981bff"},
    #             {"activeDays":5,"allDays":3,"assignmentName":"维修机组","carLicense":"粤BV21M6","color":"黑色","professionalNames":"","ratio":"null","vehicleId":"34981bff"},
    #             {"activeDays":0,"allDays":3,"assignmentName":"维修机组","carLicense":"粤BV21M6","color":"黑色","professionalNames":"","ratio":"null","vehicleId":"34981bff"},
    #             {"activeDays":7,"allDays":3,"assignmentName":"维修机组","carLicense":"粤BV21M6","color":"黑色","professionalNames":"","ratio":"null","vehicleId":"34981bff"},
    #             {"activeDays":6,"allDays":3,"assignmentName":"维修机组","carLicense":"粤BV21M6","color":"黑色","professionalNames":"","ratio":"null","vehicleId":"34981bff"},
    #             ]



    
    return HttpResponse(json.dumps(ret))