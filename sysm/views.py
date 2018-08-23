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
from django.contrib.auth.mixins import PermissionRequiredMixin,UserPassesTestMixin

from accounts.models import User,MyRoles
from legacy.models import District,Bigmeter,HdbFlowData,HdbFlowDataDay,HdbFlowDataMonth,HdbPressureData,Metercomm,Meterprotocol
from dmam.models import DMABaseinfo,DmaStations,Station
from entm.models import Organizations
from .forms import logoPagesPhotoForm,MetercommForm

from django.core.files.storage import FileSystemStorage
# from django.core.urlresolvers import reverse_lazy
from waterwork.mixins import AjaxableResponseMixin


        
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




def getProtocolSelect(request):
    commtype = request.POST.get("commtype")
    protocls = Meterprotocol.objects.filter(commtype=int(commtype))

    print("getProtocolSelect",commtype,request.POST)
    
    data = []

    for p in protocls:
        print(p.name)
        data.append(p.protocol())

    protocls_list = {
        "exceptionDetailMsg":"null",
        "msg":None,
        "obj":data,
        "success":True
    }
   
    # print(operarions_list)
    return JsonResponse(protocls_list)


def getmetercommlist(request):
    
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
    metercomms = Metercomm.objects.all()

    
    data = []

    for m in metercomms[start:start+length]:
        data.append(m.mclist())
    
    # userl = current_user.user_list()

    # bigmeters = Bigmeter.objects.all()
    # dma_pk = request.POST.get("pk") or 4
    
    
    recordsTotal = len(metercomms)
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

class CommConfigView(LoginRequiredMixin,TemplateView):
    template_name = "sysm/commconfig.html"

    def get_context_data(self, *args, **kwargs):
        context = super(CommConfigView, self).get_context_data(*args, **kwargs)
        context["page_menu"] = "系统管理"
        # context["page_submenu"] = "组织和用户管理"
        context["page_title"] = "通讯管理"
        
        

        return context  


class CommConfigAddView(AjaxableResponseMixin,UserPassesTestMixin,CreateView):
    model = Metercomm
    template_name = "sysm/commconfigadd.html"
    form_class = MetercommForm
    success_url = reverse_lazy("sysm:commlist");

    # @method_decorator(permission_required("dma.change_stations"))
    def dispatch(self, *args, **kwargs):
        
        return super(CommConfigAddView, self).dispatch(*args, **kwargs)

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
        

        return super(CommConfigAddView,self).form_valid(form)   

class CommConfigEditView(AjaxableResponseMixin,UserPassesTestMixin,UpdateView):
    model = Metercomm
    form_class = MetercommForm
    template_name = "sysm/commconfigedit.html"
    success_url = reverse_lazy("sysm:commlist");

    # @method_decorator(permission_required("dma.change_stations"))
    def dispatch(self, *args, **kwargs):
        # self.role_id = kwargs["pk"]
        return super(CommConfigEditView, self).dispatch(*args, **kwargs)

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
        

        return super(CommConfigEditView,self).form_valid(form)

    def get_object(self):
        print(self.kwargs)
        return Metercomm.objects.get(pk=self.kwargs["pk"])
        


"""
Assets comment deletion, manager
"""
class CommConfigDeleteView(AjaxableResponseMixin,UserPassesTestMixin,DeleteView):
    model = Metercomm
    # template_name = "aidsbank/asset_comment_confirm_delete.html"

    def dispatch(self, *args, **kwargs):
        # self.comment_id = kwargs["pk"]

        return super(CommConfigDeleteView, self).dispatch(*args, **kwargs)

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
        return Metercomm.objects.get(pk=kwargs["pk"])

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        print("delete?",args,kwargs)
        self.object = self.get_object(*args,**kwargs)
            

        self.object.delete()
        return HttpResponse(json.dumps({"success":1}))
        # return JsonResponse("true", safe=False)