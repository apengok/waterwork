# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404,render,redirect
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.contrib import messages

import json
import random
from datetime import datetime

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
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from collections import OrderedDict
from accounts.models import User,MyRoles
from accounts.forms import RoleCreateForm,MyRolesForm,RegisterForm,UserDetailChangeForm

from .utils import unique_cid_generator,unique_uuid_generator,unique_rid_generator
from .forms import OrganizationsAddForm,OrganizationsEditForm
from . models import Organizations
# from django.core.urlresolvers import reverse_lazy


PERMISSION_TREE = [
        {"name":"数据监控","pId":"0","id":"perms_datamonitor"},
        {"name":"数据分析","pId":"0","id":"perms_datanalys"},
        {"name":"报警中心","pId":"0","id":"perms_alarmcenter"},
        {"name":"基础管理","pId":"0","id":"perms_basemanager"},
        {"name":"设备管理","pId":"0","id":"perms_devicemanager"},
        {"name":"企业管理","pId":"0","id":"perms_firmmanager"},
        {"name":"基准分析","pId":"0","id":"perms_basenalys"},
        {"name":"报表统计","pId":"0","id":"perms_reporttable"},
        {"name":"系统管理","pId":"0","id":"perms_systemconfig"},

        # 数据监控 sub
        {"name":"地图监控","pId":"perms_datamonitor","id":"mapmonitor_perms_datamonitor"},
        {"name":"可写","pId":"mapmonitor_perms_datamonitor","id":"mapmonitor_perms_datamonitor_edit","type":"premissionEdit"},
        {"name":"实时曲线","pId":"perms_datamonitor","id":"realcurlv_perms_datamonitor"},
        {"name":"可写","pId":"realcurlv_perms_datamonitor","id":"realcurlv_perms_datamonitor_edit","type":"premissionEdit"},
        {"name":"实时数据","pId":"perms_datamonitor","id":"realdata_perms_datamonitor"},
        {"name":"可写","pId":"realdata_perms_datamonitor","id":"realdata_perms_datamonitor_edit","type":"premissionEdit"},
        {"name":"DMA在线监控","pId":"perms_datamonitor","id":"dmaonline_perms_datamonitor"},
        {"name":"可写","pId":"dmaonline_perms_datamonitor","id":"dmaonline_perms_datamonitor_edit","type":"premissionEdit"},

        # 数据分析 sub
        {"name":"日用水分析","pId":"perms_datanalys","id":"dailyuse_perms_datanalys"},
        {"name":"可写","pId":"dailyuse_perms_datanalys","id":"dailyuse_perms_datanalys_edit","type":"premissionEdit"},
        {"name":"月用水分析","pId":"perms_datanalys","id":"monthlyuse_perms_datanalys"},
        {"name":"可写","pId":"monthlyuse_perms_datanalys","id":"monthlyuse_perms_datanalys_edit","type":"premissionEdit"},
        {"name":"DMA产销差分析","pId":"perms_datanalys","id":"dmacxc_perms_datanalys"},
        {"name":"可写","pId":"dmacxc_perms_datanalys","id":"dmacxc_perms_datanalys_edit","type":"premissionEdit"},
        {"name":"流量分析","pId":"perms_datanalys","id":"flownalys_perms_datanalys"},
        {"name":"可写","pId":"flownalys_perms_datanalys","id":"flownalys_perms_datanalys_edit","type":"premissionEdit"},
        {"name":"对比分析","pId":"perms_datanalys","id":"comparenalys_perms_datanalys"},
        {"name":"可写","pId":"comparenalys_perms_datanalys","id":"comparenalys_perms_datanalys_edit","type":"premissionEdit"},
        {"name":"配表分析","pId":"perms_datanalys","id":"peibiao_perms_datanalys"},
        {"name":"可写","pId":"peibiao_perms_datanalys","id":"peibiao_perms_datanalys_edit","type":"premissionEdit"},
        {"name":"原始数据","pId":"perms_datanalys","id":"rawdata_perms_datanalys"},
        {"name":"可写","pId":"rawdata_perms_datanalys","id":"rawdata_perms_datanalys_edit","type":"premissionEdit"},
        {"name":"夜间最小流量","pId":"perms_datanalys","id":"mnf_perms_datanalys"},
        {"name":"可写","pId":"mnf_perms_datanalys","id":"mnf_perms_datanalys_edit","type":"premissionEdit"},

        # 报警中心 sub
        {"name":"站点报警设置","pId":"perms_alarmcenter","id":"stationalarm_perms_alarmcenter"},
        {"name":"可写","pId":"stationalarm_perms_alarmcenter","id":"stationalarm_perms_alarmcenter_edit","type":"premissionEdit"},
        {"name":"DMA报警设置","pId":"perms_alarmcenter","id":"dmaalarm_perms_alarmcenter"},
        {"name":"可写","pId":"dmaalarm_perms_alarmcenter","id":"dmaalarm_perms_alarmcenter_edit","type":"premissionEdit"},
        {"name":"报警查询","pId":"perms_alarmcenter","id":"queryalarm_perms_alarmcenter"},
        {"name":"可写","pId":"queryalarm_perms_alarmcenter","id":"queryalarm_perms_alarmcenter_edit","type":"premissionEdit"},
        

        # 基础管理 sub
        {"name":"dma管理","pId":"perms_basemanager","id":"dmamanager_perms_basemanager"},
        {"name":"可写","pId":"dmamanager_perms_basemanager","id":"dmamanager_perms_basemanager_edit","type":"premissionEdit"},
        {"name":"站点管理","pId":"perms_basemanager","id":"stationmanager_perms_basemanager"},
        {"name":"可写","pId":"stationmanager_perms_basemanager","id":"stationmanager_perms_basemanager_edit","type":"premissionEdit"},

        # 企业管理 sub
        {"name":"角色管理","pId":"perms_firmmanager","id":"rolemanager_perms_firmmanager"},
        {"name":"可写","pId":"rolemanager_perms_firmmanager","id":"rolemanager_perms_firmmanager_edit","type":"premissionEdit"},
        {"name":"组织和用户管理","pId":"perms_firmmanager","id":"organusermanager_perms_basemanager"},
        {"name":"可写","pId":"organusermanager_perms_basemanager","id":"organusermanager_perms_basemanager_edit","type":"premissionEdit"},

        # 设备管理 sub
        {"name":"表具管理","pId":"perms_devicemanager","id":"meters_perms_devicemanager"},
        {"name":"可写","pId":"meters_perms_devicemanager","id":"meters_perms_devicemanager_edit","type":"premissionEdit"},
        {"name":"SIM卡管理","pId":"perms_devicemanager","id":"simcard_perms_devicemanager"},
        {"name":"可写","pId":"simcard_perms_devicemanager","id":"simcard_perms_devicemanager_edit","type":"premissionEdit"},
        {"name":"参数指令","pId":"perms_devicemanager","id":"params_perms_devicemanager"},
        {"name":"可写","pId":"params_perms_devicemanager","id":"params_perms_devicemanager_edit","type":"premissionEdit"},
        
        # 基准分析 sub
        {"name":"DMA基准分析","pId":"perms_basenalys","id":"dma_perms_basenalys"},
        {"name":"可写","pId":"dma_perms_basenalys","id":"dma_perms_basenalys_edit","type":"premissionEdit"},
        {"name":"最小流量分析","pId":"perms_basenalys","id":"mf_perms_basenalys"},
        {"name":"可写","pId":"mf_perms_basenalys","id":"mf_perms_basenalys_edit","type":"premissionEdit"},
        {"name":"日基准流量分析","pId":"perms_basenalys","id":"day_perms_basenalys"},
        {"name":"可写","pId":"day_perms_basenalys","id":"day_perms_basenalys_edit","type":"premissionEdit"},
        
        # 统计报表 sub
        {"name":"日志查询","pId":"perms_reporttable","id":"querylog_perms_reporttable"},
        {"name":"可写","pId":"querylog_perms_reporttable","id":"querylog_perms_reporttable_edit","type":"premissionEdit"},
        {"name":"报警报表","pId":"perms_reporttable","id":"alarm_perms_reporttable"},
        {"name":"可写","pId":"alarm_perms_reporttable","id":"alarm_perms_reporttable_edit","type":"premissionEdit"},
        {"name":"DMA统计报表","pId":"perms_reporttable","id":"dmastatics_perms_reporttable"},
        {"name":"可写","pId":"dmastatics_perms_reporttable","id":"dmastatics_perms_reporttable_edit","type":"premissionEdit"},
        {"name":"大用户报表","pId":"perms_reporttable","id":"biguser_perms_reporttable"},
        {"name":"可写","pId":"biguser_perms_reporttable","id":"biguser_perms_reporttable_edit","type":"premissionEdit"},
        {"name":"流量报表","pId":"perms_reporttable","id":"flows_perms_reporttable"},
        {"name":"可写","pId":"flows_perms_reporttable","id":"flows_perms_reporttable_edit","type":"premissionEdit"},
        {"name":"水量报表","pId":"perms_reporttable","id":"waters_perms_reporttable"},
        {"name":"可写","pId":"waters_perms_reporttable","id":"waters_perms_reporttable_edit","type":"premissionEdit"},
        {"name":"表务报表","pId":"perms_reporttable","id":"biaowu_perms_reporttable"},
        {"name":"可写","pId":"biaowu_perms_reporttable","id":"biaowu_perms_reporttable_edit","type":"premissionEdit"},
        {"name":"大数据报表","pId":"perms_reporttable","id":"bigdata_perms_reporttable"},
        {"name":"可写","pId":"bigdata_perms_reporttable","id":"bigdata_perms_reporttable_edit","type":"premissionEdit"},
        


        
        # 系统管理 sub
        {"name":"平台个性化管理","pId":"perms_systemconfig","id":"personality_perms_systemconfig"},
        {"name":"可写","pId":"personality_perms_systemconfig","id":"personality_perms_systemconfig_edit","type":"premissionEdit"},
        {"name":"系统设置","pId":"perms_systemconfig","id":"system_perms_systemconfig"},
        {"name":"可写","pId":"system_perms_systemconfig","id":"system_perms_systemconfig_edit","type":"premissionEdit"},
        {"name":"转发设置","pId":"perms_systemconfig","id":"retransit_perms_systemconfig"},
        {"name":"可写","pId":"retransit_perms_systemconfig","id":"retransit_perms_systemconfig_edit","type":"premissionEdit"},
        {"name":"图标配置","pId":"perms_systemconfig","id":"icons_perms_systemconfig"},
        {"name":"可写","pId":"icons_perms_systemconfig","id":"icons_perms_systemconfig_edit","type":"premissionEdit"},
        {"name":"日志查询","pId":"perms_systemconfig","id":"querylog_perms_systemconfig"},
        {"name":"可写","pId":"querylog_perms_systemconfig","id":"querylog_perms_systemconfig_edit","type":"premissionEdit"},
    ]


def error_404(request):
    return render(request,"404.html",{})

def error_500(request):
    return render(request,"500.html",{})

def i18n_javascript(request):
    return admin.site.i18n_javascript(request)


class StaticView(TemplateView):
    def get(self, request, page, *args, **kwargs):
        self.template_name = page
        print(page)
        response = super(StaticView, self).get(request, *args, **kwargs)
        try:
            return response.render()
        except TemplateDoesNotExist:
            raise Http404()


def room(request, room_name):
    return render(request, "entm/room.html", {
        "room_name_json": mark_safe(json.dumps(room_name))
    })

class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin,self).form_invalid(form)
        # print("dasf:",form.cleaned_data.get("register_date"))
        err_str = ""
        for k,v in form.errors.items():
            print(k,v)
            err_str += v[0]
        if self.request.is_ajax():
            data = {
                "success": 0,
                "obj":{
                    "flag":0,
                    "errMsg":err_str
                    }
            }
            print(form.errors)
            return HttpResponse(json.dumps(data)) #JsonResponse(data)
            # return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent"s form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin,self).form_valid(form)
        if self.request.is_ajax():
            data = {
                "success": 1,
                "obj":{"flag":1}
            }
            return HttpResponse(json.dumps(data)) #JsonResponse(data)
        else:
            return response



def recursive_node_to_dict(node,url_cat):
    result = {
        'id':node.pk,
        'name': node.name,
        'open':'true',
        'url':'/dma/{}/{}'.format(node.pk,url_cat),
        'target':'_self',
        'icon':"/static/virvo/images/站点管理/u842_1.png",
        'class':"J_menuItem",
    }
    
    children = [recursive_node_to_dict(c,url_cat) for c in node.get_children()]
    
    # get each node's station if exist
    if url_cat != '':
        try:
            sats = node.station.all()
            for s in sats:
                children.append({
                    'name':s.station_name,
                    'url':'/dma/{}/{}/{}'.format(node.pk,url_cat,s.id),
                    'target':'_self',
                    'icon':"/static/virvo/images/u3672.png",
                    # 'class':"J_menuItem",
                })
            # children.append({'name':})
        except:
            pass

    if children:
        result['children'] = children
    
    return result

def gettree(request):
    page_name = request.GET.get('page_name') or ''
    print(page_name)
    organs = Organization.objects.all()
    
    top_nodes = get_cached_trees(organs)

    dicts = []
    for n in top_nodes:
        dicts.append(recursive_node_to_dict(n,page_name))

    
    # print json.dumps(dicts, indent=4)

    virvo_tree = [{'name':'威尔沃','open':'true','children':dicts}]
    return JsonResponse({'trees':virvo_tree})                


choicetreedict=OrderedDict()
choicetreedict["datamonitor"]={
        "name":"数据监控",
        "submenu":[{
            "mapmonitor":{"name":"地图监控","sub":{"name":"可写"}},
            "realcurlv":{"name":"实时曲线","sub":{"name":"可写"}},
            "realdata":{"name":"实时数据","sub":{"name":"可写"}},
            "dmaonline":{"name":"DMA在线监控","sub":{"name":"可写"}},
        }],
    }


choicetreedict["datanalys"] = {
        "name":"数据分析",
        "submenu":[{
            "dailyuse":{"name":"日用水分析","sub":{"name":"可写"}},
            "monthlyuse":{"name":"月用水分析","sub":{"name":"可写"}},
            "dmacxc":{"name":"DMA产销差分析","sub":{"name":"可写"}},
            "flownalys":{"name":"流量分析","sub":{"name":"可写"}},
            "comparenalys":{"name":"对比分析","sub":{"name":"可写"}},
            "peibiao":{"name":"配表分析","sub":{"name":"可写"}},
            "rawdata":{"name":"原始数据","sub":{"name":"可写"}},
            "mnf":{"name":"夜间最小流量","sub":{"name":"可写"}},
        }],
    }
choicetreedict["alarmcenter"] = {
        "name":"报警中心",
        "submenu":[{
            "stationalarm":{"name":"站点报警设置","sub":{"name":"可写"}},
            "dmaalarm":{"name":"DMA报警设置","sub":{"name":"可写"}},
            "queryalarm":{"name":"报警查询","sub":{"name":"可写"}},
        }],
    }
choicetreedict["basemanager"] = {
        "name":"基础管理",
        "submenu":[{
            "dmamanager":{"name":"dma管理","sub":{"name":"可写"}},
            "stationmanager":{"name":"站点管理","sub":{"name":"可写"}},
        }],
    }
choicetreedict["devicemanager"] = {
        "name":"设备管理",
        "submenu":[{
            "meters":{"name":"表具管理","sub":{"name":"可写"}},
            "simcard":{"name":"SIM卡管理","sub":{"name":"可写"}},
            "params":{"name":"参数指令","sub":{"name":"可写"}},
        }],
    }
choicetreedict["firmmanager"] = {
        "name":"企业管理",
        "submenu":[{
            "rolemanager":{"name":"角色管理","sub":{"name":"可写"}},
            "organusermanager":{"name":"组织和用户管理","sub":{"name":"可写"}},
        }],
    }
choicetreedict["basenalys"] = {
        "name":"基准分析",
        "submenu":[{
            "dma":{"name":"DMA基准分析","sub":{"name":"可写"}},
            "mf":{"name":"最小流量分析","sub":{"name":"可写"}},
            "day":{"name":"日基准流量分析","sub":{"name":"可写"}},
        }],
    }
choicetreedict["reporttable"] = {
        "name":"报表统计",
        "submenu":[{
            "querylog":{"name":"日志查询","sub":{"name":"可写"}},
            "alarm":{"name":"报警报表","sub":{"name":"可写"}},
            "dmastatics":{"name":"DMA统计报表","sub":{"name":"可写"}},
            "biguser":{"name":"大用户报表","sub":{"name":"可写"}},
            "flows":{"name":"流量报表","sub":{"name":"可写"}},
            "waters":{"name":"水量报表","sub":{"name":"可写"}},
            "biaowu":{"name":"表务报表","sub":{"name":"可写"}},
            "bigdata":{"name":"大数据报表","sub":{"name":"可写"}},
        }],
    }
choicetreedict["systemconfig"] = {
        "name":"系统管理",
        "submenu":[{
            "personality":{"name":"平台个性化管理","sub":{"name":"可写"}},
            "system":{"name":"系统设置","sub":{"name":"可写"}},
            "retransit":{"name":"转发设置","sub":{"name":"可写"}},
            "icons":{"name":"图标配置","sub":{"name":"可写"}},
            "querylog":{"name":"日志查询","sub":{"name":"可写"}},
        }],
    }
    


def buildchoicetree(permstree=None):
    ctree = []
    # print("buildtree permm:",permstree,type(permstree))
    pt_dict = {}
    for pt in permstree:
        print(pt["id"],pt["edit"])
        pt_dict[pt["id"]] = pt["edit"]


    for key in choicetreedict.keys():
        pname = choicetreedict[key]["name"]
        pid = key
        

        tmp1 = {}
        tmp1["name"] = pname
        tmp1["pId"] = 0
        tmp1["id"] = pid
        if key in pt_dict.keys():
            tmp1["checked"] = "true"
        else:
            tmp1["chkDisabled"] = "true" 
        ctree.append(tmp1)
        
        submenu = choicetreedict[key]["submenu"][0]
        for sub_key in submenu.keys():
            name = submenu[sub_key]["name"]
            idstr = "{id}_{pid}".format(id=sub_key,pid=pid)
            cid = pid

            tmp2 = {}
            tmp2["name"] = name
            tmp2["pId"] = cid
            tmp2["id"] = idstr
            if idstr in pt_dict.keys():
                tmp2["checked"] = "true"
            else:
                tmp2["chkDisabled"] = "true" 
            ctree.append(tmp2)

        
            
            #可写
            edit_id = "{pid}_edit".format(pid=idstr)
            tmp3 = {}
            tmp3["name"] = "可写"
            tmp3["pId"] = idstr
            tmp3["id"] = edit_id
            tmp3["type"] = "premissionEdit"
            if idstr in pt_dict.keys() and pt_dict[idstr] == True:
                tmp3["checked"] = "true"
            else:
                tmp3["chkDisabled"] = "true" 
            ctree.append(tmp3)

            

    return ctree



def choicePermissionTree(request):

    
    rid = request.POST.get("roleId") or ''
    print(" get choicePermissionTree",rid)

    
    # print('buildtree:',buildtree)

    if len(rid) <= 0:
        user = request.user
        permissiontree = user.Role.permissionTree

    else:
        instance = MyRoles.objects.get(rid=rid)
        permissiontree = instance.permissionTree


    if len(permissiontree) > 0:
        ptree = json.loads(permissiontree)
        buildtree = buildchoicetree(ptree)
            


    # return JsonResponse(dicts,safe=False)

    return HttpResponse(json.dumps(buildtree))

def oranizationtree(request):   
    organtree = []

    organs = Organizations.objects.all()
    for o in organs:
        organtree.append({
            "name":o.name,
            "id":o.cid,
            "pId":o.pId,
            "type":"group",
            "uuid":o.uuid
            })

    
    result = dict()
    result["data"] = organtree
    
    # print(json.dumps(result))
    
    return HttpResponse(json.dumps(organtree))

    # return JsonResponse(organtree,safe=False)

def findOperations(request):

    operarions_list = {
        # "exceptionDetailMsg":"",
        # "msg":"",
        "obj":{
                "operation":[
                {"explains":"自来水公司","id":"waterworks","operationType":"自来水公司"},
                {"explains":"非自来水公司","id":"nonwaterworks","operationType":"非自来水公司"},
                
            ]
        },
        "success":True
    }
   

    return JsonResponse(operarions_list)
    

"""
group add
"""
class UserGroupAddView(AjaxableResponseMixin,UserPassesTestMixin,CreateView):
    model = Organizations
    template_name = "entm/groupadd.html"
    form_class = OrganizationsAddForm
    success_url = reverse_lazy("entm:usermanager");

    # @method_decorator(permission_required("dma.change_stations"))
    def dispatch(self, *args, **kwargs):
        # print("dispatch",args,kwargs)
        if self.request.method == "GET":
            cid = self.request.GET.get("id")
            pid = self.request.GET.get("pid")
            kwargs["cid"] = cid
            kwargs["pId"] = pid
        return super(UserGroupAddView, self).dispatch(*args, **kwargs)

    def test_func(self):
        user = self.request.user
        permissiontree = user.Role.permissionTree

        ptree = json.loads(permissiontree)
        pt_dict = {}
        for pt in ptree:
            print(pt["id"],pt["edit"])
            pt_dict[pt["id"]] = pt["edit"]

        if 'organusermanager_firmmanager' in pt_dict.keys() and pt_dict['organusermanager_firmmanager'] == True:
            return True
        return False

    def handle_no_permission(self):
        data = {
                "mheader": "修改用户",
                "err_msg":"您没有权限进行操作，请联系管理员."
                    
            }
        # return HttpResponse(json.dumps(err_data))
        return render(self.request,"entm/permission_error.html",data)

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        # print("user group add here?:",self.request.POST)
        # print(form)
        # do something
        instance = form.save(commit=False)
        instance.is_org = True
        cid = self.request.POST.get("pId","oranization")  #cid is parent orgnizations
        organizaiton_belong = Organizations.objects.get(cid=cid)
        instance.parent = organizaiton_belong
        instance.pId = cid
        instance.cid = unique_cid_generator(instance,new_cid=cid)

        instance.uuid = unique_uuid_generator(instance)
        


        return super(UserGroupAddView,self).form_valid(form)   


    def get(self,request, *args, **kwargs):
        print("get::::",args,kwargs)
        form = super(UserGroupAddView, self).get_form()
        # Set initial values and custom widget
        initial_base = self.get_initial() #Retrieve initial data for the form. By default, returns a copy of initial.
        # initial_base["menu"] = Menu.objects.get(id=1)
        initial_base["cid"] = kwargs.get("cid")
        initial_base["pId"] = kwargs.get("pId")
        form.initial = initial_base
        
        return render(request,self.template_name,
                      {"form":form,})


"""
Group edit, manager
"""
class UserGroupEditView(AjaxableResponseMixin,UserPassesTestMixin,UpdateView):
    model = Organizations
    form_class = OrganizationsEditForm
    template_name = "entm/groupedit.html"
    success_url = reverse_lazy("entm:rolemanager");

    # @method_decorator(permission_required("dma.change_stations"))
    def dispatch(self, *args, **kwargs):
        # self.role_id = kwargs["pk"]
        return super(UserGroupEditView, self).dispatch(*args, **kwargs)

    def test_func(self):
        user = self.request.user
        permissiontree = user.Role.permissionTree

        ptree = json.loads(permissiontree)
        pt_dict = {}
        for pt in ptree:
            print(pt["id"],pt["edit"])
            pt_dict[pt["id"]] = pt["edit"]

        if 'organusermanager_firmmanager' in pt_dict.keys() and pt_dict['organusermanager_firmmanager'] == True:
            return True
        return False

    def handle_no_permission(self):
        data = {
                "mheader": "修改用户",
                "err_msg":"您没有权限进行操作，请联系管理员."
                    
            }
        # return HttpResponse(json.dumps(err_data))
        return render(self.request,"entm/permission_error.html",data)

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        print("group update here?:",self.request.POST)
        # print(form)
        # do something
        
                

        return super(UserGroupEditView,self).form_valid(form)

    def get_object(self):
        print(self.kwargs)
        return Organizations.objects.get(cid=self.kwargs["pId"])
        

"""
Group Detail, manager
"""
class UserGroupDetailView(DetailView):
    model = Organizations
    form_class = OrganizationsEditForm
    template_name = "entm/groupdetail.html"
    # success_url = reverse_lazy("entm:rolemanager");

    # @method_decorator(permission_required("dma.change_stations"))
    def dispatch(self, *args, **kwargs):
        # self.role_id = kwargs["pk"]
        return super(UserGroupDetailView, self).dispatch(*args, **kwargs)

    
    def get_object(self):
        print(self.kwargs)
        return Organizations.objects.get(cid=self.kwargs["pId"])

"""
Assets comment deletion, manager
"""
class UserGroupDeleteView(AjaxableResponseMixin,DeleteView):
    model = Organizations
    # template_name = "aidsbank/asset_comment_confirm_delete.html"

    def dispatch(self, *args, **kwargs):
        # self.comment_id = kwargs["pk"]

        
        print(self.request.POST)
        kwargs["pId"] = self.request.POST.get("pId")
        print("delete dispatch:",args,kwargs)
        return super(UserGroupDeleteView, self).dispatch(*args, **kwargs)

    def get_object(self,*args, **kwargs):
        print("delete objects:",self.kwargs,kwargs)
        return Organizations.objects.get(cid=kwargs["pId"])

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        print("delete?",args,kwargs)
        self.object = self.get_object(*args,**kwargs)

        #删除组织 需要删除该组织的用户
        users = self.object.users.all()
        print('delete ',self.object,'and users:',users)
        for u in users:
            u.delete()
        self.object.delete()
        return JsonResponse({"success":True})
        
    

def rolelist(request):
    print('get rolelist:',request)
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

    if request.method == "POST":
        draw = int(request.POST.get("draw", 1))
        length = int(request.POST.get("length", 10))
        start = int(request.POST.get("start", 0))
        pageSize = int(request.POST.get("pageSize", 10))
        search_value = request.POST.get("search[value]", None)
        # order_column = request.POST.get("order[0][column]", None)[0]
        # order = request.POST.get("order[0][dir]", None)[0]

    # print("get rolelist:",draw,length,start,search_value)
    rolel = MyRoles.objects.all()
    data = []
    for r in rolel:
        data.append({"idstr":r.rid,"name":r.name,"notes":r.notes})
        print('idstr:',r.rid)
    # json = serializers.serialize("json", rolel)
    recordsTotal = rolel.count()

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
    # return JsonResponse([result],safe=False)


def userlist(request):
    # print("userlist",request.POST)
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
        print("simpleQueryParam",simpleQueryParam)

    if request.method == "POST":
        draw = int(request.POST.get("draw", 1))
        length = int(request.POST.get("length", 10))
        start = int(request.POST.get("start", 0))
        pageSize = int(request.POST.get("pageSize", 10))
        search_value = request.POST.get("search[value]", None)
        # order_column = request.POST.get("order[0][column]", None)[0]
        # order = request.POST.get("order[0][dir]", None)[0]
        groupName = request.POST.get("groupName")
        simpleQueryParam = request.POST.get("simpleQueryParam")
        print(request.POST.get("draw"))
        print("groupName",groupName)
        print("post simpleQueryParam",simpleQueryParam)

    # print("get rolelist:",draw,length,start,search_value)

    def u_info(u):
        rolename = u.Role.name if u.Role else ''
        return {
            "id":u.pk,
            "user_name":u.user_name,
            "real_name":u.real_name,
            "sex":u.sex,
            "phone_number":u.phone_number,
            "expire_date":u.expire_date,
            "groupName":u.belongto.name,
            "roleName":rolename,
            "email":u.email,
        }
    data = []
    #当前登录用户
    current_user = request.user
    #当前用户所属组织
    user_orgnization = current_user.belongto
    
    
    if groupName == "":
        #获取当前组织的所有用户
        userl = user_orgnization.users.all()
        for u in userl:
            data.append(u_info(u))
        #获取当前组织的下级组织所有用户
        for c in user_orgnization.get_children():
            for u in c.users.all():
                data.append(u_info(u))
    else:
        # entprise = Organizations.objects.get(cid=groupName)
        # userl = User.objects.filter(idstr__icontains=groupName)
        # userl = User.user_in_group.search(groupName)
        og = Organizations.objects.get(cid=groupName)
        print('og',og)
        if og:
            userl = og.users.all()
            for u in og.users.all():
                data.append(u_info(u))
        


    if simpleQueryParam != "":
        userl = userl.filter(real_name__icontains=simpleQueryParam)
    
    # data = []
    # for u in userl:
    #     # ros = [r.name for r in  u.groups.all()]
    #     rolename = u.Role.name if u.Role else ''
    #     data.append({
    #         "id":u.pk,
    #         "user_name":u.user_name,
    #         "real_name":u.real_name,
    #         "sex":u.sex,
    #         "phone_number":u.phone_number,
    #         "expire_date":u.expire_date,
    #         "groupName":u.belongto.name,
    #         "roleName":rolename,
    #         "email":u.email,
    #     })
    # json = serializers.serialize("json", rolel)
    recordsTotal = len(data)
    print('userlist draw:',draw)
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
    # return JsonResponse([result],safe=False)


#check if useradd name exists
def verifyUserName(request):
    print("verifyUserName:",request.POST)

    username = request.POST.get("userName")
    bflag = not User.objects.filter(user_name=username).exists()

    return HttpResponse(json.dumps({"success":bflag}))

def verification(request):
    print("verification:",request.POST,request.user)
    user = request.user
    user_expiredate = user.expire_date
    authorizationDate = request.POST.get("authorizationDate")
    a = datetime.strptime(user_expiredate,"%Y-%m-%d")
    b = datetime.strptime(authorizationDate,"%Y-%m-%d")
    bflag = b < a
    return HttpResponse(json.dumps({"success":bflag}))


def userdeletemore(request):
    print(request)

    return HttpResponse(json.dumps([{"ok":1}]))


def roledeletemore(request):
    print(request)

    return HttpResponse(json.dumps([{"ok":1}]))




# 角色管理
class RolesMangerView(LoginRequiredMixin,TemplateView):
    template_name = "entm/rolelist.html"

    def get_context_data(self, *args, **kwargs):
        context = super(RolesMangerView, self).get_context_data(*args, **kwargs)
        context["page_title"] = "角色管理"
        context["page_menu"] = "企业管理"
        
        return context  

    


"""
Roles creation, manager
"""
class RolesAddView(AjaxableResponseMixin,UserPassesTestMixin,CreateView):
    model = MyRoles
    template_name = "entm/roleadd.html"
    form_class = RoleCreateForm
    success_url = reverse_lazy("entm:rolemanager");

    # @method_decorator(permission_required("dma.change_stations"))
    def dispatch(self, *args, **kwargs):
        return super(RolesAddView, self).dispatch(*args, **kwargs)

    def test_func(self):
        user = self.request.user
        permissiontree = user.Role.permissionTree

        ptree = json.loads(permissiontree)
        pt_dict = {}
        for pt in ptree:
            print(pt["id"],pt["edit"])
            pt_dict[pt["id"]] = pt["edit"]

        if 'rolemanager_firmmanager' in pt_dict.keys() and pt_dict['rolemanager_firmmanager'] == True:
            return True
        return False

    def handle_no_permission(self):
        data = {
                "mheader": "添加角色",
                "err_msg":"您没有权限进行操作，请联系管理员."
                    
            }
        # return HttpResponse(json.dumps(err_data))
        return render(self.request,"entm/permission_error.html",data)

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        # print("role create here?:",self.request.POST)
        # print(form)
        # do something
        permissiontree = form.cleaned_data.get("permissionTree")
        ptree = json.loads(permissiontree)
        instance = form.save()
        instance.rid = unique_rid_generator(instance)
        user = self.request.user
        instance.uid = user.idstr
        instance.belongto = user.belongto
        

        # for pt in ptree:
        #     pname = pt["id"]
        #     p_edit = pt["edit"]
        #     perms = Permission.objects.get(codename=pname)
            
        #     if p_edit:
        #         node_edit = "{}_edit".format(pname)
        #         perms_edit = Permission.objects.get(codename=node_edit)
        #         instance.permissions.add(perms)
        #         instance.permissions.add(perms_edit)


        return super(RolesAddView,self).form_valid(form)


"""
Roles edit, manager
"""
class RoleEditView(AjaxableResponseMixin,UserPassesTestMixin,UpdateView):
    model = MyRoles
    form_class = MyRolesForm
    template_name = "entm/roleedit.html"
    success_url = reverse_lazy("entm:rolemanager");

    # @method_decorator(permission_required("dma.change_stations"))
    def dispatch(self, *args, **kwargs):
        print('roleedit dispatch:',self.request,args,kwargs)
        return super(RoleEditView, self).dispatch(*args, **kwargs)

    def test_func(self):
        user = self.request.user
        permissiontree = user.Role.permissionTree

        ptree = json.loads(permissiontree)
        pt_dict = {}
        for pt in ptree:
            print(pt["id"],pt["edit"])
            pt_dict[pt["id"]] = pt["edit"]

        if 'rolemanager_firmmanager' in pt_dict.keys() and pt_dict['rolemanager_firmmanager'] == True:
            return True
        return False

    def handle_no_permission(self):
        data = {
                "mheader": "修改用户",
                "err_msg":"您没有权限进行操作，请联系管理员."
                    
            }
        # return HttpResponse(json.dumps(err_data))
        return render(self.request,"entm/permission_error.html",data)

    def get_object(self,*args, **kwargs):
        print("role edit get object:",self.kwargs,kwargs)
        return MyRoles.objects.get(rid=self.kwargs["cn"])

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        # print("role edit here?:",self.request.POST)
        # print(form)
        # do something
        permissiontree = self.request.POST.get("permissionTree")
        # print('permissiontree:',permissiontree)
        print('user:',self.request.user.user_name)
        
        # ptree = json.loads(permissiontree)
        # instance = self.object
        # old_permissions = instance.permissions.all()
        # instance.permissions.clear()

        # for pt in ptree:
        #     pname = pt["id"]
        #     p_edit = pt["edit"]
        #     perms = Permission.objects.get(codename=pname)
            
        #     if p_edit:
        #         node_edit = "{}_edit".format(pname)
        #         perms_edit = Permission.objects.get(codename=node_edit)
        #         instance.permissions.add(perms)
        #         instance.permissions.add(perms_edit)
                

        return super(RoleEditView,self).form_valid(form)
        


"""
Assets comment deletion, manager
"""
class RoleDeleteView(AjaxableResponseMixin,DeleteView):
    model = MyRoles
    
    def dispatch(self, *args, **kwargs):
        print('role delete dispatch:',self.request,args,kwargs)

        print("role delete:",args,kwargs)
        
        return super(RoleDeleteView, self).dispatch(*args, **kwargs)

    def get_object(self,*args, **kwargs):
        print("delete objects:",self.kwargs,kwargs)
        return MyRoles.objects.get(rid=self.kwargs["cn"])

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        print("delete?",args,kwargs)
        self.object = self.get_object(*args,**kwargs)

        #delete user role in groups
        # for g in self.object.groups.all():
        #     g.user_set.remove(self.object)

        self.object.delete()
        result = dict()
        # result["success"] = 1
        return HttpResponse(json.dumps({"success":1}))


"""
组织和用户管理
"""
class UserMangerView(LoginRequiredMixin,TemplateView):
    template_name = "entm/userlist.html"

    def get_context_data(self, *args, **kwargs):
        context = super(UserMangerView, self).get_context_data(*args, **kwargs)
        context["page_menu"] = "企业管理"
        # context["page_submenu"] = "组织和用户管理"
        context["page_title"] = "组织和用户管理"

        # context["user_list"] = User.objects.all()
        

        return context  


"""
User add, manager
"""
class UserAddView(AjaxableResponseMixin,UserPassesTestMixin,CreateView):
    model = User
    template_name = "entm/useradd.html"
    form_class = RegisterForm
    success_url = reverse_lazy("entm:usermanager")
    # permission_required = ('entm.rolemanager_perms_firmmanager_edit', 'entm.organusermanager_perms_basemanager_edit')

    # @method_decorator(permission_required("dma.change_stations"))
    def dispatch(self, *args, **kwargs):
        if self.request.method == 'GET':
            uuid = self.request.GET.get("uuid")
            kwargs["uuid"] = uuid

        if self.request.method == 'POST':
            uuid = self.request.POST.get("uuid")
            kwargs["uuid"] = uuid
        print("uuid:",kwargs.get('uuid'))
        return super(UserAddView, self).dispatch(*args, **kwargs)

    def test_func(self):
        user = self.request.user
        permissiontree = user.Role.permissionTree

        ptree = json.loads(permissiontree)
        pt_dict = {}
        for pt in ptree:
            print(pt["id"],pt["edit"])
            pt_dict[pt["id"]] = pt["edit"]

        if 'organusermanager_firmmanager' in pt_dict.keys() and pt_dict['organusermanager_firmmanager'] == True:
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
        print("user  add here?:",self.request.POST)
        print(self.kwargs,self.args)
        print(form)
        # do something
        instance = form.save(commit=False)
        uid = self.request.POST.get('user_name')
        groupId = self.request.POST.get('groupId')
        organization = Organizations.objects.get(cid=groupId)
        instance.belongto = organization
        idstr = 'uid={uid},ou={groupid}'.format(
            uid=uid,
            groupid=groupId)
        print('idstr:',idstr)
        instance.idstr=groupId

        instance.uuid=unique_uuid_generator(instance)

        return super(UserAddView,self).form_valid(form)   

    def get_context_data(self, *args, **kwargs):
        context = super(UserAddView, self).get_context_data(*args, **kwargs)

        print('useradd context',args,kwargs,self.request)
        uuid = self.request.GET.get('uuid') or ''

        print('request user:',self.request.user)

        groupId = ''
        groupname = ''
        if len(uuid) > 0:
            organ = Organizations.objects.get(uuid=uuid)
            groupId = organ.cid
            groupname = organ.name
        
        context["groupId"] = groupId
        context["groupname"] = groupname
        

        return context  


"""
User edit, manager
"""
class UserEditView(AjaxableResponseMixin,UserPassesTestMixin,UpdateView):
    model = User
    form_class = UserDetailChangeForm
    template_name = "entm/useredit.html"
    success_url = reverse_lazy("entm:usermanager")
    # login_url = None
    # permission_denied_message = 'Not allowed edit user,please contact manager'
    # permission_required = ('entm.erwqrqwer', 'entm.qewrqerq')
    # permission_required = ('entm.rolemanager_perms_firmmanager_edit', 'entm.organusermanager_perms_basemanager_edit')

    # @method_decorator(permission_required("dma.change_stations"))
    def dispatch(self, *args, **kwargs):
        # self.user_id = kwargs["pk"]
        return super(UserEditView, self).dispatch(*args, **kwargs)

    def test_func(self):
        user = self.request.user
        permissiontree = user.Role.permissionTree

        ptree = json.loads(permissiontree)
        pt_dict = {}
        for pt in ptree:
            print(pt["id"],pt["edit"])
            pt_dict[pt["id"]] = pt["edit"]

        if 'organusermanager_firmmanager' in pt_dict.keys() and pt_dict['organusermanager_firmmanager'] == True:
            return True
        return False

    def handle_no_permission(self):
        data = {
                "mheader": "修改用户",
                "err_msg":"您没有权限进行操作，请联系管理员."
                    
            }
        # return HttpResponse(json.dumps(err_data))
        return render(self.request,"entm/permission_error.html",data)

    def form_invalid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        print("user edit form_invalid:::")
        return super(UserEditView,self).form_invalid(form)

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        print('useredit form:',form)
        instance = form.save()
        uid = form.cleaned_data.get('user_name')
        groupId = form.cleaned_data.get('groupIds')
        idstr = 'uid={uid},ou={groupid}'.format(
            uid=uid,
            groupid=groupId)
        print('idstr:',idstr)
        instance.idstr=groupId
        # instance.uuid=unique_uuid_generator(instance)
        return super(UserEditView,self).form_valid(form)
        # role_list = MyRoles.objects.get(id=self.role_id)
        # return HttpResponse(render_to_string("dma/role_manager.html", {"role_list":role_list}))

    # def get_context_data(self, **kwargs):
    #     context = super(UserEditView, self).get_context_data(**kwargs)
    #     context["page_title"] = "修改用户"
    #     return context


class AssignRoleView(TemplateView):
    """docstring for AssignRoleView"""
    template_name = "entm/assignrole.html"
        
    def get_context_data(self, **kwargs):
        context = super(AssignRoleView, self).get_context_data(**kwargs)
        context["page_title"] = "分配角色"
        context["role_list"] = MyRoles.objects.all()
        pk = kwargs["pk"]
        # context["object_id"] = pk
        context["object"] = self.get_object()
        return context

    def get_object(self):
        # print(self.kwargs)
        return User.objects.get(id=self.kwargs["pk"])

    def post(self,request,*args,**kwargs):
        print ("assinrole:",request.POST)
        print(kwargs)
        context = self.get_context_data(**kwargs)

        role_ids = request.POST.get("roleIds").split(",")
        print("role_ids:",role_ids)
        #只允许一个角色
        user = self.get_object()
        print("user:",user)

        rolename = ''
        for ri in role_ids:
            role = MyRoles.objects.get(id=int(ri))
            user.groups.add(role)
            print("role:",role)
            user.Role = role

            # permission_set = role.permissions.all()
            # user.user_permissions.add(permission_set)
        # user.Role = rolename
        
        user.save()

        data = {
                "msg": "分配完成",
                "obj":{"flag":1}
            }
        return JsonResponse(data)
        


class AssignStnView(TemplateView):
    """docstring for AssignRoleView"""
    template_name = "entm/assignstn.html"
        
    def get_context_data(self, **kwargs):
        context = super(AssignStnView, self).get_context_data(**kwargs)
        context["page_title"] = "分配角色"
        context["role_list"] = MyRoles.objects.all()
        pk = kwargs["pk"]
        context["object_id"] = pk
        context["user"] = User.objects.get(pk=pk)
        return context

    def get_object(self):
        # print(self.kwargs)
        return User.objects.get(id=self.kwargs["pk"])

    def post(self,request,*args,**kwargs):
        print (request.POST)
        print(kwargs)
        context = self.get_context_data(**kwargs)

        role = request.POST.get("checks[]")
        user = context["user"]
        # user.Role = role
        group = MyRoles.objects.filter(name__iexact=role).first()
        print(group)
        user.groups.add(group)
        user.save()

        data = {
                "msg": "分配完成",
                "obj":{"flag":1}
            }
        return JsonResponse(data)


"""
Assets comment deletion, manager
"""
class UserDeleteView(AjaxableResponseMixin,DeleteView):
    model = User
    # template_name = "aidsbank/asset_comment_confirm_delete.html"

    def dispatch(self, *args, **kwargs):
        # self.comment_id = kwargs["pk"]

        print("user delete:",args,kwargs)
        
        return super(UserDeleteView, self).dispatch(*args, **kwargs)

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
        

class AuthStationView(TemplateView):
    """docstring for AuthStationView"""
    template_name = "dma/auth_station.html"
        
    def get_context_data(self, **kwargs):
        context = super(AuthStationView, self).get_context_data(**kwargs)
        context["page_title"] = "分配角色"
        return context        

