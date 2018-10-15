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
import os
from django.conf import settings

from waterwork.mixins import AjaxableResponseMixin
import logging

logger_info = logging.getLogger('info_logger')
logger_error = logging.getLogger('error_logger')




class WlquerydataView(LoginRequiredMixin,TemplateView):
    template_name = "wirelessm/wlquerydata.html"

    def get_context_data(self, *args, **kwargs):
        context = super(WlquerydataView, self).get_context_data(*args, **kwargs)
        context["page_title"] = "数据查询"
        context["page_menu"] = "无线抄表"
        
        return context  


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
