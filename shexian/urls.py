# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

from . import views

app_name = 'shexian'
urlpatterns = [
    
    url(r'^$', TemplateView.as_view(template_name='shexian/dmareport.html')),

    url(r'^district/dmatree/?$',views.dmatree,name='dmatree'),
    

    
    # DMA报表
    url(r'^dmastatics/?$',views.DmastaticsView.as_view(),name='dmastatics'),
    url(r'^dmareport/?$',views.dmareport,name='dmareport'),
    url(r'^wenxinyuan/?$',views.WenxinyuanView.as_view(),name='wenxinyuan'),
    
    url(r'^mnf/?$',views.MnfView.as_view(),name='mnf'),
    url(r'flowdata_mnf/?$',views.flowdata_mnf,name='flowdata_mnf'),
        
    url(r'^paramter/?$',views.ParamsMangerView.as_view(),name='paramter'),

]