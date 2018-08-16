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
from dmam.models import DMABaseinfo,DmaStations,Station
from entm.models import Organizations
from .forms import logoPagesPhotoForm

from django.core.files.storage import FileSystemStorage
# from django.core.urlresolvers import reverse_lazy


        
class personalizedView(TemplateView):
    template_name = "sysm/personalizedList.html"

    def get_context_data(self, *args, **kwargs):
        context = super(personalizedView, self).get_context_data(*args, **kwargs)
        context["page_menu"] = "系统管理"
        # context["page_submenu"] = "组织和用户管理"
        context["page_title"] = "个性化设置"

        return context      


def logoPagesPhotoUpdate(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'core/model_form_upload.html', {
        'form': form
    })        


def personalizedUpdate(request):
    print("update:",request.POST)

    ret = {"exceptionDetailMsg":"null",
            "msg":"null",
            "obj":"null",
            "success":1}
    return HttpResponse(json.dumps(ret))

def personalizedUpdate_img(request):

    print("update_img:",request.FILES)
    # form = logoPagesPhotoForm(request.POST,request.FILES)
    # print (form)
    imgName = ''
    if request.method == 'POST' and request.FILES['file']:
        myfile = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        imgName = filename
        print(filename,uploaded_file_url)

    ret = {"exceptionDetailMsg":"null",
            "msg":"null",
            "obj":"null",
            "imgName":imgName,
            "success":1}
    return HttpResponse(json.dumps(ret))

def personalizedFind(request):

    ret = {"exceptionDetailMsg":"null",
            "msg":"null",
            "obj":{
                "list":{
                    "copyright":"?2015-2017威尔沃自动化设备（深圳）有限公司",
                    "createDataTime":"2017-10-22 10:51:16",
                    "createDataUsername":"13911755733",
                    "editable":1,
                    "enabled":1,
                    "flag":1,
                    "frontPage":"",
                    "frontPageUrl":"null",
                    "groupId":"338c7dc2-384a-1037-8466-cb3a0ec2dddf",
                    "homeLogo":"indexLogo.png",
                    "id":"afa33228-1f5d-4f6d-8183-888bf6ff01f9",
                    "loginLogo":"loginLogo.png",
                    "priority":1,
                    "recordNumber":"京ICP备15041746号-1",
                    "sortOrder":1,
                    "topTitle":"智慧水务管控一体化",
                    "updateDataTime":"2018-08-15 15:47:57",
                    "updateDataUsername":"13911755733",
                    "webIco":"favicon.ico",
                    "websiteName":"www.virvo.com.cn"
                    }
                },
            "success":1}
    return HttpResponse(json.dumps(ret))

def personalizedDefault(request):

    ret = {"exceptionDetailMsg":"null",
            "msg":"null",
            "obj":"null",
            "success":1}
    return HttpResponse(json.dumps(ret))
