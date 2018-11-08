# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404,render,redirect
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect,StreamingHttpResponse
from django.contrib import messages
from django.template import TemplateDoesNotExist
import json
import random
import datetime
import time

from mptt.utils import get_cached_trees
from mptt.templatetags.mptt_tags import cache_tree_children
from django.contrib.auth.mixins import PermissionRequiredMixin,UserPassesTestMixin
from django.template.loader import render_to_string
from django.shortcuts import render,HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView,DeleteView,FormView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import admin
from django.contrib.auth.models import Permission
from django.utils.safestring import mark_safe
from django.utils.encoding import escape_uri_path
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from collections import OrderedDict
from accounts.models import User,MyRoles
from accounts.forms import RoleCreateForm,MyRolesForm,RegisterForm,UserDetailChangeForm

from entm.utils import unique_cid_generator,unique_uuid_generator,unique_rid_generator
from entm.forms import OrganizationsAddForm,OrganizationsEditForm
from entm.models import Organizations
from legacy.models import Bigmeter,District,Community,HdbFlowData,HdbFlowDataDay,HdbFlowDataMonth,HdbPressureData
from dmam.models import WaterUserType,DMABaseinfo,DmaStation,Station,Meter,VCommunity,VConcentrator,DmaGisinfo
import os
from django.conf import settings

from waterwork.mixins import AjaxableResponseMixin

from .models import FenceDistrict,Polygon

# Create your views here.

class PipelineQueryView(LoginRequiredMixin,TemplateView):
    template_name = "gis/pipelinequery.html"

    def get_context_data(self, *args, **kwargs):
        context = super(PipelineQueryView, self).get_context_data(*args, **kwargs)
        context["page_title"] = "管网查询"
        context["page_menu"] = "GIS系统"
        
        return context  


class PipelineStasticView(LoginRequiredMixin,TemplateView):
    template_name = "gis/pipelinestastic.html"

    def get_context_data(self, *args, **kwargs):
        context = super(PipelineStasticView, self).get_context_data(*args, **kwargs)
        context["page_title"] = "管网统计"
        context["page_menu"] = "GIS系统"
        
        return context  


class PipelineAnalysView(LoginRequiredMixin,TemplateView):
    template_name = "gis/pipelineanalys.html"

    def get_context_data(self, *args, **kwargs):
        context = super(PipelineAnalysView, self).get_context_data(*args, **kwargs)
        context["page_title"] = "管网分析"
        context["page_menu"] = "GIS系统"
        
        return context  


class PipelineImexportView(LoginRequiredMixin,TemplateView):
    template_name = "gis/pipelineimexport.html"

    def get_context_data(self, *args, **kwargs):
        context = super(PipelineImexportView, self).get_context_data(*args, **kwargs)
        context["page_title"] = "导入导出"
        context["page_menu"] = "GIS系统"
        
        return context  

def fenceTree(request):

    fences = FenceDistrict.objects.values()

    fentree = []
    for fs in fences:
        fentree.append({
            "name":fs["name"],
            "pId":fs["pId"],
            "id":fs["cid"],
            "type":fs["ftype"],
            "open":"true"
            })

    # fentree = [{"name":"标注","pId":"","id":"zw_m_marker","type":"fenceParent","open":"true"},
    #             {"name":"路线","pId":"","id":"zw_m_line","type":"fenceParent","open":"true"},
    #             {"name":"矩形","pId":"","id":"zw_m_rectangle","type":"fenceParent","open":"true"},
    #             {"name":"圆形","pId":"","id":"zw_m_circle","type":"fenceParent","open":"true"},
    #             {"name":"多边形","pId":"0","id":"zw_m_polygon","type":"fenceParent","open":"true"},
    #             {"name":"行政区划","pId":"0","id":"zw_m_administration","type":"fenceParent","open":"true"},
    #             {"name":"导航路线","pId":"0","id":"zw_m_travel_line","type":"fenceParent","open":"true"},
    #             {"fenceInfoId":"e4b27c3a-a0f8-4529-9ad2-3b8da18a83ea","iconSkin":"zw_m_rectangle_skin","name":"554454","pId":"zw_m_rectangle","id":"6f355158-dae4-47de-a545-ffb8b0310e5a","type":"fence","open":"true"},
    #             {"fenceInfoId":"392e9263-9d04-4c39-972c-4638161eccfb","iconSkin":"zw_m_rectangle_skin","name":"tes","pId":"zw_m_rectangle","id":"32d9703b-4049-4114-a284-4c6b7bca69ee","type":"fence","open":"true"},
    #             {"fenceInfoId":"fd86ef00-0389-4eaf-8dfc-2e90e258814a","iconSkin":"zw_m_rectangle_skin","name":"5454","pId":"zw_m_rectangle","id":"3e84af67-b09d-41ab-ab9d-a6a1c212241f","type":"fence","open":"true"},
    #             {"fenceInfoId":"de78e9f8-5d56-4e8c-9565-eca05e1100b8","iconSkin":"zw_m_rectangle_skin","name":"8315","pId":"zw_m_rectangle","id":"79bdeb76-b076-4fd4-9f47-638b927564fb","type":"fence","open":"true"},
    #             {"fenceInfoId":"30ac3eea-41d9-482b-a459-74c4afdeb7cd","iconSkin":"zw_m_rectangle_skin","name":"5015","pId":"zw_m_rectangle","id":"74a0ac33-1a3d-4c30-b1b0-94f339134459","type":"fence","open":"true"},
    #             {"fenceInfoId":"1ca32858-2c67-4804-a983-5cc140608a26","iconSkin":"zw_m_rectangle_skin","name":"8363","pId":"zw_m_rectangle","id":"3c397610-82f1-4ae9-b427-af5f373aa796","type":"fence","open":"true"},
    #             {"fenceInfoId":"862509d3-ff9c-4ac4-8859-b2e896397da8","iconSkin":"zw_m_circle_skin","name":"区域二","pId":"zw_m_circle","id":"a3074a92-c95a-45c9-917f-3ab8faef2c6b","type":"fence","open":"true"},
    #             {"fenceInfoId":"5cf3dcc5-76c2-4225-838e-7fc8ef10409f","iconSkin":"zw_m_circle_skin","name":"区域一","pId":"zw_m_circle","id":"d585d745-3556-4f46-9e5d-603efcc65bb8","type":"fence","open":"true"},
    #             {"fenceInfoId":"3997cb87-1508-44b4-8997-5fa376ccccb5","iconSkin":"zw_m_administration_skin","name":"黄山市","pId":"zw_m_administration","id":"85f33f82-5f19-41ce-b295-eadafc55326e","type":"fence","open":"true"},
    #             {"fenceInfoId":"de560d08-8630-4525-ada1-fdcd75cc6f5b","iconSkin":"zw_m_administration_skin","name":"安徽省","pId":"zw_m_administration","id":"d27bbdb0-e52b-4bc3-9fb8-718f5337464d","type":"fence","open":"true"},
    #             {"fenceInfoId":"5868c978-c622-4bd9-bafd-a6d7d1136b6f","iconSkin":"zw_m_administration_skin","name":"彭阳县","pId":"zw_m_administration","id":"4f64dcee-f2f9-4b61-915f-48feebf6152c","type":"fence","open":"true"},
    #             {"fenceInfoId":"1760fabc-5b19-4ce7-bfc3-beabbf8bf77d","iconSkin":"zw_m_administration_skin","name":"歙县","pId":"zw_m_administration","id":"ce7ce77c-fb52-49a8-8213-74ce9125629e","type":"fence","open":"true"}]

    return HttpResponse(json.dumps(fentree))


def fencelist(request):
    # print("userlist",request.POST)
    draw = 1
    length = 0
    start=0
    
    if request.method == "GET":
        draw = int(request.GET.get("draw", 1))
        length = int(request.GET.get("length", 10))
        start = int(request.GET.get("start", 0))
        search_value = request.GET.get("search[value]", None)
        # order_column = request.GET.get("order[0][column]", None)[0]
        # order = request.GET.get("order[0][dir]", None)[0]
        groupName = request.GET.get("groupName")
        simpleQueryParam = request.POST.get("simpleQueryParam")
        # print("simpleQueryParam",simpleQueryParam)

    if request.method == "POST":
        draw = int(request.POST.get("draw", 1))
        length = int(request.POST.get("length", 10))
        start = int(request.POST.get("start", 0))
        pageSize = int(request.POST.get("pageSize", 10))
        search_value = request.POST.get("search[value]", None)
        # order_column = request.POST.get("order[0][column]", None)[0]
        # order = request.POST.get("order[0][dir]", None)[0]
        groupName = request.POST.get("groupName")
        districtId = request.POST.get("districtId")
        simpleQueryParam = request.POST.get("simpleQueryParam")
        # print(request.POST.get("draw"))
        print("groupName",groupName)
        print("districtId:",districtId)
        # print("post simpleQueryParam",simpleQueryParam)

    

    
    data = []
    
    
    
    
    recordsTotal = len(data)
    # recordsTotal = len(data)
    
    result = dict()
    result["records"] = data
    result["draw"] = draw
    result["success"] = "true"
    result["pageSize"] = pageSize
    result["totalPages"] = recordsTotal/pageSize
    result["recordsTotal"] = recordsTotal
    result["recordsFiltered"] = recordsTotal
    result["start"] = 0
    result["end"] = 0

    # {"draw":1,"end":0,"page":0,"pageSize":0,"records":[],"recordsFiltered":0,"recordsTotal":0,"start":0,"success":true,"totalPages":0,"totalRecords":0}
    
    return HttpResponse(json.dumps(result))

'''
polygons <QueryDict: {'addOrUpdatePolygonFlag': ['0'], 'polygonId': [''], 'name': ['test'], 'type': ['普通区域'], 'dma_no': [''], 'shape': ['多边形'],
 'description': [''], 'pointSeqs': ['0,1,2,3,4'], 'longitudes': ['114.083971,114.085848,114.08617,114.085215,114.083938'],
  'latitudes': ['22.547862,22.548234,22.547183,22.546718,22.547268']}>
'''
    # save ploygon
def polygons(request):
    print("polygons",request.POST)
    addOrUpdatePolygonFlag = request.POST.get("addOrUpdatePolygonFlag")
    polygonId = request.POST.get("polygonId")
    name = request.POST.get("name")
    ftype = request.POST.get("type")
    dma_no = request.POST.get("dma_no")
    shape = request.POST.get("shape")
    description = request.POST.get("description")
    pointSeqs = request.POST.get("pointSeqs")
    longitudes = request.POST.get("longitudes")
    latitudes = request.POST.get("latitudes")

    createDataUsername = request.user.user_name

    FenceDistrict.objects.create(name=name,ftype=ftype,createDataUsername=createDataUsername,description=description,cid="test_no1",pId="zw_m_polygon")
    Polygon.objects.create(polygonId=polygonId,name=name,ftype=ftype,shape=shape,pointSeqs=pointSeqs,longitudes=longitudes,latitudes=latitudes)

    return HttpResponse(json.dumps({"success":1}))



def getFenceDetails(request):
    print("getFenceDetails",request.POST)
    name = request.POST.get("name")
    fenceNodes = request.POST.get("fenceNodes")
    print("name",name)
    print("fenceNodes",fenceNodes,type(fenceNodes))
    fenceNodes_json = json.loads(fenceNodes)
    print("json ?",fenceNodes_json,type(fenceNodes_json[0]))
    name=fenceNodes_json[0]["name"]
    pgo = Polygon.objects.filter(name=name).values().first()

    fenceData = []
    pointSeqs = pgo["pointSeqs"].split(",")
    longitudes = pgo["longitudes"].split(",")
    latitudes = pgo["latitudes"].split(",")
    print(pointSeqs,type(pointSeqs))
    print(longitudes,type(longitudes))
    print(latitudes,type(latitudes))

    for p in pointSeqs:
        idx = int(p)
        fenceData.append({
            "createDataTime":"2018-11-08 20:46:57",
            "createDataUsername":"admin",
            "description":"null",
            "flag":1,
            "id":"null",
            "latitude":latitudes[idx],
            "longitude":longitudes[idx],
            "name":"null",
            "polygonId":"037f67e5-acfa-466f-a6b0-60916d88d8a2",
            "sortOrder":idx,
            "type":"null",
            "updateDataTime":"null",
            "updateDataUsername":"null"
            })

    details = {
        "exceptionDetailMsg":"null",
        "msg":"null",
        "obj":[
            {"fenceType":"zw_m_polygon",
            "fenceData":fenceData
            }],
        "success":1
    }

    return JsonResponse(details)