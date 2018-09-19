# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView,DeleteView,FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin,UserPassesTestMixin

from waterwork.mixins import AjaxableResponseMixin

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

