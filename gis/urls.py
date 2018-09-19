# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

from . import views

app_name = 'gis'
urlpatterns = [
    
    url(r'^$', TemplateView.as_view(template_name='gis/pipelinequery.html')),

    

    # GIS系统 --管网查询
    url(r'^pipelinequery/?$',views.PipelineQueryView.as_view(),name='pipelinequery'),
    
    # 管网统计
    url(r'^pipelinestastic/?$',views.PipelineStasticView.as_view(),name='pipelinestastic'),
    
    
    # GIS系统 --管网分析
    url(r'^pipelineanalys/?$',views.PipelineAnalysView.as_view(),name='pipelineanalys'),
    
    # 导入导出
    url(r'^pipelineimexport/?$',views.PipelineImexportView.as_view(),name='pipelineimexport'),
]