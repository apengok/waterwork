# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

from . import views

app_name = 'reports'
urlpatterns = [
    
    url(r'^$', TemplateView.as_view(template_name='reports/querylog.html')),

    

    # 统计报表 --日志查询
    url(r'^querylog/?$',views.QuerylogView.as_view(),name='querylog'),
    
    # 报警报表
    url(r'^alarm/?$',views.AlarmView.as_view(),name='alarm'),
    
    # 大用户报表
    url(r'^biguser/?$',views.BiguserView.as_view(),name='biguser'),
    
    # DMA报表
    url(r'^dmastatics/?$',views.DmastaticsView.as_view(),name='dmastatics'),
    # 流量报表
    url(r'^flows/?$',views.FlowsView.as_view(),name='flows'),
    # 水量报表
    url(r'^waters/?$',views.WatersView.as_view(),name='waters'),
    # 表务表况
    url(r'^biaowu/?$',views.BiaowuView.as_view(),name='biaowu'),
    # 车辆报表
    url(r'^vehicle/?$',views.VehicleView.as_view(),name='vehicle'),
    # 大数据报表
    url(r'^bigdata/?$',views.BigdataView.as_view(),name='bigdata'),
        
]