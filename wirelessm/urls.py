# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

from . import views

app_name = 'wirelessm'
urlpatterns = [
    
    #使用hplus页面布局时的首页
    # url(r'^$', TemplateView.as_view(template_name='hplus.html'),name='virvo_home'),
    url(r'^$', TemplateView.as_view(template_name='_vbase.html'),name='virvo_home'),


    #无线抄表
    # 数据查询
    url(r'^wlquerydata/?$',views.WlquerydataView.as_view(),name='wlquerydata'),
    
    # 小区日用水
    url(r'^neighborhoodusedayly/?$', views.NeighborhoodusedaylyView.as_view(), name='neighborhoodusedayly'),#组织和用户管理
    
    # 小区月用水
    url(r'^neighborhoodusemonthly/$',views.NeighborhoodusemonthlyView.as_view(),name='neighborhoodusemonthly'),
    
    # 户表管理
    url(r'^neighborhoodmetermanager/?$',views.NeighborhoodmeterMangerView.as_view(),name='neighborhoodmetermanager'),
   

    
]