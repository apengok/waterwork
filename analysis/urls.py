# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

from . import views

app_name = 'analysis'
urlpatterns = [
    
    url(r'^$', TemplateView.as_view(template_name='analysis/mnf.html'),name='analysis_home'),

    

    # 数据分析 -- 夜间最小流量
    url(r'^mnf/?$',views.MnfView.as_view(),name='mnf'),
    url(r'^mnf2/?$',views.MnfView2.as_view(),name='mnf2'),

    url(r'flowdata_mnf/?$',views.flowdata_mnf,name='flowdata_mnf'),

    url(r'^cxc/?$',views.CXCView.as_view(),name='cxc'),
    url(r'^cxc2/?$',views.CXCView2.as_view(),name='cxc2'),
    url(r'flowdata_cxc/?$',views.flowdata_cxc,name='flowdata_cxc'),
    # url(r'analysisCxc/dmastations//?$',views.dmastations,name='dmastations'),

    
        
]