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

from django.template.loader import render_to_string
from django.shortcuts import render,HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView,DeleteView,FormView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import admin
from django.contrib.auth.models import Permission

from django.urls import reverse_lazy
from .forms import OrganizationsAddForm,OrganizationsEditForm
from . models import Organizations
from accounts.models import User,MyRoles
from accounts.forms import RoleCreateForm,MyRolesForm,RegisterForm,UserDetailChangeForm

from .utils import unique_cid_generator

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


class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin,self).form_invalid(form)
        print('dasf:',form.cleaned_data.get('register_date'))
        err_str = ''
        for k,v in form.errors.items():
            print(k,v)
            err_str += v[0]
        if self.request.is_ajax():
            data = {
                'success': 1,
                'obj':{
                    'flag':0,
                    'errMsg':err_str
                    }
            }
            print(form.errors)
            return JsonResponse(data)
            # return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin,self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'success': True,
                'obj':{'flag':1}
            }
            return JsonResponse(data)
        else:
            return response

def choicePermissionTree(request):



    roleid = request.POST.get('roleId') or -1
    print(' get choicePermissionTree',roleid)

    if roleid < 0:
        return HttpResponse(json.dumps(PERMISSION_TREE))

    
    instance = MyRoles.objects.get(id=roleid)
    permissiontree = instance.permissionTree
    ctree = PERMISSION_TREE[:]

    print(permissiontree)
    
    if len(permissiontree) > 0:
        ptree = json.loads(permissiontree)
        

        for pt in ptree:
            nodeid = pt['id']
            node_edit = '{}_edit'.format(nodeid)
            p_edit = pt['edit']

            node = [n for n in ctree if n['id']==nodeid][0]
            if p_edit:
                node['checked'] = 'true'
                node_sub = [n for n in ctree if n['id']==node_edit][0]
                node_sub['checked'] = 'true'
            else:
                node['checked'] = 'true'
            


    # return JsonResponse(dicts,safe=False)
    return HttpResponse(json.dumps(ctree))

def oranizationtree(request):   
    organtree = []

    organs = Organizations.objects.all()
    for o in organs:
        organtree.append({
            'name':o.name,
            'id':o.cid,
            'pId':o.pId,
            'type':'group',
            'uuid':o.uuid
            })

    return HttpResponse(json.dumps(organtree)) 

def findOperations(request):

    operarions_list = {
        # "exceptionDetailMsg":'',
        # "msg":'',
        "obj":{
                "operation":[
                {"explains":"自来水公司","id":"waterworks","operationType":"自来水公司"},
                {"explains":"非自来水公司","id":"nonwaterworks","operationType":"非自来水公司"},
                
            ]
        },
        "success":True
    }
   

    return JsonResponse(operarions_list)
    

# def groupadd(request):
#     print(request)

#     return HttpResponse(json.dumps([{'ok':1}]))


"""
group add
"""
class UserGroupAddView(AjaxableResponseMixin,CreateView):
    model = Organizations
    template_name = 'entm/groupadd.html'
    form_class = OrganizationsAddForm
    success_url = reverse_lazy('entm:usermanager');

    # @method_decorator(permission_required('dma.change_stations'))
    def dispatch(self, *args, **kwargs):
        # print('dispatch',args,kwargs)
        if self.request.method == 'GET':
            cid = self.request.GET.get('id')
            pid = self.request.GET.get('pid')
            kwargs['cid'] = cid
            kwargs['pId'] = pid
        return super(UserGroupAddView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        # print('user group add here?:',self.request.POST)
        # print(form)
        # do something
        instance = form.save(commit=False)
        instance.is_org = True
        cid = self.request.POST.get('pId','oranization')
        
        instance.pId = cid
        instance.cid = unique_cid_generator(instance,new_cid=cid)
        


        return super(UserGroupAddView,self).form_valid(form)   

    # def get_context_data(self, *args, **kwargs):
    #     context = super(UserGroupAddView, self).get_context_data(*args, **kwargs)
    #     print(args,kwargs)
    #     return context

    # def get_form_kwargs(self, *args, **kwargs):
    #     print('get form kwargs',args,kwargs)
    #     form_kwargs = super(UserGroupAddView, self).get_form_kwargs(*args, **kwargs)
        
    #     return form_kwargs

    def get(self,request, *args, **kwargs):
        print('get::::',args,kwargs)
        form = super(UserGroupAddView, self).get_form()
        # Set initial values and custom widget
        initial_base = self.get_initial() #Retrieve initial data for the form. By default, returns a copy of initial.
        # initial_base['menu'] = Menu.objects.get(id=1)
        initial_base['cid'] = kwargs.get('cid')
        initial_base['pId'] = kwargs.get('pId')
        form.initial = initial_base
        # form.fields['cid'].value = kwargs.get('cid')
        # form.fields['pId'].value = kwargs.get('pid')
        # form.fields['name'].widget = forms.widgets.Textarea()
        # return response using standard render() method
        return render(request,self.template_name,
                      {'form':form,})

    
    # def post(self,request,*args,**kwargs):
    #     print('do you been here 123?')
    #     print (request.POST)
    #     print(kwargs)
        

    #     form = self.get_form()
        
            
        

    #     # return super(AssignRoleView,self).render_to_response(context)
    #     return redirect(reverse_lazy('entm:groupadd'))



"""
Group edit, manager
"""
class UserGroupEditView(AjaxableResponseMixin,UpdateView):
    model = Organizations
    form_class = OrganizationsEditForm
    template_name = 'entm/groupedit.html'
    success_url = reverse_lazy('entm:rolemanager');

    # @method_decorator(permission_required('dma.change_stations'))
    def dispatch(self, *args, **kwargs):
        # self.role_id = kwargs['pk']
        return super(UserGroupEditView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        print('group update here?:',self.request.POST)
        # print(form)
        # do something
        
                

        return super(UserGroupEditView,self).form_valid(form)

    def get_object(self):
        print(self.kwargs)
        return Organizations.objects.get(cid=self.kwargs['pId'])
        

"""
Group Detail, manager
"""
class UserGroupDetailView(DetailView):
    model = Organizations
    form_class = OrganizationsEditForm
    template_name = 'entm/groupdetail.html'
    # success_url = reverse_lazy('entm:rolemanager');

    # @method_decorator(permission_required('dma.change_stations'))
    def dispatch(self, *args, **kwargs):
        # self.role_id = kwargs['pk']
        return super(UserGroupDetailView, self).dispatch(*args, **kwargs)

    
    def get_object(self):
        print(self.kwargs)
        return Organizations.objects.get(cid=self.kwargs['pId'])

"""
Assets comment deletion, manager
"""
class UserGroupDeleteView(AjaxableResponseMixin,DeleteView):
    model = Organizations
    # template_name = 'aidsbank/asset_comment_confirm_delete.html'

    def dispatch(self, *args, **kwargs):
        # self.comment_id = kwargs['pk']

        
        print(self.request.POST)
        kwargs['pId'] = self.request.POST.get('pId')
        print('delete dispatch:',args,kwargs)
        return super(UserGroupDeleteView, self).dispatch(*args, **kwargs)

    def get_object(self,*args, **kwargs):
        print('delete objects:',self.kwargs,kwargs)
        return Organizations.objects.get(cid=kwargs['pId'])

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        print('delete?',args,kwargs)
        self.object = self.get_object(*args,**kwargs)
        self.object.delete()
        return JsonResponse({'success':True})
        
    

def rolelist(request):
    draw = 1
    length = 0
    start=0
    if request.method == 'GET':
        draw = int(request.GET.get('draw', None)[0])
        length = int(request.GET.get('length', None)[0])
        start = int(request.GET.get('start', None)[0])
        search_value = request.GET.get('search[value]', None)
        # order_column = request.GET.get('order[0][column]', None)[0]
        # order = request.GET.get('order[0][dir]', None)[0]

    if request.method == 'POST':
        draw = int(request.POST.get('draw', None)[0])
        length = int(request.POST.get('length', None)[0])
        start = int(request.POST.get('start', None)[0])
        pageSize = int(request.POST.get('pageSize', 10))
        search_value = request.POST.get('search[value]', None)
        # order_column = request.POST.get('order[0][column]', None)[0]
        # order = request.POST.get('order[0][dir]', None)[0]

    # print('get rolelist:',draw,length,start,search_value)
    rolel = MyRoles.objects.all()
    data = []
    for r in rolel:
        data.append({'id':r.pk,'name':r.name,'notes':r.notes})
    # json = serializers.serialize('json', rolel)
    recordsTotal = rolel.count()

    result = dict()
    result['records'] = data
    result['draw'] = draw
    result['success'] = 'true'
    result['pageSize'] = pageSize
    # result['totalPages'] = recordsTotal/pageSize
    result['recordsTotal'] = recordsTotal
    # result['recordsFiltered'] = music['count']
    
    return HttpResponse(json.dumps(result))
    # return JsonResponse([result],safe=False)


def userlist(request):
    print('userlist',request)
    draw = 1
    length = 0
    start=0
    if request.method == 'GET':
        draw = int(request.GET.get('draw', None)[0])
        length = int(request.GET.get('length', None)[0])
        start = int(request.GET.get('start', None)[0])
        search_value = request.GET.get('search[value]', None)
        # order_column = request.GET.get('order[0][column]', None)[0]
        # order = request.GET.get('order[0][dir]', None)[0]

    if request.method == 'POST':
        draw = int(request.POST.get('draw', None)[0])
        length = int(request.POST.get('length', None)[0])
        start = int(request.POST.get('start', None)[0])
        pageSize = int(request.POST.get('pageSize', 10))
        search_value = request.POST.get('search[value]', None)
        # order_column = request.POST.get('order[0][column]', None)[0]
        # order = request.POST.get('order[0][dir]', None)[0]

    # print('get rolelist:',draw,length,start,search_value)
    userl = User.objects.all()
    data = []
    for u in userl:
        data.append({
            'id':u.pk,
            'user_name':u.user_name,
            'real_name':u.real_name,
            'sex':u.sex,
            'phone_number':u.phone_number,
            'expire_date':u.expire_date,
            'groupName':u.belongto,
            'roleName':u.Role,
            'email':u.email,
        })
    # json = serializers.serialize('json', rolel)
    recordsTotal = userl.count()

    result = dict()
    result['records'] = data
    result['draw'] = draw
    result['success'] = 'true'
    result['pageSize'] = pageSize
    # result['totalPages'] = recordsTotal/pageSize
    result['recordsTotal'] = recordsTotal
    # result['recordsFiltered'] = music['count']
    
    return HttpResponse(json.dumps(result))
    # return JsonResponse([result],safe=False)


def useredit(request):
    print(request)

    return HttpResponse(json.dumps([{'ok':1}]))

def useradd(request):
    print(request)

    return HttpResponse(json.dumps([{'ok':1}]))    


def userdelete(request):
    print(request)

    return HttpResponse(json.dumps([{'ok':1}]))


def userdeletemore(request):
    print(request)

    return HttpResponse(json.dumps([{'ok':1}]))

def roleedit(request):
    print(request)

    return HttpResponse(json.dumps([{'ok':1}]))

# def roleadd(request):
#     print(request)

#     return HttpResponse(json.dumps([{'ok':1}]))    


def roledelete(request):
    print(request)

    return HttpResponse(json.dumps([{'ok':1}]))


def roledeletemore(request):
    print(request)

    return HttpResponse(json.dumps([{'ok':1}]))




# 角色管理
class RolesMangerView(TemplateView):
    template_name = 'entm/rolelist.html'

    def get_context_data(self, *args, **kwargs):
        context = super(RolesMangerView, self).get_context_data(*args, **kwargs)
        context['page_title'] = '角色管理'
        context['role_list'] = MyRoles.objects.all()

        return context  

    


"""
Roles creation, manager
"""
class RolesAddView(AjaxableResponseMixin,CreateView):
    model = MyRoles
    template_name = 'entm/roleadd.html'
    form_class = RoleCreateForm
    success_url = reverse_lazy('entm:rolemanager');

    # @method_decorator(permission_required('dma.change_stations'))
    def dispatch(self, *args, **kwargs):
        return super(RolesAddView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        print('role create here?:',self.request.POST)
        # print(form)
        # do something
        permissiontree = form.cleaned_data.get('permissionTree')
        ptree = json.loads(permissiontree)
        instance = form.save()
        # old_permissions = instance.permissions.all()
        # instance.permissions.clear()

        for pt in ptree:
            pname = pt['id']
            p_edit = pt['edit']
            perms = Permission.objects.get(codename=pname)
            
            if p_edit:
                node_edit = '{}_edit'.format(pname)
                perms_edit = Permission.objects.get(codename=node_edit)
                instance.permissions.add(perms)
                instance.permissions.add(perms_edit)


        return super(RolesAddView,self).form_valid(form)

    # def post(self,request,*args,**kwargs):
    #     print('do you been here 123?')
    #     print (request.POST)
    #     print(kwargs)

    #     form = self.get_form()
    #     instance = form.save(commit=False)
    #     print(form.cleaned_data['permissionTree'])
        
    #     form.save()
            
        

    #     # return super(AssignRoleView,self).render_to_response(context)
    #     return redirect(reverse_lazy('dma:roles_manager'))



"""
Roles edit, manager
"""
class RoleEditView(UpdateView):
    model = MyRoles
    form_class = MyRolesForm
    template_name = 'entm/roleedit.html'
    success_url = reverse_lazy('entm:rolemanager');

    # @method_decorator(permission_required('dma.change_stations'))
    def dispatch(self, *args, **kwargs):
        self.role_id = kwargs['pk']
        return super(RoleEditView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        print('role update here?:',self.request.POST)
        # print(form)
        # do something
        permissiontree = form.cleaned_data.get('permissionTree')
        ptree = json.loads(permissiontree)
        instance = self.object
        old_permissions = instance.permissions.all()
        instance.permissions.clear()

        for pt in ptree:
            pname = pt['id']
            p_edit = pt['edit']
            perms = Permission.objects.get(codename=pname)
            
            if p_edit:
                node_edit = '{}_edit'.format(pname)
                perms_edit = Permission.objects.get(codename=node_edit)
                instance.permissions.add(perms)
                instance.permissions.add(perms_edit)
                

        return super(RoleEditView,self).form_valid(form)
        

    # def post(self,request,*args,**kwargs):
    #     print('role update ?')
    #     print (request.POST)
    #     print(kwargs)

    #     form = self.get_form()
    #     if form.is_valid():
    #         print(form)
    #         print(form.cleaned_data['permissionTree'])
    #         # instance = form.save(commit=False)
    #         return self.form_valid(form)
            
    #     else:
    #         print(form.errors)
            
            
        

    #     # return super(AssignRoleView,self).render_to_response(context)
    #     return redirect(reverse_lazy('dma:roles_manager'))

    def get_context_data(self, **kwargs):
        context = super(RoleEditView, self).get_context_data(**kwargs)
        context['page_title'] = '修改角色'
        return context


"""
组织和用户管理
"""
class UserMangerView(TemplateView):
    template_name = 'entm/userlist.html'

    def get_context_data(self, *args, **kwargs):
        context = super(UserMangerView, self).get_context_data(*args, **kwargs)
        context['page_menu'] = '企业管理'
        # context['page_submenu'] = '组织和用户管理'
        context['page_title'] = '组织和用户管理'

        context['user_list'] = User.objects.all()
        

        return context  


"""
User add, manager
"""
class UserAddView(AjaxableResponseMixin,CreateView):
    model = User
    template_name = 'entm/useradd.html'
    form_class = RegisterForm
    success_url = reverse_lazy('dma:organ_users');

    # @method_decorator(permission_required('dma.change_stations'))
    def dispatch(self, *args, **kwargs):
        return super(UserAddView, self).dispatch(*args, **kwargs)


"""
User edit, manager
"""
class UserEditView(AjaxableResponseMixin,UpdateView):
    model = User
    form_class = UserDetailChangeForm
    template_name = 'dma/user_edit_manager.html'
    success_url = reverse_lazy('dma:organ_users')

    # @method_decorator(permission_required('dma.change_stations'))
    def dispatch(self, *args, **kwargs):
        self.user_id = kwargs['pk']
        return super(UserEditView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        form.save()
        return super(UserEditView,self).form_valid(form)
        # role_list = MyRoles.objects.get(id=self.role_id)
        # return HttpResponse(render_to_string('dma/role_manager.html', {'role_list':role_list}))

    def get_context_data(self, **kwargs):
        context = super(UserEditView, self).get_context_data(**kwargs)
        context['page_title'] = '修改用户'
        return context


class AssignRoleView(TemplateView):
    """docstring for AssignRoleView"""
    template_name = 'dma/assign_role.html'
        
    def get_context_data(self, **kwargs):
        context = super(AssignRoleView, self).get_context_data(**kwargs)
        context['page_title'] = '分配角色'
        context['role_list'] = MyRoles.objects.all()
        pk = kwargs['pk']
        context['object_id'] = pk
        context['user'] = User.objects.get(pk=pk)
        return context

    def post(self,request,*args,**kwargs):
        print (request.POST)
        print(kwargs)
        context = self.get_context_data(**kwargs)

        role = request.POST.get("checks[]")
        user = context['user']
        # user.Role = role
        group = MyRoles.objects.filter(name__iexact=role).first()
        print(group)
        user.groups.add(group)
        user.save()

        # return super(AssignRoleView,self).render_to_response(context)
        return redirect(reverse_lazy('dma:organ_users'))



class AuthStationView(TemplateView):
    """docstring for AuthStationView"""
    template_name = 'dma/auth_station.html'
        
    def get_context_data(self, **kwargs):
        context = super(AuthStationView, self).get_context_data(**kwargs)
        context['page_title'] = '分配角色'
        return context        

