# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404,render,redirect
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect,StreamingHttpResponse
from django.contrib import messages
from django.template import TemplateDoesNotExist
import json
import random
import datetime

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
from . models import WaterUserType,DMABaseinfo,DmaStations,Station,Meter
from .forms import StationsForm,StationsEditForm
from . forms import WaterUserTypeForm,DMACreateForm,DMABaseinfoForm,StationAssignForm
import os
from django.conf import settings

from waterwork.mixins import AjaxableResponseMixin
import logging

logger_info = logging.getLogger('info_logger')
logger_error = logging.getLogger('error_logger')




def dmatree(request):   
    organtree = []
    
    stationflag = request.POST.get("isStation") or ''
    dmaflag = request.POST.get("isDma") or ''
    user = request.user
    
    # if user.is_anonymous:
    if not user.is_authenticated:
        organs = Organizations.objects.first()
    else:
        organs = user.belongto #Organizations.objects.all()
    print("dmatree",organs)
    for o in organs.get_descendants(include_self=True):
        if o.dma.exists():
            p_dma_no = o.dma.first().dma_no
        else:
            p_dma_no = ''
        organtree.append({
            "name":o.name,
            "id":o.cid,
            "pId":o.pId,
            "districtid":'',
            "type":"group",
            "dma_no":p_dma_no,  #如果存在dma分区，分配第一个dma分区的dma_no，点击数条目的时候使用
            "icon":"/static/virvo/resources/img/wenjianjia.png",
            "uuid":o.uuid
        })

        #dma
        if dmaflag == '1':
            for d in o.dma.all():
                organtree.append({
                "name":d.dma_name,
                "id":d.pk,
                "districtid":d.pk,
                "pId":o.cid,
                "type":"dma",
                "dma_no":d.dma_no,
                "icon":"/static/virvo/resources/img/dma.png",
                "uuid":''
            })

        #station
        if stationflag == '1':
            for s in o.station_set.all():
                # if s.dmaid is None: #已分配dma分区的不显示
                organtree.append({
                    "name":s.username,
                    "id":s.pk,
                    "districtid":'',
                    "pId":o.cid,
                    "type":"station",
                    "dma_no":'',
                    "icon":"/static/virvo/resources/img/station.png",
                    "uuid":''
                })

    # district
    # districts = District.objects.all()
    # for d in districts:
    #     organtree.append({
    #         "name":d.name,
    #         "id":d.id,
    #         "districtid":d.id,
    #         "pId":organs.cid,
    #         "type":"district",
    #         "icon":"/static/virvo/resources/img/u8836.png",
    #         "uuid":''
    #     })
        # bigmeters = Bigmeter.objects.filter(districtid=d.id)
        # for b in bigmeters:
        #     organtree.append({
        #     "name":b.username,
        #     "id":b.userid,
        #     "stationid":b.userid,
        #     "pId":d.id,
        #     "type":"station",
        #     "icon":"/static/virvo/resources/img/u8836.png",
        #     "uuid":''
        # })

    #bigmeter

    
    result = dict()
    result["data"] = organtree
    
    # print(json.dumps(result))
    
    return HttpResponse(json.dumps(organtree))


def getmeterlist(request):

    meters = Meter.objects.all()

    def m_info(m):
        
        return {
            "id":m.pk,
            "serialnumber":m.serialnumber,
            
        }
    data = []

    for m in meters:
        data.append(m_info(m))

    operarions_list = {
        "exceptionDetailMsg":"null",
        "msg":None,
        "obj":{
                "meterlist":data
        },
        "success":True
    }
   

    return JsonResponse(operarions_list)


def getmeterParam(request):

    mid = request.POST.get("mid")
    meter = Meter.objects.get(id=int(mid))
    operarions_list = {
        "exceptionDetailMsg":"null",
        "msg":None,
        "obj":{
                "id":meter.pk,
                "simid":meter.simid.simcardNumber if meter.simid else "",
                "dn":meter.dn,
                "belongto":meter.belongto.name,#current_user.belongto.name,
                "metertype":meter.metertype,
                "serialnumber":meter.serialnumber,
        },
        "success":True
    }
   

    return JsonResponse(operarions_list)

def stationlist(request):
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

    

    #当前登录用户
    current_user = request.user

    def u_info(u):  #u means station

        simcardNumber = ""
        if u.meter:
            s = u.meter.simid
            if s:
                simcardNumber = s.simcardNumber
        
        return {
            "id":u.pk,
            "username":u.username,
            "usertype":u.usertype,
            "simid":simcardNumber,
            "dn":u.meter.dn if u.meter else '',
            "belongto":u.belongto.name,# if u.meter else '',#current_user.belongto.name,
            "metertype":u.meter.metertype if u.meter else '',
            "serialnumber":u.meter.serialnumber if u.meter else '',
            "big_user":1,
            "focus":1,
            "createdate":u.madedate,
            "related":True if u.dmaid.all().count() else False
        }
    data = []
    
    
    # userl = current_user.user_list()

    # bigmeters = Bigmeter.objects.all()
    # stations = Station.objects.all()
    stations = current_user.station_list_queryset()

    if districtId != '': #dma
        dma = DMABaseinfo.objects.get(pk=int(districtId))
        dma_stations = dma.station_set.all()
        stations = [s for s in dma_stations if s in stations]
    elif groupName != '':
        filter_group = Organizations.objects.get(cid=groupName)
        stations = [s for s in stations if s.belongto == filter_group]
    
    
    # # print("user all:",userl)
    # if districtId != "":
    #     #查询的组织
    #     query_district = District.objects.get(id=districtId)
    #     bigmeters = [u for u in bigmeters if u.districtid == query_district]
    #     # print("query organ user,",userl)
    # for m in bigmeters[start:start+length]:
    #     data.append(u_info(m))
    
    
    # def search_user(u):
    #     if simpleQueryParam in u.user_name or simpleQueryParam in u.real_name or simpleQueryParam in u.email or simpleQueryParam in u.phone_number :
    #         return True


    # if simpleQueryParam != "":
    #     print('simpleQueryParam:',simpleQueryParam)
    #     # userl = userl.filter(real_name__icontains=simpleQueryParam)
    #     userl = [u for u in userl if search_user(u) is True]
    
    # for u in userl[start:start+length]:
    #     data.append(u_info(u))

    

    for m in stations[start:start+length]:
        data.append(u_info(m))
    
    recordsTotal = len(stations)
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

    
    
    return HttpResponse(json.dumps(result))


def dmastationlist(request):
    print("userlist",request.POST,request.kwargs)
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

    

    #当前登录用户
    current_user = request.user

    def u_info(u):
        
        return {
            "id":u.pk,
            "username":u.username,
            "usertype":u.usertype,
            "simid":u.meter.simid.simcardNumber if u.meter and u.meter.simid else '',
            "dn":u.meter.dn if u.meter else '',
            "belongto":u.meter.belongto.name if u.meter else '',#current_user.belongto.name,
            "metertype":u.meter.metertype if u.meter else '',
            "serialnumber":u.meter.serialnumber if u.meter else '',
            "big_user":1,
            "focus":1,
            "createdate":u.madedate
        }
    data = []
    
    
    # userl = current_user.user_list()

    # bigmeters = Bigmeter.objects.all()
    # dma_pk = request.POST.get("pk") or 4
    dma_pk=4
    dma = DMABaseinfo.objects.first() #get(pk=int(dma_pk))
    stations = dma.station_set.all()
    
    
    

    

    for m in stations[start:start+length]:
        data.append(u_info(m))
    
    recordsTotal = len(stations)
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

    
    
    return HttpResponse(json.dumps(result))

# class DistrictFormView(FormView):
#     form_class = DMABaseinfoForm

def dmabaseinfo(request):

    if request.method == 'GET':
        
        data = []
        dma_no = request.GET.get("dma_no")
        if dma_no == '':
            operarions_list = {
                "exceptionDetailMsg":"null",
                "msg":None,
                "obj":{
                        "baseinfo":{
                            "dma_no":'',
                            "pepoles_num":'',
                            "acreage":'',
                            "user_num":'',
                            "pipe_texture":'',
                            "pipe_length":'',
                            "pipe_links":'',
                            "pipe_years":'',
                            "pipe_private":'',
                            "ifc":'',
                            "aznp":'',
                            "night_use":'',
                            "cxc_value":'',
                            "belongto":''
                            },
                        "dmastationlist":data
                },
                "success":True
            }
           

            return JsonResponse(operarions_list)
            

        dmabase = DMABaseinfo.objects.get(dma_no=dma_no)

        def u_info(u):
        
            return {
                "id":u.pk,
                "username":u.username,
                "usertype":u.usertype,
                "simid":u.meter.simid.simcardNumber if u.meter and u.meter.simid else '',
                "dn":u.meter.dn if u.meter else '',
                "belongto":u.meter.belongto.name if u.meter else '',#current_user.belongto.name,
                "metertype":u.meter.metertype if u.meter else '',
                "serialnumber":u.meter.serialnumber if u.meter else '',
                "big_user":1,
                "focus":1,
                "createdate":u.madedate
            }
        
        #dma分区的站点
        stations = dmabase.station_set.all()
        for s in stations:
            data.append(u_info(s))

        operarions_list = {
            "exceptionDetailMsg":"null",
            "msg":None,
            "obj":{
                    "baseinfo":{
                        "dma_no":dmabase.dma_no,
                        "pepoles_num":dmabase.pepoles_num,
                        "acreage":dmabase.acreage,
                        "user_num":dmabase.user_num,
                        "pipe_texture":dmabase.pipe_texture,
                        "pipe_length":dmabase.pipe_length,
                        "pipe_links":dmabase.pipe_links,
                        "pipe_years":dmabase.pipe_years,
                        "pipe_private":dmabase.pipe_private,
                        "ifc":dmabase.ifc,
                        "aznp":dmabase.aznp,
                        "night_use":dmabase.night_use,
                        "cxc_value":dmabase.cxc_value,
                        "belongto":dmabase.belongto.name
                        },
                    "dmastationlist":data
            },
            "success":True
        }
       

        return JsonResponse(operarions_list)

    if request.method == 'POST':
        print('dmabaseinfo post:',request.POST)
        # dma_no = request.POST.get("dma_no")
        # dmabase = DMABaseinfo.objects.get(dma_no=dma_no)
        # form = DMABaseinfoForm(request.POST or None)
        # if form.is_valid():
        #     form.save()
        #     flag = 1
        # err_str = ""
        # if form.errors:
        #     flag = 0
        #     for k,v in form.errors.items():
        #         print(k,v)
        #         err_str += v[0]
    
        # data = {
        #     "success": flag,
        #     "errMsg":err_str
            
        # }
        
        # return HttpResponse(json.dumps(data)) #JsonResponse(data)


    return HttpResponse(json.dumps({"success":True}))


def getdmamapusedata(request):
    print('getdmamapusedata:',request.GET)
    dma_name = request.GET.get("dma_name")
    dma = DMABaseinfo.objects.get(dma_name=dma_name)
    dmastation = dma.dmastation.first()
    commaddr = dmastation.station_id

    dmaflow = 0
    month_sale = 0
    lastmonth_sale = 0
    bili = 0
    today = datetime.date.today()
    today_str = today.strftime("%Y-%m-%d")
    today_flow = HdbFlowDataDay.objects.filter(hdate=today_str)
    if today_flow.exists():
        dmaflow = today_flow.first().dosage

    month_str = today.strftime("%Y-%m")
    month_flow = HdbFlowDataMonth.objects.filter(hdate=month_str)
    if month_flow.exists():
        month_sale = month_flow.first().dosage

    lastmonth = datetime.datetime(year=today.year,month=today.month-1,day=today.day)
    lastmonth_str = lastmonth.strftime("%Y-%m")
    lastmonth_flow = HdbFlowDataMonth.objects.filter(hdate=lastmonth_str)
    if lastmonth_flow.exists():
        lastmonth_sale = lastmonth_flow.first().dosage

    if float(month_sale) > 0 and float(lastmonth_sale) > 0:
        bili =  (float(month_sale) - float(lastmonth_sale) ) / float(lastmonth_sale)

    data = {
        "dma_statics":{
            "belongto":dma.belongto.name,
            "dma_level":"二级",
            "dma_status":"在线",
            "dmaflow":round(float(dmaflow),2),
            "month_sale":round(float(month_sale),2),
            "lastmonth_sale":round(float(lastmonth_sale),2),
            "bili":round(bili,2)
        }
    }

    return HttpResponse(json.dumps(data))

class DMABaseinfoEditView(AjaxableResponseMixin,UserPassesTestMixin,UpdateView):
    model = DMABaseinfo
    form_class = DMABaseinfoForm
    template_name = "dmam/baseinfo.html"
    success_url = reverse_lazy("dmam:districtmanager");

    # @method_decorator(permission_required("dma.change_stations"))
    def dispatch(self, *args, **kwargs):
        # self.role_id = kwargs["pk"]
        return super(DMABaseinfoEditView, self).dispatch(*args, **kwargs)

    def test_func(self):
        if self.request.user.has_menu_permission_edit('dmamanager_basemanager'):
            return True
        return False

    def handle_no_permission(self):
        data = {
                "mheader": "修改用户",
                "err_msg":"您没有权限进行操作，请联系管理员."
                    
            }
        # return HttpResponse(json.dumps(err_data))
        return render(self.request,"dmam/permission_error.html",data)

    def form_invalid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        print("dmabaseinfo edit form_invalid?:",self.request.POST)
        # print(form)
        # do something
        
                

        return super(DMABaseinfoEditView,self).form_invalid(form)

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        print("dmabaseinfo edit here?:",self.request.POST)
        # print(form)
        # do something
        belongto_name = form.cleaned_data.get("belongto")
        print('belongto_name',belongto_name)
        organ = Organizations.objects.get(name=belongto_name)
        instance = form.save(commit=False)
        instance.belongto = organ
                

        return super(DMABaseinfoEditView,self).form_valid(form)

    # def get_object(self):
    #     print(self.kwargs)
    #     return Organizations.objects.get(cid=self.kwargs["pId"])

class DistrictMangerView(LoginRequiredMixin,TemplateView):
    template_name = "dmam/districtlist.html"

    def get_context_data(self, *args, **kwargs):
        context = super(DistrictMangerView, self).get_context_data(*args, **kwargs)
        context["page_menu"] = "dma管理"
        # context["page_submenu"] = "组织和用户管理"
        context["page_title"] = "dma分区管理"
        user_organ = self.request.user.belongto

        default_dma = DMABaseinfo.objects.first()   # user_organ.dma.all().first()
        # print('districtmanager',default_dma.pk,default_dma.dma_name)
        context["current_dma_pk"] = default_dma.pk if default_dma else ''
        context["current_dma_no"] = default_dma.dma_no if default_dma else ''
        context["current_dma_name"] = default_dma.dma_name if default_dma else ''

        # context["user_list"] = User.objects.all()
        

        return context  

    """
group add
"""
def verifydmano(request):
    dma_no = request.POST.get("dma_no")
    bflag = not DMABaseinfo.objects.filter(dma_no=dma_no).exists()

    return HttpResponse(json.dumps({"success":bflag}))

def verifydmaname(request):
    dma_name = request.POST.get("dma_name")
    bflag = not DMABaseinfo.objects.filter(dma_name=dma_name).exists()

    return HttpResponse(json.dumps({"success":bflag}))    


def verifyusername(request):
    username = request.POST.get("username")
    bflag = not Station.objects.filter(username=username).exists()

    return HttpResponse(json.dumps({"success":bflag}))  

class DistrictAddView(AjaxableResponseMixin,UserPassesTestMixin,CreateView):
    model = Organizations
    template_name = "dmam/districtadd.html"
    form_class = DMACreateForm
    success_url = reverse_lazy("dmam:districtmanager");

    # @method_decorator(permission_required("dma.change_stations"))
    def dispatch(self, *args, **kwargs):
        print("dispatch",args,kwargs)
        if self.request.method == "GET":
            cid = self.request.GET.get("id")
            pid = self.request.GET.get("pid")
            kwargs["cid"] = cid
            kwargs["pId"] = pid
        return super(DistrictAddView, self).dispatch(*args, **kwargs)

    def test_func(self):
        if self.request.user.has_menu_permission_edit('dmamanager_basemanager'):
            return True
        return False

    def handle_no_permission(self):
        data = {
                "mheader": "修改用户",
                "err_msg":"您没有权限进行操作，请联系管理员."
                    
            }
        # return HttpResponse(json.dumps(err_data))
        return render(self.request,"dmam/permission_error.html",data)

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        print("dma add here?:",self.request.POST)
        print(form)
        # do something
        instance = form.save(commit=False)
        instance.is_org = True
        cid = self.request.POST.get("pId","oranization")  #cid is parent orgnizations
        print('cid:',cid)
        organizaiton_belong = Organizations.objects.get(cid=cid)
        instance.belongto = organizaiton_belong
        
        


        return super(DistrictAddView,self).form_valid(form)   

    # def get_context_data(self, *args, **kwargs):
    #     context = super(DistrictAddView, self).get_context_data(*args, **kwargs)
    #     context["cid"] = kwargs.get("cid")
    #     context["pId"] = kwargs.get("pId")
        

    #     return context  

    def get(self,request, *args, **kwargs):
        print("get::::",args,kwargs)
        form = super(DistrictAddView, self).get_form()
        # Set initial values and custom widget
        # initial_base = self.get_initial() #Retrieve initial data for the form. By default, returns a copy of initial.
       
        # initial_base["cid"] = kwargs.get("cid")
        # initial_base["pId"] = kwargs.get("pId")
        # form.initial = initial_base
        cid = kwargs.get("cid")
        pId = kwargs.get("pId")
        
        return render(request,self.template_name,
                      {"form":form,"cid":cid,"pId":pId})


"""
Group edit, manager
"""
class DistrictEditView(AjaxableResponseMixin,UserPassesTestMixin,UpdateView):
    model = DMABaseinfo
    form_class = DMACreateForm
    template_name = "dmam/districtedit.html"
    success_url = reverse_lazy("dmam:districtmanager");

    # @method_decorator(permission_required("dma.change_stations"))
    def dispatch(self, *args, **kwargs):
        # self.role_id = kwargs["pk"]
        return super(DistrictEditView, self).dispatch(*args, **kwargs)

    def test_func(self):
        if self.request.user.has_menu_permission_edit('dmamanager_basemanager'):
            return True
        return False

    def handle_no_permission(self):
        data = {
                "mheader": "修改用户",
                "err_msg":"您没有权限进行操作，请联系管理员."
                    
            }
        # return HttpResponse(json.dumps(err_data))
        return render(self.request,"dmam/permission_error.html",data)

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        print("group update here?:",self.request.POST)
        # print(form)
        # do something
        
                

        return super(DistrictEditView,self).form_valid(form)

    def get_object(self):
        print(self.kwargs)
        return DMABaseinfo.objects.get(pk=self.kwargs["pId"])
        

"""
Group Detail, manager
"""
class DistrictDetailView(DetailView):
    model = DMABaseinfo
    form_class = DMABaseinfoForm
    template_name = "dmam/districtdetail.html"
    # success_url = reverse_lazy("entm:rolemanager");

    # @method_decorator(permission_required("dma.change_stations"))
    def dispatch(self, *args, **kwargs):
        # self.role_id = kwargs["pk"]
        return super(DistrictDetailView, self).dispatch(*args, **kwargs)

    
    def get_object(self):
        print(self.kwargs)
        return DMABaseinfo.objects.get(pk=self.kwargs["pId"])

"""
Assets comment deletion, manager
"""
class DistrictDeleteView(AjaxableResponseMixin,UserPassesTestMixin,DeleteView):
    model = DMABaseinfo
    # template_name = "aidsbank/asset_comment_confirm_delete.html"

    def dispatch(self, *args, **kwargs):
        # self.comment_id = kwargs["pk"]

        
        print(self.request.POST)
        kwargs["pId"] = self.request.POST.get("pId")
        print("delete dispatch:",args,kwargs)
        return super(DistrictDeleteView, self).dispatch(*args, **kwargs)

    def test_func(self):
        if self.request.user.has_menu_permission_edit('dmamanager_basemanager'):
            return True
        return False

    def handle_no_permission(self):
        data = {
                "success": 0,
                "msg":"您没有权限进行操作，请联系管理员."
                    
            }
        return HttpResponse(json.dumps(data))
        # return render(self.request,"dmam/permission_error.html",data)

    def get_object(self,*args, **kwargs):
        print("delete objects:",self.kwargs,kwargs)
        return DMABaseinfo.objects.get(pk=kwargs["pId"])

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        print("delete?",args,kwargs)
        self.object = self.get_object(*args,**kwargs)
            

        self.object.delete()
        return JsonResponse({"success":True})


class DistrictAssignStationView(AjaxableResponseMixin,UserPassesTestMixin,UpdateView):
    model = DMABaseinfo
    form_class = StationAssignForm
    template_name = "dmam/districtassignstation.html"
    success_url = reverse_lazy("dmam:districtmanager");

    # @method_decorator(permission_required("dma.change_stations"))
    def dispatch(self, *args, **kwargs):
        # self.role_id = kwargs["pk"]
        return super(DistrictAssignStationView, self).dispatch(*args, **kwargs)

    def test_func(self):
        if self.request.user.has_menu_permission_edit('dmamanager_basemanager'):
            return True
        return False

    def handle_no_permission(self):
        data = {
                "mheader": "修改用户",
                "err_msg":"您没有权限进行操作，请联系管理员."
                    
            }
        # return HttpResponse(json.dumps(err_data))
        return render(self.request,"dmam/permission_error.html",data)

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        print("dma station assign here?:",self.request.POST)
        # print(form)
        # do something
        stationassign = form.cleaned_data.get("stationassign")
        jd = json.loads(stationassign)

        print(jd)
        self.object = self.get_object()
        for d in jd:
            print(d["station_id"],d["dma_name"],d["station_name"],d["metertype"])
            station_id = int(d["station_id"])
            metertype = d["metertype"]
            station = Station.objects.get(pk=station_id)
            station.dmaid = self.object
            station.dmametertype = metertype
            station.save()
        
        data = {
                "success": 1,
                "obj":{"flag":1}
            }
        return HttpResponse(json.dumps(data)) #JsonResponse(data)        

        # return super(DistrictAssignStationView,self).form_valid(form)

    def get_object(self):
        print(self.kwargs)
        return DMABaseinfo.objects.get(pk=int(self.kwargs["pk"]))
        
    def get_context_data(self, *args, **kwargs):
        context = super(DistrictAssignStationView, self).get_context_data(*args, **kwargs)
        

        self.object = self.get_object()  # user_organ.dma.all().first()
        
        context["dma_pk"] = self.object.pk
        context["dma_no"] = self.object.dma_no
        context["dma_name"] = self.object.dma_name
        context["dma_group"] = self.object.belongto.name

        #dma station
        dmastaions = self.object.station_set.all()

        data = []
        #dma分区的站点
        
        for s in dmastaions:
            data.append({
                "id":s.pk,
                "username":s.username,
                "pid":self.object.belongto.cid,
                "dmametertype":s.dmametertype
            })

        dmastation_list = {
            "obj":{
                    "dmastationlist":data
            }
        }

        context["dmastation_list"] = json.dumps(dmastation_list)
        

        return context  


def saveDmaStation(request):
    dma_pk = request.POST.get("dma_pk")
    dma = DMABaseinfo.objects.get(pk=int(dma_pk))
    stationassign = request.POST.get("stationassign")
    jd = json.loads(stationassign)

    
    dmastations = dma.station_set.all()
    print("dma stations:",dmastations)

    refresh_list = []
    # 更新dma分区站点信息，
    for d in jd:
        print(d["station_id"],d["dma_name"],d["station_name"],d["metertype"])
        station_id = int(d["station_id"])
        refresh_list.append(station_id)
        metertype = d["metertype"]
        station = Station.objects.get(pk=station_id)
        if station not in dmastations:
            station.dmaid.add(dma)

        station.dmametertype = metertype
        station.save()
    
    print("refresh_list:",refresh_list)
    # 删除不在更新列表里的已分配的站点
    for s in dmastations:
        if s.id not in refresh_list:
            dma.station_set.remove(s)

    data = {
            "success": 1,
            "obj":{"flag":1}
        }
    return HttpResponse(json.dumps(data)) #JsonResponse(data)   


def getdmastationsbyId(request):

    dma_pk = request.POST.get("dma_pk")
    dma = DMABaseinfo.objects.get(pk = int(dma_pk))

    #dma station
    dmastaions = dma.station_set.all()

    data = []
    #dma分区的站点
    
    for s in dmastaions:
        data.append({
            "id":s.pk,
            "username":s.username,
            "pid":dma.belongto.cid,
            "dmametertype":s.dmametertype
        })

    dmastation_list = {
        "obj":data,
        "success":True
    }

    return HttpResponse(json.dumps(dmastation_list)) 

"""
用水性质
"""

def findusertypeByusertype(request):
    print(request.POST)
    usertype = request.POST.get('type')
    flag = not WaterUserType.objects.filter(usertype=usertype).exists()

    return JsonResponse(flag, safe=False)

def findUsertypeCompare(request):
    print('findUsertypeCompare',request.POST)
    usertype = request.POST.get('usertype')
    updateuserType = request.POST.get("updateuserType")
    recomposeType = request.POST.get("recomposeType")
    print(usertype,updateuserType,recomposeType)

    tmp = WaterUserType.objects.filter(usertype=updateuserType)
    print('tmp:',tmp)
    flag = not WaterUserType.objects.filter(usertype=usertype).exists()

    return JsonResponse(flag, safe=False)

def findUsertypes(request):
    usertypes = WaterUserType.objects.all()
    data = []
    for ut in usertypes:
        data.append({
            "explains":ut.explains,
            "id":ut.pk,
            "userType":ut.usertype
            })
    operarions_list = {
        "exceptionDetailMsg":"",
        "msg":"",
        "obj":{
                "operation":data
        },
        "success":True
    }
   

    return JsonResponse(operarions_list)



def usertypeadd(request):
    if not request.user.has_menu_permission_edit('stationmanager_basemanager'):
        return HttpResponse(json.dumps({"success":0,"msg":"您没有权限进行操作，请联系管理员."}))

    print('usertypeadd:',request.POST)
    usertypeform = WaterUserTypeForm(request.POST or None)
    print('usertypeform',usertypeform)

    usertype = request.POST.get("usertype")
    explains = request.POST.get("explains")
    obj = WaterUserType.objects.create(
            usertype = usertype,
            explains = explains)

    if obj:
        flag = 1
    else:
        flag = 0

    return HttpResponse(json.dumps({"success":flag}))

def findUsertypeById(request):
    print(request.POST)
    tid = request.POST.get("id")
    tid = int(tid)
    ut = WaterUserType.objects.get(pk=tid)

    operarions_list = {
        "exceptionDetailMsg":"",
        "msg":"",
        "obj":{
                "operation":{
                    "explains":ut.explains,
                    "id":ut.pk,
                    "userType":ut.usertype}
        },
        "success":True
    }
   

    return JsonResponse(operarions_list)

def updateOperation(request):
    print('updateOperation:',request.POST)
    tid = request.POST.get("id")
    usertype = request.POST.get("userType")
    explains = request.POST.get("explains")
    tid = int(tid)
    ut = WaterUserType.objects.get(pk=tid)
    ut.usertype = usertype
    ut.explains = explains
    ut.save()

    return JsonResponse({"success":True})


def deleteOperation(request):
    tid = request.POST.get("id")
    tid = int(tid)
    ut = WaterUserType.objects.get(pk=tid)
    ut.delete()

    return JsonResponse({"success":True})

def deleteOperationMore(request):
    print("deleteOperationMore:",request.POST)
    deltems = request.POST.get("ids")
    deltems_list = deltems.split(',')
    print(deltems_list)
    for uid in deltems_list:
        if uid !='':
            u = WaterUserType.objects.get(id=int(uid))
            u.delete()
    return JsonResponse({"success":True})

def usertypeedit(request):
    pass


def usertypedeletemore(request):
    if not request.user.has_menu_permission_edit('stationmanager_basemanager'):
        return HttpResponse(json.dumps({"success":0,"msg":"您没有权限进行操作，请联系管理员."}))

    deltems = request.POST.get("deltems")
    deltems_list = deltems.split(';')

    for uid in deltems_list:
        u = User.objects.get(id=int(uid))
        # print('delete user ',u)
        #删除用户 并且删除用户在分组中的角色
        for g in u.groups.all():
            g.user_set.remove(u)
        u.delete()

    return HttpResponse(json.dumps({"success":1}))


def userdeletemore(request):
    # print('userdeletemore',request,request.POST)

    if not request.user.has_menu_permission_edit('dmamanager_basemanager'):
        return HttpResponse(json.dumps({"success":0,"msg":"您没有权限进行操作，请联系管理员."}))

    deltems = request.POST.get("deltems")
    deltems_list = deltems.split(';')

    for uid in deltems_list:
        u = User.objects.get(id=int(uid))
        # print('delete user ',u)
        #删除用户 并且删除用户在分组中的角色
        for g in u.groups.all():
            g.user_set.remove(u)
        u.delete()

    return HttpResponse(json.dumps({"success":1}))

"""
Assets comment deletion, manager
"""
class UsertypeDeleteView(AjaxableResponseMixin,UserPassesTestMixin,DeleteView):
    model = WaterUserType
    # template_name = "aidsbank/asset_comment_confirm_delete.html"

    def test_func(self):
        
        if self.request.user.has_menu_permission_edit('stationmanager_basemanager'):
            return True
        return False

    def handle_no_permission(self):
        data = {
                "success": 0,
                "msg":"您没有权限进行操作，请联系管理员."
                    
            }
        HttpResponse(json.dumps(data))
        # return render(self.request,"dmam/permission_error.html",data)

    def dispatch(self, *args, **kwargs):
        # self.comment_id = kwargs["pk"]

        print("user delete:",args,kwargs)
        
        return super(StationDeleteView, self).dispatch(*args, **kwargs)

    def get_object(self,*args, **kwargs):
        # print("delete objects:",self.kwargs,kwargs)
        return User.objects.get(pk=kwargs["pk"])

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        print("delete?",args,kwargs)
        self.object = self.get_object(*args,**kwargs)

        #delete user role in groups
        for g in self.object.groups.all():
            g.user_set.remove(self.object)

        self.object.delete()
        result = dict()
        # result["success"] = 1
        return HttpResponse(json.dumps({"success":1}))
        

class StationMangerView(LoginRequiredMixin,TemplateView):
    template_name = "dmam/stationlist.html"

    def get_context_data(self, *args, **kwargs):
        context = super(StationMangerView, self).get_context_data(*args, **kwargs)
        context["page_menu"] = "dma管理"
        # context["page_submenu"] = "组织和用户管理"
        context["page_title"] = "站点管理"

        # context["user_list"] = User.objects.all()
        

        return context  


"""
User add, manager
"""
class StationAddView(AjaxableResponseMixin,UserPassesTestMixin,CreateView):
    model = Station
    form_class = StationsForm
    template_name = "dmam/stationadd.html"
    success_url = reverse_lazy("dmam:stationsmanager")
    # permission_required = ('entm.rolemanager_perms_basemanager_edit', 'entm.dmamanager_perms_basemanager_edit')

    # @method_decorator(permission_required("dma.change_stations"))
    def dispatch(self, *args, **kwargs):
        #uuid is selectTreeIdAdd namely organizations uuid
        if self.request.method == 'GET':
            uuid = self.request.GET.get("uuid")
            kwargs["uuid"] = uuid

        if self.request.method == 'POST':
            uuid = self.request.POST.get("uuid")
            kwargs["uuid"] = uuid
        print("uuid:",kwargs.get('uuid'))
        return super(StationAddView, self).dispatch(*args, **kwargs)

    def test_func(self):
        if self.request.user.has_menu_permission_edit('stationmanager_basemanager'):
            return True
        return False

    def handle_no_permission(self):
        data = {
                "mheader": "增加用户",
                "err_msg":"您没有权限进行操作，请联系管理员."
                    
            }
        # return HttpResponse(json.dumps(err_data))
        return render(self.request,"dmam/permission_error.html",data)

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        
        # print(form)
        # do something
        user = self.request.user
        user_groupid = user.belongto.cid
        instance = form.save(commit=False)
        organ_name = self.request.POST.get('belongto')
        
        organization = Organizations.objects.get(name=organ_name)
        instance.belongto = organization
        
        serialnumber = self.request.POST.get("serialnumber")
        meter = Meter.objects.get(serialnumber=serialnumber)
        instance.meter = meter

        return super(StationAddView,self).form_valid(form)   

    def get_context_data(self, *args, **kwargs):
        context = super(StationAddView, self).get_context_data(*args, **kwargs)

        
        uuid = self.request.GET.get('uuid') or ''
        
        groupId = self.request.user.belongto.cid
        groupname = self.request.user.belongto.name
        if len(uuid) > 0:
            organ = Organizations.objects.get(uuid=uuid)
            groupId = organ.cid
            groupname = organ.name
        # else:
        #     user = self.request.user
        #     groupId = user.belongto.cid
        #     groupname = user.belongto.name
        
        context["groupId"] = groupId
        context["groupname"] = groupname

        

        return context  


"""
User edit, manager
"""
class StationEditView(AjaxableResponseMixin,UserPassesTestMixin,UpdateView):
    model = Station
    form_class = StationsEditForm
    template_name = "dmam/stationedit.html"
    success_url = reverse_lazy("dmam:stationsmanager")
    
    # @method_decorator(permission_required("dma.change_stations"))
    def dispatch(self, *args, **kwargs):
        # self.user_id = kwargs["pk"]
        return super(StationEditView, self).dispatch(*args, **kwargs)

    def get_object(self):
        return Station.objects.get(id=self.kwargs["pk"])

    def test_func(self):
        if self.request.user.has_menu_permission_edit('stationmanager_basemanager'):
            return True
        return False

    def handle_no_permission(self):
        data = {
                "mheader": "修改站点",
                "err_msg":"您没有权限进行操作，请联系管理员."
                    
            }
        # return HttpResponse(json.dumps(err_data))
        return render(self.request,"dmam/permission_error.html",data)

    def form_invalid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        print("user edit form_invalid:::")
        return super(StationEditView,self).form_invalid(form)

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        

        
        instance = form.save(commit=False)
        organ_name = self.request.POST.get('belongto')
        
        organization = Organizations.objects.get(name=organ_name)
        instance.belongto = organization
        
        serialnumber = self.request.POST.get("serialnumber")
        meter = Meter.objects.get(serialnumber=serialnumber)
        instance.meter = meter
        
        # instance.uuid=unique_uuid_generator(instance)
        return super(StationEditView,self).form_valid(form)
        # role_list = MyRoles.objects.get(id=self.role_id)
        # return HttpResponse(render_to_string("dma/role_manager.html", {"role_list":role_list}))

    # def get(self,request, *args, **kwargs):
    #     print("get::::",args,kwargs)
    #     form = super(StationEditView, self).get_form()
    #     print("edit form:",form)
    #     # Set initial values and custom widget
    #     initial_base = self.get_initial() #Retrieve initial data for the form. By default, returns a copy of initial.
    #     # initial_base["menu"] = Menu.objects.get(id=1)
    #     self.object = self.get_object()

    #     initial_base["belongto"] = self.object.belongto.name
    #     initial_base["serialnumber"] = self.object.meter.serialnumber
    #     initial_base["dn"] = self.object.meter.dn
    #     initial_base["meter"] = self.object.meter.serialnumber
    #     initial_base["simid"] = self.object.meter.simid
    #     form.initial = initial_base
        
    #     return render(request,self.template_name,
    #                   {"form":form,"object":self.object})

    # def get_context_data(self, **kwargs):
    #     context = super(UserEditView, self).get_context_data(**kwargs)
    #     context["page_title"] = "修改用户"
    #     return context



def userdeletemore(request):
    # print('userdeletemore',request,request.POST)

    if not request.user.has_menu_permission_edit('dmamanager_basemanager'):
        return HttpResponse(json.dumps({"success":0,"msg":"您没有权限进行操作，请联系管理员."}))

    deltems = request.POST.get("deltems")
    deltems_list = deltems.split(';')

    for uid in deltems_list:
        u = User.objects.get(id=int(uid))
        # print('delete user ',u)
        #删除用户 并且删除用户在分组中的角色
        for g in u.groups.all():
            g.user_set.remove(u)
        u.delete()

    return HttpResponse(json.dumps({"success":1}))

"""
Assets comment deletion, manager
"""
class StationDeleteView(AjaxableResponseMixin,UserPassesTestMixin,DeleteView):
    model = Station
    # template_name = "aidsbank/asset_comment_confirm_delete.html"

    def test_func(self):
        
        if self.request.user.has_menu_permission_edit('stationmanager_basemanager'):
            return True
        return False

    def handle_no_permission(self):
        data = {
                "success": 0,
                "msg":"您没有权限进行操作，请联系管理员."
                    
            }
        HttpResponse(json.dumps(data))
        # return render(self.request,"dmam/permission_error.html",data)

    def dispatch(self, *args, **kwargs):
        # self.comment_id = kwargs["pk"]

        print("user delete:",args,kwargs)
        
        return super(StationDeleteView, self).dispatch(*args, **kwargs)

    def get_object(self,*args, **kwargs):
        # print("delete objects:",self.kwargs,kwargs)
        return Station.objects.get(pk=kwargs["pk"])

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        print("delete?",args,kwargs)
        self.object = self.get_object(*args,**kwargs)

        # 删除抄表系统中对应的大表
        commaddr = self.object.commaddr
        bigm = Bigmeter.objects.filter(commaddr=commaddr)
        if bigm.exists():
            bigm.first().delete()

        self.object.delete()
        result = dict()
        # result["success"] = 1
        return HttpResponse(json.dumps({"success":1}))
        