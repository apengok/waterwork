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
from legacy.models import Bigmeter,District,Community,HdbFlowData,HdbFlowDataDay,HdbFlowDataMonth,HdbPressureData,Concentrator,MeterParameter
from dmam.models import WaterUserType,DMABaseinfo,DmaStation,Station,Meter,SimCard,VConcentrator
import os
from django.conf import settings

from waterwork.mixins import AjaxableResponseMixin
import logging

logger_info = logging.getLogger('info_logger')
logger_error = logging.getLogger('error_logger')



from .forms import MeterAddForm,MeterEditForm,SimCardAddForm,SimCardEditForm
# Create your views here.

# 表具管理/表具列表 dataTable
def meterlist(request):
    draw = 1
    length = 0
    start=0
    print('userlist:',request.user)
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

    print("get userlist:",draw,length,start,search_value)

    user = request.user
    organs = user.belongto

    meters = user.meter_list_queryset(simpleQueryParam).values("pk","serialnumber","simid__simcardNumber","version","dn",
        "metertype","belongto__name","mtype","manufacturer","protocol","R","q3","q1","check_cycle","state","station__username")
    # meters = Meter.objects.all()

    def m_info(m):
        
        return {
            "id":m["pk"],
            # "simid":m.simid,
            # "dn":m.dn,
            # "belongto":m.belongto.name,#current_user.belongto.name,
            # "metertype":m.metertype,
            "serialnumber":m["serialnumber"],
            "simid":m["simid__simcardNumber"] if m["simid__simcardNumber"] else "",
            "version":m["version"],
            "dn":m["dn"],
            "metertype":m["metertype"],
            "belongto":m["belongto__name"],
            "mtype":m["mtype"],
            "manufacturer":m["manufacturer"],
            "protocol":m["protocol"],
            "R":m["R"],
            "q3":m["q3"],
            "q1":m["q1"],
            "check_cycle":m["check_cycle"],
            "state":m["state"],
            "station":m["station__username"] #m.station_set.first().username if m.station_set.count() > 0 else ""
        }
    data = []

    for m in meters[start:start+length]:
        data.append(m_info(m))

    recordsTotal = meters.count()
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

    print(draw,pageSize,recordsTotal/pageSize,recordsTotal)
    
    return HttpResponse(json.dumps(result))


def repetition(request):
    serialnumber = request.POST.get("serialnumber")
    bflag = not Meter.objects.filter(serialnumber=serialnumber).exists()

    # return HttpResponse(json.dumps(bflag))
    return HttpResponse(json.dumps({"success":bflag}))

class MeterMangerView(LoginRequiredMixin,TemplateView):
    template_name = "devm/meterlist.html"

    def get_context_data(self, *args, **kwargs):
        context = super(MeterMangerView, self).get_context_data(*args, **kwargs)
        context["page_menu"] = "设备管理"
        # context["page_submenu"] = "组织和用户管理"
        context["page_title"] = "表具管理"

        # context["user_list"] = User.objects.all()
        

        return context  


"""
User add, manager
"""
class MeterAddView(AjaxableResponseMixin,UserPassesTestMixin,CreateView):
    model = Meter
    form_class = MeterAddForm
    template_name = "devm/meteradd.html"
    success_url = reverse_lazy("devm:metermanager")
    # permission_required = ('entm.rolemanager_perms_basemanager_edit', 'entm.dmamanager_perms_basemanager_edit')

    # @method_decorator(permission_required("dma.change_meters"))
    def dispatch(self, *args, **kwargs):
        #uuid is selectTreeIdAdd namely organizations uuid
        if self.request.method == 'GET':
            uuid = self.request.GET.get("uuid")
            kwargs["uuid"] = uuid

        if self.request.method == 'POST':
            uuid = self.request.POST.get("uuid")
            kwargs["uuid"] = uuid
        print("uuid:",kwargs.get('uuid'))
        return super(MeterAddView, self).dispatch(*args, **kwargs)

    def test_func(self):
        if self.request.user.has_menu_permission_edit('metermanager_devm'):
            return True
        return False

    def handle_no_permission(self):
        data = {
                "mheader": "增加用户",
                "err_msg":"您没有权限进行操作，请联系管理员."
                    
            }
        # return HttpResponse(json.dumps(err_data))
        return render(self.request,"entm/permission_error.html",data)

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        print("meter  add here?:",self.request.POST)
        print(self.kwargs,self.args)
        # print(form)
        # do something
        user = self.request.user
        user_groupid = user.belongto.cid
        instance = form.save(commit=False)
        organ_name = self.request.POST.get('belongto')
        
        organization = Organizations.objects.get(name=organ_name)
        instance.belongto = organization
        simcardNumber = self.request.POST.get('simid') or ''
        if SimCard.objects.filter(simcardNumber=simcardNumber).exists():
            instance.simid = SimCard.objects.get(simcardNumber=simcardNumber)
        # else:
        #     tmp=SimCard.objects.create(simcardNumber=simcardNumber,belongto=organization)
        #     instance.simid = tmp
        # instance.simid = SimCard.objects.get_or_create(simcardNumber=simcardNumber)
        # instance.simid = SimCard.objects.get_or_create(simcardNumber=simcardNumber)

        return super(MeterAddView,self).form_valid(form)   

    def get_context_data(self, *args, **kwargs):
        context = super(MeterAddView, self).get_context_data(*args, **kwargs)

        print('useradd context',args,kwargs,self.request)
        uuid = self.request.GET.get('uuid') or ''
        
        groupId = ''
        groupname = ''
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
class MeterEditView(AjaxableResponseMixin,UserPassesTestMixin,UpdateView):
    model = Meter
    form_class = MeterEditForm
    template_name = "devm/meteredit.html"
    success_url = reverse_lazy("devm:metermanager")
    
    # @method_decorator(permission_required("dma.change_meters"))
    def dispatch(self, *args, **kwargs):
        # self.user_id = kwargs["pk"]
        return super(MeterEditView, self).dispatch(*args, **kwargs)

    def get_object(self):
        return Meter.objects.get(id=self.kwargs["pk"])

    def test_func(self):
        if self.request.user.has_menu_permission_edit('metermanager_devm'):
            return True
        return False

    def handle_no_permission(self):
        data = {
                "mheader": "修改站点",
                "err_msg":"您没有权限进行操作，请联系管理员."
                    
            }
        # return HttpResponse(json.dumps(err_data))
        return render(self.request,"entm/permission_error.html",data)

    def form_invalid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        print("user edit form_invalid:::")
        return super(MeterEditView,self).form_invalid(form)

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        print(form)
        print(self.request.POST)

        
        instance = form.save(commit=False)
        organ_name = self.request.POST.get('belongto')
        
        organization = Organizations.objects.get(name=organ_name)
        instance.belongto = organization
        
        simcardNumber = self.request.POST.get('simid') or ''
        if SimCard.objects.filter(simcardNumber=simcardNumber).exists():
            instance.simid = SimCard.objects.get(simcardNumber=simcardNumber)
        
        
        # instance.uuid=unique_uuid_generator(instance)
        return super(MeterEditView,self).form_valid(form)
        # role_list = MyRoles.objects.get(id=self.role_id)
        # return HttpResponse(render_to_string("dma/role_manager.html", {"role_list":role_list}))

    # def get(self,request, *args, **kwargs):
    #     print("get::::",args,kwargs)
    #     form = super(MeterEditView, self).get_form()
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



def meterdeletemore(request):
    # print('userdeletemore',request,request.POST)

    if not request.user.has_menu_permission_edit('metermanager_devm'):
        return HttpResponse(json.dumps({"success":0,"msg":"您没有权限进行操作，请联系管理员."}))

    deltems = request.POST.get("deltems")
    print('deltems:',deltems)
    deltems_list = deltems.split(',')

    for uid in deltems_list:
        u = Meter.objects.get(id=int(uid))
        # print('delete user ',u)
        #删除用户 并且删除用户在分组中的角色
        
        u.delete()

    return HttpResponse(json.dumps({"success":1}))

"""
Assets comment deletion, manager
"""
class MeterDeleteView(AjaxableResponseMixin,UserPassesTestMixin,DeleteView):
    model = Meter
    # template_name = "aidsbank/asset_comment_confirm_delete.html"

    def test_func(self):
        
        if self.request.user.has_menu_permission_edit('metermanager_devm'):
            return True
        return False

    def handle_no_permission(self):
        data = {
                "success": 0,
                "msg":"您没有权限进行操作，请联系管理员."
                    
            }
        HttpResponse(json.dumps(data))
        # return render(self.request,"entm/permission_error.html",data)

    def dispatch(self, *args, **kwargs):
        # self.comment_id = kwargs["pk"]

        print("user delete:",args,kwargs)
        
        return super(MeterDeleteView, self).dispatch(*args, **kwargs)

    def get_object(self,*args, **kwargs):
        # print("delete objects:",self.kwargs,kwargs)
        return Meter.objects.get(pk=kwargs["pk"])

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        print("delete?",args,kwargs)
        self.object = self.get_object(*args,**kwargs)

        

        self.object.delete()
        result = dict()
        # result["success"] = 1
        return HttpResponse(json.dumps({"success":1}))
        



#simcard manager
def simcardlist(request):
    draw = 1
    length = 0
    start=0
    print('userlist:',request.user)
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

    print("get simcardlist:",draw,length,start,search_value)
    import time
    t1=time.time()
    user = request.user
    organs = user.belongto

    simcards = user.simcard_list_queryset(simpleQueryParam).values("pk","simcardNumber","isStart","iccid","imei","imsi","belongto__name",
        "operator","simFlow","openCardTime","endTime","remark","create_date","update_date","meter__serialnumber","meter__station__username")
    # simcards = SimCard.objects.all()

    def m_info(s):

        #关联表具
        # s_m = ""
        # s_m_t = ""
        # related = "" #是否关联了表具
        # if s.meter.count() > 0:
        #     m = s.meter.first()
        #     s_m = m.serialnumber
        # else:
        #     m = ""

        # #关联站点，站点由表具关联，所以取表具关联的站点
        # if m != "":
        #     if m.station_set.count() > 0:
        #         t = m.station_set.first()
        #         s_m_t = t.username
        #     else:
        #         t = ""
        
        return {
            "id":s["pk"],
            "simcardNumber":s["simcardNumber"],
            "isStart":s["isStart"],
            "iccid":s["iccid"],
            "imei":s["imei"],
            "imsi":s["imsi"],
            "belongto":s["belongto__name"],
            "operator":s["operator"],
            "simFlow":s["simFlow"],
            "openCardTime":s["openCardTime"],
            "endTime":s["endTime"],
            "remark":s["remark"],
            "createDataTime":s["create_date"].strftime("%Y-%m-%d %H:%M:%S"),
            "updateDataTime":s["update_date"].strftime("%Y-%m-%d %H:%M:%S"),
            "meter":s["meter__serialnumber"],
            "station": s["meter__station__username"]
        }
    data = []

    for m in simcards[start:start+length]:
        data.append(m_info(m))

    recordsTotal = simcards.count()
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

    print(draw,pageSize,recordsTotal/pageSize,recordsTotal)
    print("simcard list time elapsed ",time.time()-t1)
    return HttpResponse(json.dumps(result))

def releaseRelate(request):
    sid = request.POST.get("sid")
    sim = SimCard.objects.get(pk=int(sid))

    sim.meter.clear()
    # sim.meter.simid = None
    return HttpResponse(json.dumps(True))

def getSimRelated(request):
    simcardNumber = request.POST.get("simcardNumber")
    bflag = not SimCard.objects.filter(simcardNumber=simcardNumber).exists()

    return HttpResponse(json.dumps(bflag))

def simcard_repetition(request):
    simcardNumber = request.POST.get("simcardNumber")
    bflag = not SimCard.objects.filter(simcardNumber=simcardNumber).exists()

    return HttpResponse(json.dumps(bflag))
    # return HttpResponse(json.dumps({"success":bflag}))

class SimCardMangerView(LoginRequiredMixin,TemplateView):
    template_name = "devm/simcardlist.html"

    def get_context_data(self, *args, **kwargs):
        context = super(SimCardMangerView, self).get_context_data(*args, **kwargs)
        context["page_menu"] = "设备管理"
        # context["page_submenu"] = "组织和用户管理"
        context["page_title"] = "SIM卡管理"

        # context["user_list"] = User.objects.all()
        

        return context  


"""
User add, manager
"""
class SimCardAddView(AjaxableResponseMixin,UserPassesTestMixin,CreateView):
    model = SimCard
    form_class = SimCardAddForm
    template_name = "devm/simcardadd.html"
    success_url = reverse_lazy("devm:simcardmanager")
    # permission_required = ('entm.rolemanager_perms_basemanager_edit', 'entm.dmamanager_perms_basemanager_edit')

    # @method_decorator(permission_required("dma.change_simcards"))
    def dispatch(self, *args, **kwargs):
        #uuid is selectTreeIdAdd namely organizations uuid
        if self.request.method == 'GET':
            uuid = self.request.GET.get("uuid")
            kwargs["uuid"] = uuid

        if self.request.method == 'POST':
            uuid = self.request.POST.get("uuid")
            kwargs["uuid"] = uuid
        print("uuid:",kwargs.get('uuid'))
        return super(SimCardAddView, self).dispatch(*args, **kwargs)

    def test_func(self):
        if self.request.user.has_menu_permission_edit('simcardmanager_devm'):
            return True
        return False

    def handle_no_permission(self):
        data = {
                "mheader": "增加用户",
                "err_msg":"您没有权限进行操作，请联系管理员."
                    
            }
        # return HttpResponse(json.dumps(err_data))
        return render(self.request,"entm/permission_error.html",data)

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        print("simcard  add here?:",self.request.POST)
        print(self.kwargs,self.args)
        # print(form)
        # do something
        user = self.request.user
        user_groupid = user.belongto.cid
        instance = form.save(commit=False)
        organ_name = self.request.POST.get('belongto')
        
        organization = Organizations.objects.get(name=organ_name)
        instance.belongto = organization
        
        

        return super(SimCardAddView,self).form_valid(form)   

    def get_context_data(self, *args, **kwargs):
        context = super(SimCardAddView, self).get_context_data(*args, **kwargs)

        print('useradd context',args,kwargs,self.request)
        uuid = self.request.GET.get('uuid') or ''
        
        groupId = ''
        groupname = ''
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
class SimCardEditView(AjaxableResponseMixin,UserPassesTestMixin,UpdateView):
    model = SimCard
    form_class = SimCardEditForm
    template_name = "devm/simcardedit.html"
    success_url = reverse_lazy("devm:simcardmanager")
    
    # @method_decorator(permission_required("dma.change_simcards"))
    def dispatch(self, *args, **kwargs):
        # self.user_id = kwargs["pk"]
        return super(SimCardEditView, self).dispatch(*args, **kwargs)

    def get_object(self):
        return SimCard.objects.get(id=self.kwargs["pk"])

    def test_func(self):
        if self.request.user.has_menu_permission_edit('simcardmanager_devm'):
            return True
        return False

    def handle_no_permission(self):
        data = {
                "mheader": "修改站点",
                "err_msg":"您没有权限进行操作，请联系管理员."
                    
            }
        # return HttpResponse(json.dumps(err_data))
        return render(self.request,"entm/permission_error.html",data)

    def form_invalid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        print("user edit form_invalid:::")
        return super(SimCardEditView,self).form_invalid(form)

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        print(form)
        print(self.request.POST)

        
        instance = form.save(commit=False)
        organ_name = self.request.POST.get('belongto')
        
        organization = Organizations.objects.get(name=organ_name)
        instance.belongto = organization
        
        
        
        # instance.uuid=unique_uuid_generator(instance)
        return super(SimCardEditView,self).form_valid(form)
        # role_list = MyRoles.objects.get(id=self.role_id)
        # return HttpResponse(render_to_string("dma/role_manager.html", {"role_list":role_list}))

    # def get(self,request, *args, **kwargs):
    #     print("get::::",args,kwargs)
    #     form = super(SimCardEditView, self).get_form()
    #     print("edit form:",form)
    #     # Set initial values and custom widget
    #     initial_base = self.get_initial() #Retrieve initial data for the form. By default, returns a copy of initial.
    #     # initial_base["menu"] = Menu.objects.get(id=1)
    #     self.object = self.get_object()

    #     initial_base["belongto"] = self.object.belongto.name
    #     initial_base["serialnumber"] = self.object.simcard.serialnumber
    #     initial_base["dn"] = self.object.simcard.dn
    #     initial_base["simcard"] = self.object.simcard.serialnumber
    #     initial_base["simid"] = self.object.simcard.simid
    #     form.initial = initial_base
        
    #     return render(request,self.template_name,
    #                   {"form":form,"object":self.object})

    # def get_context_data(self, **kwargs):
    #     context = super(UserEditView, self).get_context_data(**kwargs)
    #     context["page_title"] = "修改用户"
    #     return context



def simcarddeletemore(request):
    # print('userdeletemore',request,request.POST)

    if not request.user.has_menu_permission_edit('simcardmanager_devm'):
        return HttpResponse(json.dumps({"success":0,"msg":"您没有权限进行操作，请联系管理员."}))

    deltems = request.POST.get("deltems")
    deltems_list = deltems.split(',')

    for uid in deltems_list:
        u = SimCard.objects.get(id=int(uid))
        # print('delete user ',u)
        
        u.delete()

    return HttpResponse(json.dumps({"success":1}))

"""
Assets comment deletion, manager
"""
class SimCardDeleteView(AjaxableResponseMixin,UserPassesTestMixin,DeleteView):
    model = SimCard
    # template_name = "aidsbank/asset_comment_confirm_delete.html"

    def test_func(self):
        
        if self.request.user.has_menu_permission_edit('simcardmanager_devm'):
            return True
        return False

    def handle_no_permission(self):
        data = {
                "success": 0,
                "msg":"您没有权限进行操作，请联系管理员."
                    
            }
        HttpResponse(json.dumps(data))
        # return render(self.request,"entm/permission_error.html",data)

    def dispatch(self, *args, **kwargs):
        # self.comment_id = kwargs["pk"]

        print("user delete:",args,kwargs)
        
        return super(SimCardDeleteView, self).dispatch(*args, **kwargs)

    def get_object(self,*args, **kwargs):
        # print("delete objects:",self.kwargs,kwargs)
        return SimCard.objects.get(pk=kwargs["pk"])

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        print("delete?",args,kwargs)
        self.object = self.get_object(*args,**kwargs)

        

        self.object.delete()
        result = dict()
        # result["success"] = 1
        return HttpResponse(json.dumps({"success":1}))


def getSimcardSelect(request):
    # meters = Meter.objects.all()
    simcards = request.user.simcard_list_queryset('')

    def m_info(m):
        
        return {
            "id":m.pk,
            # "simid":m.simid,
            # "dn":m.dn,
            # "belongto":m.belongto.name,#current_user.belongto.name,
            # "metertype":m.metertype,
            "name":m.simcardNumber,
            
        }
    data = []

    for m in simcards:
        if m.meter.count() == 0:
            data.append(m_info(m))

    operarions_list = {
        "exceptionDetailMsg":"null",
        "msg":None,
        "obj":data,
        "success":True
    }
   
    # print(operarions_list)
    return JsonResponse(operarions_list)



def getMeterSelect(request):
    # meters = Meter.objects.all()
    meters = request.user.meter_list_queryset('')

    def m_info(m):
        
        return {
            "id":m.pk,
            "name":m.serialnumber,
            
        }
    data = []

    for m in meters:
        if m.station_set.count() == 0:    #len(m.serialnumber) > 2
            data.append(m_info(m))

    operarions_list = {
        "exceptionDetailMsg":"null",
        "msg":None,
        "obj":data,
        "success":True
    }
   
    # print(operarions_list)
    return JsonResponse(operarions_list)


class PressureMangerView(LoginRequiredMixin,TemplateView):
    template_name = "devm/pressuremanager.html"

    def get_context_data(self, *args, **kwargs):
        context = super(PressureMangerView, self).get_context_data(*args, **kwargs)
        context["page_title"] = "压力管理"
        context["page_menu"] = "设备管理"
        
        return context  


class FireboltMangerView(LoginRequiredMixin,TemplateView):
    template_name = "devm/fireboltmanager.html"

    def get_context_data(self, *args, **kwargs):
        context = super(FireboltMangerView, self).get_context_data(*args, **kwargs)
        context["page_title"] = "消防栓管理"
        context["page_menu"] = "设备管理"
        
        return context  


class ConcentratorMangerView(LoginRequiredMixin,TemplateView):
    template_name = "devm/concentratormanager.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ConcentratorMangerView, self).get_context_data(*args, **kwargs)
        context["page_title"] = "集中器管理"
        context["page_menu"] = "设备管理"
        
        return context  


def concentratorlist(request):
    draw = 1
    length = 0
    start=0
    print('userlist:',request.user)
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

    print("get userlist:",draw,length,start,search_value)

    user = request.user
    organs = user.belongto

    # meters = user.meter_list_queryset(simpleQueryParam)
    meters = Concentrator.objects.all() #.filter(communityid=105)  #文欣苑105

    def m_info(m):
        commaddr = m.commaddr
        v=VConcentrator.objects.get(commaddr=commaddr)
        return {
            "id":m.pk,
            # "simid":m.simid,
            # "dn":m.dn,
            # "belongto":m.belongto.name,#current_user.belongto.name,
            # "metertype":m.metertype,
            "name":v.name,
            "belongto":v.belongto.name,
            "installationsite":m.installationsite,
            "manufacturer":m.manufacturer,
            "model":m.model,
            "madedate":m.madedate,
            "lng":m.lng,
            "lat":m.lat,
            "coortype":m.coortype,
            "commaddr":m.commaddr,
            "simid":m.simid,
            "gpflow":m.gpflow,
            "uplimitflow":m.uplimitflow,
            "monthdownflow":m.monthdownflow,
            "communityid":m.communityid,
            # "station":m.station_set.first().username if m.station_set.count() > 0 else ""
        }
    data = []

    for m in meters[start:start+length]:
        data.append(m_info(m))

    recordsTotal = len(meters)
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

    print(draw,pageSize,recordsTotal/pageSize,recordsTotal)
    
    return HttpResponse(json.dumps(result))

# class ParamsMangerView(LoginRequiredMixin,TemplateView):
class ParamsMangerView(LoginRequiredMixin,TemplateView):
    template_name = "devm/paramsmanager.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ParamsMangerView, self).get_context_data(*args, **kwargs)
        context["page_title"] = "参数指令"
        context["page_menu"] = "设备管理"
        
        return context  

# 指令参数列表
def commandlist(request):

    draw = 1
    length = 0
    start=0
    print('userlist:',request.user)
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
        sid = request.POST.get("sid")
        # print(request.POST.get("draw"))
        print("groupName",groupName)
        print("districtId:",districtId)
        # print("post simpleQueryParam",simpleQueryParam)

    data = []
    if sid != '':
        station = Station.objects.filter(pk=int(sid)).values("pk","meter__serialnumber","meter__simid__simcardNumber","username","belongto__name")
        
        
        
        data.append({
            "status":0,
            "commandType":"12",
            "sierialnumber":station.first()["meter__serialnumber"],
            "station_name":station.first()["username"],
            "simcardnumber":station.first()["meter__simid__simcardNumber"],
            "belongto":station.first()["belongto__name"],
            "sendparametertime":"",
            "readparametertime":"",
            "createDataTime":"",
            })

    

    # recordsTotal = 1
    recordsTotal = len(data)
    
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

    print(draw,pageSize,recordsTotal/pageSize,recordsTotal)
    
    return HttpResponse(json.dumps(result))


def saveCommand(request):

    print("saveCommand",request.POST)

    operarions_list = {
        "exceptionDetailMsg":"null",
        "msg":None,
        "obj":{"commandTypes":[]},
        "success":True
    }
   

    return JsonResponse(operarions_list)

# obslete
def getCommandTypes(request):

    sid = request.POST.get("sid") #station id

    operarions_list = {
        "exceptionDetailMsg":"null",
        "msg":None,
        "obj":{"commandTypes":[11]},
        "success":True
    }
   

    return JsonResponse(operarions_list)


def getCommandParam(request):
    print("getCommandParam",request.POST)
    sid = request.POST.get("sid")   #station pk
    commandType = request.POST.get("commandType")   #参数类型 11-通讯参数 12-终端参数 13-采集指令 14-基表参数
    isRefer = request.POST.get("isRefer")
    commaddr = request.POST.get("commaddr")

    # user = request.user

    # current meter
    station = Station.objects.filter(pk=int(sid)).values("pk","meter__serialnumber","meter__simid__simcardNumber","username")
    if station.exists():
        s = station.first()
        commaddr = s["meter__simid__simcardNumber"]
    
    commParam = {}
    terminalParam = {}
    aquiryParam = {}
    meterbaseParam = {}

    paramlist = MeterParameter.objects.filter(commaddr=commaddr).values()
    if paramlist.exists():
        param = paramlist.first()
    

    
        if commandType == "11":
            commParam = {
                "tcpresendcount":param["tcpresendcount"],
                "tcpresponovertime":param["tcpresponovertime"],
                "udpresendcount":param["udpresendcount"],
                "udpresponovertime":param["udpresponovertime"],
                "smsresendcount":param["smsresendcount"],
                "smsresponovertime":param["smsresponovertime"],
                "heartbeatperiod":param["heartbeatperiod"],
            }

        if commandType == "12":
            terminalParam = {
                "ipaddr":param["ipaddr"],
                "port":param["port"],
                "entrypoint":param["entrypoint"],
                
            }

        if commandType == "13":
            aquiryParam = {
                "updatastarttime":param["updatastarttime"],
                "updatamode":param["updatamode"],
                "collectperiod":param["collectperiod"],
                "updataperiod":param["updataperiod"],
                "updatatime1":param["updatatime1"],
                "updatatime2":param["updatatime2"],
                "updatatime3":param["updatatime3"],
                "updatatime4":param["updatatime4"],
            }

        if commandType == "14":
            meterbaseParam = {
                "dn":param["dn"],
                "liciperoid":param["liciperoid"],
                "maintaindate":param["maintaindate"],
                "transimeterfactor":param["transimeterfactor"],
                "biaofactor":param["biaofactor"],
                "manufacturercode":param["manufacturercode"],
                "issmallsignalcutpoint":param["issmallsignalcutpoint"],
                "smallsignalcutpoint":param["smallsignalcutpoint"],
                "isflowzerovalue":param["isflowzerovalue"],
                "flowzerovalue":param["flowzerovalue"],
                "pressurepermit":param["pressurepermit"],
                "flowdorient":param["flowdorient"],
                "plusaccumupreset":param["plusaccumupreset"],
            }
    
    operarions_list = {
        "exceptionDetailMsg":"null",
        "msg":None,
        "obj":{
            "sid":station.first()["pk"],
            "commaddr":station.first()["meter__simid__simcardNumber"],
            "serialnumber":station.first()["meter__serialnumber"],
            "station__username":station.first()["username"],
            # "referMeterList":meter_list,
            "commParam":commParam,
            "terminalParam":terminalParam,
            "aquiryParam":aquiryParam,
            "meterbaseParam":meterbaseParam,
            },
        "success":True
    }

    
    return JsonResponse(operarions_list)

# 指令参数设置的表具列表
def getReferCommand(request):
    print("getReferCommand",request.POST)
    sid = request.POST.get("sid") #station id

    operarions_list = {
        "exceptionDetailMsg":"null",
        "msg":None,
        "obj":{"referMeterList":[{
                    "updateDataTime":1541254778932,
                    "commandType":19,
                    "flag":1,
                    "editable":1,
                    "priority":1,
                    "enabled":1,
                    "vid":"d05821ab-5446-48f9-a7fe-a4e1f07ca7f0",
                    "createDataTime":1525928798000,
                    "sortOrder":1,
                    "id":"0da146c7-699c-443d-af11-5b8f6ddc4e35",
                    "createDataUsername":"13188906758",
                    "paramId":"e5cf0e5d-b7bd-4f8f-b5ba-2a14cba3a064,1f1e70de-308c-4bf8-b0c8-b959227e41aa",
                    "brand":"鲁A12345"
                },{
                    "updateDataTime":1541254778932,
                    "commandType":19,
                    "flag":1,
                    "editable":1,
                    "priority":1,
                    "enabled":1,
                    "vid":"d05821ab-5446-48f9-a7fe-a4e1f07ca7f0",
                    "createDataTime":1525928798000,
                    "sortOrder":1,
                    "id":"0da146c7-699c-443d-af11-5b8f6ddc4e35",
                    "createDataUsername":"13188906758",
                    "paramId":"e5cf0e5d-b7bd-4f8f-b5ba-2a14cba3a064,1f1e70de-308c-4bf8-b0c8-b959227e41aa",
                    "brand":"鲁A12346"
                }]},
        "success":True
    }
   

    return JsonResponse(operarions_list)