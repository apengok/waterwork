# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView,DeleteView,FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin,UserPassesTestMixin

from waterwork.mixins import AjaxableResponseMixin
from legacy.models import District,Bigmeter,HdbFlowData,HdbFlowDataDay,HdbFlowDataMonth,HdbPressureData

# Create your views here.

class QuerylogView(LoginRequiredMixin,TemplateView):
    template_name = "reports/querylog.html"

    def get_context_data(self, *args, **kwargs):
        context = super(QuerylogView, self).get_context_data(*args, **kwargs)
        context["page_title"] = "日志查询"
        context["page_menu"] = "统计报表"
        
        return context  

class AlarmView(LoginRequiredMixin,TemplateView):
    template_name = "reports/alarm.html"

    def get_context_data(self, *args, **kwargs):
        context = super(AlarmView, self).get_context_data(*args, **kwargs)
        context["page_title"] = "报警报表"
        context["page_menu"] = "统计报表"
        
        return context  

class BiguserView(LoginRequiredMixin,TemplateView):
    template_name = "reports/biguser.html"

    def get_context_data(self, *args, **kwargs):
        context = super(BiguserView, self).get_context_data(*args, **kwargs)
        context["page_title"] = "大用户报表"
        context["page_menu"] = "统计报表"
        
        return context  

class DmastaticsView(LoginRequiredMixin,TemplateView):
    template_name = "reports/dmastatics.html"

    def get_context_data(self, *args, **kwargs):
        context = super(DmastaticsView, self).get_context_data(*args, **kwargs)
        context["page_title"] = "DMA报表"
        context["page_menu"] = "统计报表"

        bigmeter = Bigmeter.objects.first()
        context["station"] = bigmeter.username
        context["organ"] = "歙县自来水公司"
        
        return context  


class WenxinyuanView(TemplateView):
    template_name = "reports/wenxinyuan.html"

    def get_context_data(self, *args, **kwargs):
        context = super(WenxinyuanView, self).get_context_data(*args, **kwargs)
        context["page_title"] = "DMA报表"
        context["page_menu"] = "统计报表"

        bigmeter = Bigmeter.objects.first()
        context["station"] = bigmeter.username
        context["organ"] = "歙县自来水公司"
        
        return context  

class FlowsView(LoginRequiredMixin,TemplateView):
    template_name = "reports/flows.html"

    def get_context_data(self, *args, **kwargs):
        context = super(FlowsView, self).get_context_data(*args, **kwargs)
        context["page_title"] = "流量报表"
        context["page_menu"] = "统计报表"
        
        return context  

class WatersView(LoginRequiredMixin,TemplateView):
    template_name = "reports/waters.html"

    def get_context_data(self, *args, **kwargs):
        context = super(WatersView, self).get_context_data(*args, **kwargs)
        context["page_title"] = "水量报表"
        context["page_menu"] = "统计报表"
        
        return context  

class BiaowuView(LoginRequiredMixin,TemplateView):
    template_name = "reports/biaowu.html"

    def get_context_data(self, *args, **kwargs):
        context = super(BiaowuView, self).get_context_data(*args, **kwargs)
        context["page_title"] = "表务表况"
        context["page_menu"] = "统计报表"
        
        return context  

class VehicleView(LoginRequiredMixin,TemplateView):
    template_name = "reports/vehicle.html"

    def get_context_data(self, *args, **kwargs):
        context = super(VehicleView, self).get_context_data(*args, **kwargs)
        context["page_title"] = "车辆报表"
        context["page_menu"] = "统计报表"
        
        return context  

class BigdataView(LoginRequiredMixin,TemplateView):
    template_name = "reports/bigdata.html"

    def get_context_data(self, *args, **kwargs):
        context = super(BigdataView, self).get_context_data(*args, **kwargs)
        context["page_title"] = "大数据报表"
        context["page_menu"] = "统计报表"
        
        return context  

