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

from .models import FenceDistrict,Polygon,FenceShape
# from django.contrib.gis.geos import Polygon

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

def fenceTree_organ(request):
    user = request.user
    fences = user.fence_list_queryset().values()

    fentree = [{"name":"圆形","pId":"-","id":"zw_m_circle","type":"fenceParent","open":"true"},
                {"name":"矩形","pId":"-","id":"zw_m_rectangle","type":"fenceParent","open":"true"},
                {"name":"多边形","pId":"-","id":"zw_m_polygon","type":"fenceParent","open":"true"},
                {"name":"行政区划","pId":"-","id":"zw_m_administration","type":"fenceParent","open":"true"},]
    for fs in fences:
        polygon = {
            "name":fs["name"],
            "pId":fs["pId"],
            "id":fs["cid"],
            "type":fs["ftype"],
            "open":"true"
            }
        if fs["pId"] == "zw_m_polygon":
            polygon["iconSkin"]="zw_m_polygon_skin",
        if fs["pId"] == "zw_m_rectangle":
            polygon["iconSkin"]="zw_m_rectangle_skin",
        if fs["pId"] == "zw_m_circle":
            polygon["iconSkin"]="zw_m_circle_skin",
        if fs["pId"] == "zw_m_administration":
            polygon["iconSkin"]="zw_m_administration_skin",
        fentree.append(polygon)

    return HttpResponse(json.dumps(fentree))

def fenceTree(request):
    return fenceTree_organ(request)
    fences = FenceDistrict.objects.values()

    fentree = []
    for fs in fences:
        polygon = {
            "name":fs["name"],
            "pId":fs["pId"],
            "id":fs["cid"],
            "type":fs["ftype"],
            "open":"true"
            }
        if fs["pId"] == "zw_m_polygon":
            polygon["iconSkin"]="zw_m_polygon_skin",
        if fs["pId"] == "zw_m_rectangle":
            polygon["iconSkin"]="zw_m_rectangle_skin",
        if fs["pId"] == "zw_m_circle":
            polygon["iconSkin"]="zw_m_circle_skin",
        if fs["pId"] == "zw_m_administration":
            polygon["iconSkin"]="zw_m_administration_skin",
        fentree.append(polygon)

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
def savePolygons(request):
    print("savePolygons",request.POST)
    addOrUpdatePolygonFlag = request.POST.get("addOrUpdatePolygonFlag")
    polygonId = request.POST.get("polygonId")
    name = request.POST.get("name")
    ftype = request.POST.get("type")
    belongto = request.POST.get("belongto")
    dma_no = request.POST.get("dma_no")
    shape = request.POST.get("shape")
    description = request.POST.get("description")
    pointSeqs = request.POST.get("pointSeqs")
    longitudes = request.POST.get("longitudes")
    latitudes = request.POST.get("latitudes")

    createDataUsername = request.user.user_name
    organ = Organizations.objects.get(name=belongto)

    if addOrUpdatePolygonFlag == "1":
        f = FenceDistrict.objects.get(cid=polygonId)
        p = FenceShape.objects.get(shapeId=polygonId)
        f.name = name
        f.belongto = organ
        f.dma_no = dma_no
        f.description = description
        f.save()
        p.name = name
        p.zonetype = ftype
        p.pointSeqs = pointSeqs
        p.longitudes = longitudes
        p.latitudes = latitudes
        p.dma_no = dma_no
        p.save()
        
    else:
        instance = FenceDistrict.objects.create(name=name,ftype="fence",createDataUsername=createDataUsername,description=description,pId="zw_m_polygon")
        FenceShape.objects.create(shapeId=instance.cid,name=name,zonetype=ftype,shape=shape,pointSeqs=pointSeqs,longitudes=longitudes,latitudes=latitudes,dma_no=dma_no)

    return HttpResponse(json.dumps({"success":1}))



def getFenceDetails(request):
    print("getFenceDetails",request.POST)
    dma_no = request.POST.get("dma_no") or ''
    fenceNodes = request.POST.get("fenceNodes")
    # print("dma_no",dma_no)
    # print("fenceNodes",fenceNodes)

    if dma_no != '':
        fenceData = []
        details_obj = []
        if FenceShape.objects.filter(dma_no=dma_no).exists():
            pgo = FenceShape.objects.filter(dma_no=dma_no).values().first()
            fd = FenceDistrict.objects.filter(cid=pgo["shapeId"]).values().first()
            
            pointSeqs = pgo["pointSeqs"].split(",")
            longitudes = pgo["longitudes"].split(",")
            latitudes = pgo["latitudes"].split(",")
            # print(pointSeqs,type(pointSeqs))
            # print(longitudes,type(longitudes))
            # print(latitudes,type(latitudes))

            for p in pointSeqs:
                idx = int(p)
                fenceData.append({
                    "createDataTime":fd["createDataTime"],
                    "createDataUsername":fd["createDataUsername"],
                    "description":fd["description"],
                    "flag":1,
                    "id":"null",
                    "latitude":latitudes[idx],
                    "longitude":longitudes[idx],
                    "name":"null",
                    "polygonId":pgo["shapeId"],
                    "sortOrder":idx,
                    "type":pgo["zonetype"],
                    "updateDataTime":fd["updateDataTime"],
                    "updateDataUsername":fd["updateDataUsername"]
                    })

            details_obj.append({"fenceType":"zw_m_polygon",
                "fillColor":pgo["fillColor"],
                "strokeColor":pgo["strokeColor"],
                "fenceData":fenceData
            })
        details = {
            "exceptionDetailMsg":"null",
            "msg":"null",
            "obj":details_obj,
            "success":1
        }

        return JsonResponse(details)

        

    if len(fenceNodes) == 0 or fenceNodes == '[null]' or fenceNodes == '[]':
        details = {
            "exceptionDetailMsg":"null",
            "msg":"empty?",
            # "obj":[
            #     {"fenceType":"zw_m_polygon",
            #     "fenceData":fenceData
            #     }],
            "success":0
        }

        return JsonResponse(details)
    
    fenceNodes_json = json.loads(fenceNodes)
    # print("json ?",fenceNodes_json,type(fenceNodes_json[0]),len(fenceNodes_json))
    details_obj = []
    for i in range(len(fenceNodes_json)):
        
        name=fenceNodes_json[i]["name"]
        pId = fenceNodes_json[i]["pId"]

        fd = FenceDistrict.objects.filter(name=name).values().first()
        pgo = FenceShape.objects.filter(name=name).values().first()
        fenceData = []
        if pId == "zw_m_polygon":

            
            pointSeqs = pgo["pointSeqs"].split(",")
            longitudes = pgo["longitudes"].split(",")
            latitudes = pgo["latitudes"].split(",")
            # print(pointSeqs,type(pointSeqs))
            # print(longitudes,type(longitudes))
            # print(latitudes,type(latitudes))

            for p in pointSeqs:
                idx = int(p)
                fenceData.append({
                    "createDataTime":fd["createDataTime"],
                    "createDataUsername":fd["createDataUsername"],
                    "description":fd["description"],
                    "flag":1,
                    "id":"null",
                    "latitude":latitudes[idx],
                    "longitude":longitudes[idx],
                    "name":"null",
                    "polygonId":pgo["shapeId"],
                    "sortOrder":idx,
                    "type":pgo["zonetype"],
                    "updateDataTime":fd["updateDataTime"],
                    "updateDataUsername":fd["updateDataUsername"]
                    })

            details_obj.append({"fenceType":pId,
                "fillColor":pgo["fillColor"],
                "strokeColor":pgo["strokeColor"],
                "fenceData":fenceData
            })

        if pId == "zw_m_rectangle":

            leftLongitude,leftLatitude = pgo["lnglatQuery_LU"].split(",")
            rightLongitude,rightLatitude = pgo["lnglatQuery_RD"].split(",")
            
            # fenceData.append({
            #     "createDataTime":fd["createDataTime"],
            #     "createDataUsername":fd["createDataUsername"],
            #     "description":fd["description"],
            #     "flag":1,
            #     "id":pgo["shapeId"],
            #     "leftLatitude":leftLatitude,
            #     "leftLongitude":leftLongitude,
            #     "rightLatitude":rightLatitude,
            #     "rightLongitude":rightLongitude,
            #     "name":pgo["name"],
            #     "type":pgo["zonetype"],
            #     "updateDataTime":fd["updateDataTime"],
            #     "updateDataUsername":fd["updateDataUsername"]
            #     })
            fenceData1 = {
                "createDataTime":fd["createDataTime"],
                "createDataUsername":fd["createDataUsername"],
                "description":fd["description"],
                "flag":1,
                "id":pgo["shapeId"],
                "leftLatitude":leftLatitude,
                "leftLongitude":leftLongitude,
                "rightLatitude":rightLatitude,
                "rightLongitude":rightLongitude,
                "name":pgo["name"],
                "type":pgo["zonetype"],
                "updateDataTime":fd["updateDataTime"],
                "updateDataUsername":fd["updateDataUsername"]
                }

            details_obj.append({"fenceType":pId,
            "fenceData":fenceData1
            })

        if pId == "zw_m_circle":

            latitude = pgo["centerPointLat"]
            longitude = pgo["centerPointLng"]
            radius = pgo["centerRadius"]
            
            fenceData1 = {
                "createDataTime":fd["createDataTime"],
                "createDataUsername":fd["createDataUsername"],
                "description":fd["description"],
                "flag":1,
                "id":pgo["shapeId"],
                "latitude":latitude,
                "longitude":longitude,
                "radius":radius,
                "name":pgo["name"],
                "type":pgo["zonetype"],
                "updateDataTime":fd["updateDataTime"],
                "updateDataUsername":fd["updateDataUsername"]
                }

            details_obj.append({"fenceType":pId,
            "fenceData":fenceData1
            })

        if pId == "zw_m_administration":

            latitude = pgo["centerPointLat"]
            longitude = pgo["centerPointLng"]
            administrativeLngLats = pgo["administrativeLngLat"].split('-')
            for i in range(len(administrativeLngLats)):
                plists = administrativeLngLats[i].split(',')
                tmp = []
                for j in range(0,len(plists),2):
                    p = [plists[j],plists[j+1]]
                    tmp.append(p)
                fenceData.append(tmp)
            
            


            details_obj.append({"fenceType":pId,
                "fenceData":fenceData,
                "aId":pgo["shapeId"]
                })
    

    details = {
        "exceptionDetailMsg":"null",
        "msg":"null",
        "obj":details_obj,
        "success":1
    }

    return JsonResponse(details)


# 编辑dma分区围栏预览
def previewFence(request):
    print("previewFence",request.POST)
    fenceIdShape = request.POST.get("fenceIdShape") 
    
    fenceId,shape = fenceIdShape.split("#")

    fd = FenceDistrict.objects.filter(cid=fenceId).values("createDataTime","createDataUsername","description","name","updateDataTime","updateDataUsername","belongto__name").first()
    pgo = FenceShape.objects.filter(shapeId=fenceId).values().first()

    details_obj = []
    fenceData = []
    if shape == "zw_m_polygon":

            
        pointSeqs = pgo["pointSeqs"].split(",")
        longitudes = pgo["longitudes"].split(",")
        latitudes = pgo["latitudes"].split(",")
        # print(pointSeqs,type(pointSeqs))
        # print(longitudes,type(longitudes))
        # print(latitudes,type(latitudes))

        for p in pointSeqs:
            idx = int(p)
            fenceData.append({
                "createDataTime":fd["createDataTime"],
                "createDataUsername":fd["createDataUsername"],
                "description":fd["description"],
                "flag":1,
                "id":pgo["shapeId"],
                "latitude":latitudes[idx],
                "longitude":longitudes[idx],
                "name":fd["name"],
                "polygonId":pgo["shapeId"],
                "sortOrder":idx,
                "type":pgo["zonetype"],
                "updateDataTime":fd["updateDataTime"],
                "updateDataUsername":fd["updateDataUsername"]
                })

    if shape == "zw_m_rectangle":

        leftLongitude,leftLatitude = pgo["lnglatQuery_LU"].split(",")
        rightLongitude,rightLatitude = pgo["lnglatQuery_RD"].split(",")
        
        fenceData = {
            "createDataTime":fd["createDataTime"],
            "createDataUsername":fd["createDataUsername"],
            "description":fd["description"],
            "flag":1,
            "id":pgo["shapeId"],
            "leftLatitude":leftLatitude,
            "leftLongitude":leftLongitude,
            "rightLatitude":rightLatitude,
            "rightLongitude":rightLongitude,
            "name":pgo["name"],
            "type":pgo["zonetype"],
            "updateDataTime":fd["updateDataTime"],
            "updateDataUsername":fd["updateDataUsername"]
            }

    if shape == "zw_m_circle":

        latitude = pgo["centerPointLat"]
        longitude = pgo["centerPointLng"]
        radius = pgo["centerRadius"]
        
        fenceData = {
            "createDataTime":fd["createDataTime"],
            "createDataUsername":fd["createDataUsername"],
            "description":fd["description"],
            "flag":1,
            "id":pgo["shapeId"],
            "latitude":latitude,
            "longitude":longitude,
            "radius":radius,
            "name":pgo["name"],
            "type":pgo["zonetype"],
            "updateDataTime":fd["updateDataTime"],
            "updateDataUsername":fd["updateDataUsername"]
            }


    details_obj.append({"fenceType":shape,
        "fenceData":fenceData
        })

    if shape == "zw_m_polygon":
        details_obj[0]["polygon"] = {
                "createDataTime":fd["createDataTime"],
                "createDataUsername":fd["createDataUsername"],
                "description":fd["description"],
                "flag":1,
                "id":pgo["shapeId"],
                "belongto":fd["belongto__name"],
                "dma_no":pgo["dma_no"],
                "latitude":"null",
                "longitude":"null",
                "name":fd["name"],
                "polygonId":"null",
                "sortOrder":"null",
                "type":pgo["zonetype"],
                "updateDataTime":fd["updateDataTime"],
                "updateDataUsername":fd["updateDataUsername"]
            }
        details_obj[0]["fillColor"] = pgo["fillColor"]
        details_obj[0]["strokeColor"] = pgo["strokeColor"]

    
    details = {
        "exceptionDetailMsg":"null",
        "msg":"null",
        "obj":details_obj,
        "success":1
    }

    return JsonResponse(details)


def deleteFence(request):
    print("deteleFence",request.POST)
    fenceId = request.POST.get("fenceId")

    fd = FenceDistrict.objects.get(cid=fenceId)
    pgo = FenceShape.objects.get(shapeId=fenceId)
    pgo.delete()
    fd.delete()

    details = {
        "exceptionDetailMsg":"null",
        "msg":"null",
        "obj":"null",
        "success":True
    }

    return JsonResponse(details)


def saveRectangles(request):
    print("saveRectangles",request.POST)
    addOrUpdateRectangleFlag = request.POST.get("addOrUpdateRectangleFlag")
    shapeId = request.POST.get("rectangleId")
    name = request.POST.get("name")
    zonetype = request.POST.get("type")
    lnglatQuery_LU = request.POST.get("lnglatQuery_LU")
    lnglatQuery_RD = request.POST.get("lnglatQuery_RD")
    dma_no = request.POST.get("dma_no")
    shape = request.POST.get("shape")
    description = request.POST.get("description")
    pointSeqs = request.POST.get("pointSeqs")
    longitudes = request.POST.get("longitudes")
    latitudes = request.POST.get("latitudes")

    createDataUsername = request.user.user_name

    if addOrUpdateRectangleFlag == "1":
        f = FenceDistrict.objects.get(cid=shapeId)
        p = FenceShape.objects.get(shapeId=shapeId)
        f.name = name
        f.description = description
        f.save()
        p.name = name
        p.zonetype = zonetype
        p.lnglatQuery_LU = lnglatQuery_LU
        p.lnglatQuery_RD = lnglatQuery_RD
        p.pointSeqs = pointSeqs
        p.longitudes = longitudes
        p.latitudes = latitudes
        p.save()
        
    else:
        instance = FenceDistrict.objects.create(name=name,ftype="fence",createDataUsername=createDataUsername,description=description,pId="zw_m_rectangle")
        FenceShape.objects.create(shapeId=instance.cid,name=name,zonetype=zonetype,shape=shape,lnglatQuery_LU=lnglatQuery_LU,lnglatQuery_RD=lnglatQuery_RD,pointSeqs=pointSeqs,longitudes=longitudes,latitudes=latitudes,dma_no=dma_no)

    return HttpResponse(json.dumps({"success":1}))


def saveCircles(request):
    print("saveCircles",request.POST)
    addOrUpdateCircleFlag = request.POST.get("addOrUpdateCircleFlag")
    shapeId = request.POST.get("circleId")
    name = request.POST.get("name")
    zonetype = request.POST.get("type")
    centerPointLat = request.POST.get("centerPointLat")
    centerPointLng = request.POST.get("centerPointLng")
    centerRadius = request.POST.get("centerRadius")
    latitude = request.POST.get("latitude")
    longitude = request.POST.get("longitude")
    dma_no = request.POST.get("dma_no")
    shape = request.POST.get("shape")
    description = request.POST.get("description")
    centerRadius = request.POST.get("centerRadius")
    radius = request.POST.get("radius")
    

    createDataUsername = request.user.user_name

    if addOrUpdateCircleFlag == "1":
        f = FenceDistrict.objects.get(cid=shapeId)
        p = FenceShape.objects.get(shapeId=shapeId)
        f.name = name
        f.description = description
        f.save()
        p.name = name
        p.zonetype = zonetype
        p.centerPointLat = centerPointLat
        p.centerPointLng = centerPointLng
        p.centerRadius = centerRadius
        
        p.save()
        
    else:
        instance = FenceDistrict.objects.create(name=name,ftype="fence",createDataUsername=createDataUsername,description=description,pId="zw_m_circle")
        FenceShape.objects.create(shapeId=instance.cid,name=name,zonetype=zonetype,shape=shape,centerPointLat=centerPointLat,centerPointLng=centerPointLng,centerRadius=centerRadius,dma_no=dma_no)

    return HttpResponse(json.dumps({"success":1}))


def addAdministration(request):
    print("addAdministration",request.POST)
    addOrUpdateCircleFlag = request.POST.get("addOrUpdateCircleFlag")
    shapeId = request.POST.get("administrativeAreaId")
    province = request.POST.get("province")
    city = request.POST.get("city")
    district = request.POST.get("district")
    name = request.POST.get("name")
    description = request.POST.get("description")
    administrativeLngLat = request.POST.get("administrativeLngLat")

    # zonetype = request.POST.get("type")
    
    dma_no = request.POST.get("dma_no")
    organ = Organizations.objects.first()
    
    

    createDataUsername = request.user.user_name

    if addOrUpdateCircleFlag == "1":
        f = FenceDistrict.objects.get(cid=shapeId)
        p = FenceShape.objects.get(shapeId=shapeId)
        f.name = name
        f.description = description
        f.save()
        p.name = name
        p.zonetype = zonetype
        p.centerPointLat = centerPointLat
        p.centerPointLng = centerPointLng
        p.centerRadius = centerRadius
        
        p.save()
        
    else:
        instance = FenceDistrict.objects.create(name=name,ftype="fence",createDataUsername=createDataUsername,description=description,pId="zw_m_administration",belongto=organ)
        FenceShape.objects.create(shapeId=instance.cid,name=name,province=province,city=city,district=district,administrativeLngLat=administrativeLngLat,dma_no=dma_no)

    return HttpResponse(json.dumps({"success":1}))


def alterFillColor(request):
    dma_no = request.POST.get("dma_no")
    fillColor = request.POST.get("fillColor")

    pgo = FenceShape.objects.filter(dma_no=dma_no)

    if pgo.exists():
        p = pgo.first()
        p.fillColor = fillColor
        p.save()

    return HttpResponse(json.dumps({"success":1}))


def alterstrokeColor(request):
    dma_no = request.POST.get("dma_no")
    strokeColor = request.POST.get("strokeColor")

    pgo = FenceShape.objects.filter(dma_no=dma_no)

    if pgo.exists():
        p = pgo.first()
        p.strokeColor = strokeColor
        p.save()

    return HttpResponse(json.dumps({"success":1}))

# 一次获取所有基本信息，供js实现逻辑效果
def getDMAFenceOnce(request):
    print("getDMAFenceOnce request",request.POST)
    dma_level = request.POST.get("dma_level") or '2'

    user = request.user
    # dma_no_list = user.dma_list_queryset().values_list("dma_no")
    dma_lists = user.dma_list_queryset().values("pk","dma_name","dma_no","belongto__cid","belongto__organlevel")

    dma_no_list = [d["dma_no"] for d in dma_lists]
    allfence = FenceShape.objects.filter(dma_no__in=dma_no_list).values()

    details_obj = []
    for pgo in allfence:
        dma_no = pgo["dma_no"]
        shapeId = pgo["shapeId"]
        if dma_no == '' or dma_no == None:
            continue

        dma = DMABaseinfo.objects.get(dma_no=dma_no)
        # if dflag == '1':
        #     if dma.belongto not in organ.sub_organizations(include_self=True):
        #         continue

        # print(shapeId,dma_no,pgo["name"])
        fenceData = []
        pointSeqs = pgo["pointSeqs"].split(",")
        longitudes = pgo["longitudes"].split(",")
        latitudes = pgo["latitudes"].split(",")
        
        for p in pointSeqs:
            idx = int(p)
            fenceData.append({
                
                "flag":1,
                "id":"null",
                "latitude":latitudes[idx],
                "longitude":longitudes[idx],
                "name":"null",
                "polygonId":pgo["shapeId"],
                "sortOrder":idx,
                "type":pgo["zonetype"],
                
                })

        details_obj.append({"fenceType":"zw_m_polygon",
            "fillColor":pgo["fillColor"],
            "strokeColor":pgo["strokeColor"],
            "dmaMapStatistic":dma.dmaMapStatistic(),
            "fenceData":fenceData
        })
    details = {
        "exceptionDetailMsg":"null",
        "msg":"null",
        "obj":details_obj,
        "success":1
    }

    return JsonResponse(details)


# DMA在线监视dma group dmaMapStatistic
# 一般水司只有一个DMA一级分区，用户登录后显示所属组织所有二级分区，当选择二级分区时再显示该二级分区的所有三级分区
def getDMAFenceDetails(request):
    return getDMAFenceOnce(request)
    print("getDMAFenceDetails",request.POST)
    dma_no = request.POST.get("dma_no") or ''
    dflag = request.POST.get("dflag") #0:all 1:organization 2:dma
    current_organ = request.POST.get("current_organ")
    fenceNodes = request.POST.get("fenceNodes")
    dma_level = request.POST.get("dma_level") or '2'
    # print("dma_no",dma_no)
    # print("fenceNodes",fenceNodes)
    user = request.user
    # dma_no_list = user.dma_list_queryset().filter(belongto__cid__icontains=current_organ).filter(belongto__organlevel=dma_level).values_list("dma_no")
    # dma_no_list = user.dma_list_queryset().filter(belongto__cid__icontains=current_organ).values_list("dma_no") #why filter
    dma_no_list = user.dma_list_queryset().values_list("dma_no")
    print("dma_no_list:",dma_no_list)

    if dflag == '2':
        allfence = FenceShape.objects.filter(dma_no=dma_no).values()
        # allfence = user.dma_list_queryset("","3",dma_no).values()
        # print("allfence",allfence)
    else:
        allfence = FenceShape.objects.filter(dma_no__in=dma_no_list).values()

    details_obj = []
    for pgo in allfence:
        dma_no = pgo["dma_no"]
        shapeId = pgo["shapeId"]
        if dma_no == '' or dma_no == None:
            continue

        dma = DMABaseinfo.objects.get(dma_no=dma_no)
        # if dflag == '1':
        #     if dma.belongto not in organ.sub_organizations(include_self=True):
        #         continue

        fd = FenceDistrict.objects.filter(cid=shapeId).values().first()
        fenceData = []
        pointSeqs = pgo["pointSeqs"].split(",")
        longitudes = pgo["longitudes"].split(",")
        latitudes = pgo["latitudes"].split(",")
        
        for p in pointSeqs:
            idx = int(p)
            fenceData.append({
                "createDataTime":fd["createDataTime"],
                "createDataUsername":fd["createDataUsername"],
                "description":fd["description"],
                "flag":1,
                "id":"null",
                "latitude":latitudes[idx],
                "longitude":longitudes[idx],
                "name":"null",
                "polygonId":pgo["shapeId"],
                "sortOrder":idx,
                "type":pgo["zonetype"],
                "updateDataTime":fd["updateDataTime"],
                "updateDataUsername":fd["updateDataUsername"]
                })

        details_obj.append({"fenceType":"zw_m_polygon",
            "fillColor":pgo["fillColor"],
            "strokeColor":pgo["strokeColor"],
            "dmaMapStatistic":dma.dmaMapStatistic(),
            "fenceData":fenceData
        })

            
            
    details = {
        "exceptionDetailMsg":"null",
        "msg":"null",
        "obj":details_obj,
        "success":1
    }

    return JsonResponse(details)

        


