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
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView,FormView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import admin
from django.contrib.auth.models import Permission

from django.urls import reverse_lazy
# from .forms import DMABaseinfoForm,CreateDMAForm,TestForm,StationsCreateManagerForm,StationsForm
# from . models import Organization,Stations,DMABaseinfo,Alarms,Organizations
from accounts.models import User,MyRoles
from accounts.forms import RoleCreateForm,MyRolesForm,RegisterForm,UserDetailChangeForm

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