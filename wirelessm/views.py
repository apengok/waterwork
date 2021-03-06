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
from legacy.models import Bigmeter,District,Community,HdbFlowData,HdbFlowDataDay,HdbFlowDataMonth,HdbPressureData,HdbWatermeterDay,HdbWatermeterMonth
import os
from django.conf import settings

from waterwork.mixins import AjaxableResponseMixin
import logging

from dmam.models import VCommunity,VConcentrator,VWatermeter
from devm.forms import VCommunityAddForm,VWatermeterAddForm,VCommunityEditForm,VWatermeterEditForm

logger_info = logging.getLogger('info_logger')
logger_error = logging.getLogger('error_logger')




class WlquerydataView(LoginRequiredMixin,TemplateView):
    template_name = "wirelessm/wlquerydata.html"

    def get_context_data(self, *args, **kwargs):
        context = super(WlquerydataView, self).get_context_data(*args, **kwargs)
        context["page_title"] = "数据查询"
        context["page_menu"] = "无线抄表"
        
        return context  


def comunitiquery(request):
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
        selectCommunity = request.POST.get("selectCommunity")
        selectBuilding = request.POST.get("selectBuilding")
        selectTreeType = request.POST.get("selectTreeType")
        simpleQueryParam = request.POST.get("simpleQueryParam")
        print(request.POST.get("selectBuilding"))
        print("groupName",groupName)
        print("districtId:",districtId)
        # print("post simpleQueryParam",simpleQueryParam)

    print("get userlist:",draw,length,start,search_value)

    if selectCommunity == "" and selectBuilding == "":
        return HttpResponse(json.dumps({"success":"true","records":[]}))

    user = request.user
    organs = user.belongto
    today = datetime.datetime.today()
    ymon = today.strftime("%Y-%m")

    # v_community = VCommunity.objects.values_list("commutid","amrs_commutid")
    # v_community_dict = dict(v_community)

    watermeters = user.watermeter_list_queryset(simpleQueryParam).values("amrs_waterid","numbersth","buildingname","roomname","belongto__name","nodeaddr","wateraddr",
        "communityid__amrs_commutid","communityid__name")
    # meters = Watermeter.objects.all() #.filter(watermeterid=105)  #文欣苑105

    if selectCommunity != "":
        watermeters = [w for w in watermeters if selectCommunity == w["communityid__name"]]

    if selectBuilding != "":
        watermeters = [w for w in watermeters if selectBuilding == w["buildingname"]]

    def m_info(m):
        waterid = m["amrs_waterid"]
        communityid = m["communityid__amrs_commutid"]
        tmp =  {
            
            "numbersth":m["numbersth"],
            "buildingname":m["buildingname"],
            "roomname":m["roomname"],
            "belongto":m["belongto__name"],#current_user.belongto.name,
            "nodeaddr":m["nodeaddr"],
            "wateraddr":m["wateraddr"],
            "community":m["communityid__name"],
            
        }
        dailydata = HdbWatermeterDay.waterid_daily_use(waterid,communityid,ymon)
        
        for k,v in dailydata.items():
            d = "d"+k[-2:]
            tmp[d] = v

        return tmp
    data = []

    for m in watermeters:
        data.append(m_info(m))

    # recordsTotal = watermeters.count()
    recordsTotal = len(watermeters)
    
    result = dict()
    result["records"] = data[start:start+length]
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

class NeighborhoodusedaylyView(LoginRequiredMixin,TemplateView):
    template_name = "wirelessm/neighborhoodusedayly.html"

    def get_context_data(self, *args, **kwargs):
        context = super(NeighborhoodusedaylyView, self).get_context_data(*args, **kwargs)
        context["page_title"] = "小区日用水"
        context["page_menu"] = "无线抄表"
        
        return context  


class NeighborhoodusemonthlyView(LoginRequiredMixin,TemplateView):
    template_name = "wirelessm/neighborhoodusemonthly.html"

    def get_context_data(self, *args, **kwargs):
        context = super(NeighborhoodusemonthlyView, self).get_context_data(*args, **kwargs)
        context["page_title"] = "小区月用水"
        context["page_menu"] = "无线抄表"
        
        return context  


class NeighborhoodmeterMangerView(LoginRequiredMixin,TemplateView):
    template_name = "wirelessm/neighborhoodmetermanager.html"

    def get_context_data(self, *args, **kwargs):
        context = super(NeighborhoodmeterMangerView, self).get_context_data(*args, **kwargs)
        context["page_title"] = "户表管理"
        context["page_menu"] = "无线抄表"
        
        return context  



def watermeter_repetition(request):
    numbersth = request.POST.get("numbersth")
    buildingname = request.POST.get("buildingname")
    roomname = request.POST.get("roomname")

    bflag = not VWatermeter.objects.filter(numbersth=numbersth,buildingname=buildingname,roomname=roomname).exists()

    # return HttpResponse(json.dumps(bflag))
    return HttpResponse(json.dumps({"success":bflag}))


"""
User add, manager
"""
class WatermeterAddView(AjaxableResponseMixin,UserPassesTestMixin,CreateView):
    model = VWatermeter
    form_class = VWatermeterAddForm
    template_name = "wirelessm/watermeteradd.html"
    success_url = reverse_lazy("wirelessm:neighborhoodmetermanager")
    # permission_required = ('entm.rolemanager_perms_basemanager_edit', 'entm.wirelessmanager_perms_basemanager_edit')

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
        return super(WatermeterAddView, self).dispatch(*args, **kwargs)

    def test_func(self):
        if self.request.user.has_menu_permission_edit('neighborhoodmetermanager_devm'):
            return True
        return False

    def handle_no_permission(self):
        data = {
                "mheader": "新增集中器",
                "err_msg":"您没有权限进行操作，请联系管理员."
                    
            }
        # return HttpResponse(json.dumps(err_data))
        return render(self.request,"entm/permission_error.html",data)

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        print("watermeter  add here?:",self.request.POST)
        print(self.kwargs,self.args)
        # print(form)
        # do something
        user = self.request.user
        user_groupid = user.belongto.cid
        instance = form.save(commit=False)
        # organ_name = self.request.POST.get('belongto')
        
        # organization = Organizations.objects.get(name=organ_name)
        communityname = self.request.POST.get("communityid")
        community = VCommunity.objects.get(name=communityname)
        instance.communityid = community
        instance.belongto = community.belongto


        instance.save()
        concentrator = self.request.POST.get('concentrator') #集中器1名称
        
        vc1 = VConcentrator.objects.filter(name=concentrator)
        
        if vc1.exists():
            instance.concentrator = vc1.first()

        
        

        return super(WatermeterAddView,self).form_valid(form)   

    def get_context_data(self, *args, **kwargs):
        context = super(WatermeterAddView, self).get_context_data(*args, **kwargs)

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
class WatermeterEditView(AjaxableResponseMixin,UserPassesTestMixin,UpdateView):
    model = VWatermeter
    form_class = VWatermeterEditForm
    template_name = "wirelessm/watermeteredit.html"
    success_url = reverse_lazy("wirelessm:neighborhoodmetermanager")
    
    # @method_decorator(permission_required("dma.change_meters"))
    def dispatch(self, *args, **kwargs):
        # self.user_id = kwargs["pk"]
        return super(WatermeterEditView, self).dispatch(*args, **kwargs)

    def get_object(self):
        return VWatermeter.objects.get(id=self.kwargs["pk"])

    def test_func(self):
        if self.request.user.has_menu_permission_edit('neighborhoodmetermanager_devm'):
            return True
        return False

    def handle_no_permission(self):
        data = {
                "mheader": "修改集中器",
                "err_msg":"您没有权限进行操作，请联系管理员."
                    
            }
        # return HttpResponse(json.dumps(err_data))
        return render(self.request,"entm/permission_error.html",data)

    def form_invalid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        print("user edit form_invalid:::")
        return super(WatermeterEditView,self).form_invalid(form)

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        print(form)
        print(self.request.POST)

        user = self.request.user
        user_groupid = user.belongto.cid
        instance = form.save(commit=False)
        # organ_name = self.request.POST.get('belongto')
        
        # organization = Organizations.objects.get(name=organ_name)
        communityname = self.request.POST.get("communityid")
        community = VCommunity.objects.get(name=communityname)
        instance.communityid = community
        instance.belongto = community.belongto


        instance.save()
        concentrator = self.request.POST.get('concentrator') #集中器1名称
        
        vc1 = VConcentrator.objects.filter(name=concentrator)
        
        if vc1.exists():
            instance.concentrator = vc1.first()
        
        
        # 直接清除
        # instance.vconcentrators.clear()
# 
        
        
        # instance.uuid=unique_uuid_generator(instance)
        return super(WatermeterEditView,self).form_valid(form)
       


def watermeterdeletemore(request):
    # print('userdeletemore',request,request.POST)

    if not request.user.has_menu_permission_edit('metermanager_devm'):
        return HttpResponse(json.dumps({"success":0,"msg":"您没有权限进行操作，请联系管理员."}))

    deltems = request.POST.get("deltems")
    print('deltems:',deltems)
    deltems_list = deltems.split(',')

    for uid in deltems_list:
        u = VWatermeter.objects.get(id=int(uid))
        # print('delete user ',u)
        #删除用户 并且删除用户在分组中的角色
        waterid = u.waterid
        zncb_watermeter = Watermeter.objects.filter(id=waterid)
        if zncb_watermeter.exists():
            z = zncb_watermeter.first()
            z.delete()
        
        u.delete()

    return HttpResponse(json.dumps({"success":1}))

"""
Assets comment deletion, manager
"""
class WatermeterDeleteView(AjaxableResponseMixin,UserPassesTestMixin,DeleteView):
    model = VWatermeter
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
        
        return super(WatermeterDeleteView, self).dispatch(*args, **kwargs)

    def get_object(self,*args, **kwargs):
        # print("delete objects:",self.kwargs,kwargs)
        return VWatermeter.objects.get(pk=kwargs["pk"])

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        print("delete?",args,kwargs)
        self.object = self.get_object(*args,**kwargs)

        
        waterid = self.object.waterid
        
        
        # 同时删除zncb Watermeter记录
        zncb_watermeter = Watermeter.objects.filter(id=waterid)
        if zncb_watermeter.exists():
            z = zncb_watermeter.first()
            z.delete()
        self.object.delete()
        # result["success"] = 1
        return HttpResponse(json.dumps({"success":1}))
        

# 小区列表
def watermeterlist(request):
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
        selectCommunity = request.POST.get("selectCommunity")
        selectBuilding = request.POST.get("selectBuilding")
        selectTreeType = request.POST.get("selectTreeType")
        simpleQueryParam = request.POST.get("simpleQueryParam")
        print(request.POST.get("selectBuilding"))
        print("groupName",groupName)
        print("districtId:",districtId)
        # print("post simpleQueryParam",simpleQueryParam)

    print("get userlist:",draw,length,start,search_value)

    user = request.user
    organs = user.belongto

    watermeters = user.watermeter_list_queryset(simpleQueryParam).values("id","name","serialnumber","numbersth","buildingname","roomname","belongto__name","installationsite","username",
        "usertel","dn","manufacturer","madedate","ValveMeter","communityid__name","concentrator__name")
    # meters = Watermeter.objects.all() #.filter(watermeterid=105)  #文欣苑105

    if selectCommunity != "":
        watermeters = [w for w in watermeters if selectCommunity == w["communityid__name"]]

    if selectBuilding != "":
        watermeters = [w for w in watermeters if selectBuilding == w["buildingname"]]

    def m_info(m):
        
        return {
            "id":m["id"],
            "serialnumber":m["serialnumber"],
            "numbersth":m["numbersth"],
            "buildingname":m["buildingname"],
            "roomname":m["roomname"],
            "belongto":m["belongto__name"],#current_user.belongto.name,
            "dn":m["dn"],
            "name":m["name"],
            "concentrator__name":m["concentrator__name"],
            "installationsite":m["installationsite"],
            "communityid__name":m["communityid__name"],
            "username":m["username"],
            "usertel":m["usertel"],
            "manufacturer":m["manufacturer"],
            "madedate":m["madedate"],
            "ValveMeter":m["ValveMeter"],
            # "station":m.station_set.first().username if m.station_set.count() > 0 else ""
        }
    data = []

    for m in watermeters:
        print(m)
        data.append(m_info(m))

    # recordsTotal = watermeters.count()
    recordsTotal = len(watermeters)
    
    result = dict()
    result["records"] = data[start:start+length]
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


def neiborhooddailydata(request):
    '''
        无线抄表 日用水查询，查询小区某月每日用水量
    '''
    
    communityid = request.GET.get("communityid") #communityid is VCommunity's id
    # sTime = request.GET.get("sTime")[:10]
    # eTIme = request.GET.get("eTime")[:10]
    month = request.GET.get("month")
    flag = request.GET.get("flag")
    # print(sTime,eTIme)

    if month is None or month == '':
        month = today.strftime("%Y-%m")
    realcommutid = VCommunity.objects.get(id=communityid).amrs_commutid #get real id

    today = datetime.datetime.today()
    if flag == "-1":    #上月
        last_month = datetime.date.today().replace(day=1) - datetime.timedelta(days=1)
        mon_str = last_month.strftime("%Y-%m")
    elif flag == "0":
        mon_str = today.strftime("%Y-%m")
    else:
        mon_str = month
        # dailydata = HdbWatermeterDay.communityDailyRange(realcommutid,sTime,eTIme)
    
    # if flag == "1":
    #     monthdata = dailydata
    # else:
    monthdata = HdbWatermeterDay.communityDailydetail(realcommutid,mon_str)
    # dailydata = HdbWatermeterDay.communityDailyRange(realcommutid,sTime,eTIme)
    # print (monthdata)
    # print (dailydata)

    return HttpResponse(json.dumps({"success":1,"monthdata":monthdata}))



def neiborhoodmonthdata(request):
    # print(request.GET)
    communityid = request.GET.get("communityid") #communityid is VCommunity's id
    sMonth = request.GET.get("sMonth")
    eMonth = request.GET.get("eMonth")
    realcommutid = VCommunity.objects.get(id=communityid).amrs_commutid #get real id
    print(communityid,realcommutid)
    monthdata = HdbWatermeterMonth.community_range_use(realcommutid,sMonth,eMonth)

    return HttpResponse(json.dumps({"success":1,"monthdata":monthdata}))


    