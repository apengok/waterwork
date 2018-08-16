# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

from . import views

app_name = 'sysm'
urlpatterns = [
    
    url(r'^$', TemplateView.as_view(template_name='sysm/personalizedList.html'),name='sysm_home'),

    

    # 数据监控 --地图监控
    url(r'^personalized/list/?$',views.personalizedView.as_view(),name='personalizedList'),
    
    
    url(r'^personalized/logoPagesPhoto/update/?$',views.logoPagesPhotoUpdate,name='logoPagesPhotoUpdate'),
    
    url(r'^personalized/update/?$',views.personalizedUpdate,name='personalizedUpdate'),
    url(r'^personalized/upload_img/?$',views.personalizedUpdate_img,name='personalizedUpdate_img'),
    url(r'^personalized/find/?$',views.personalizedFind,name='personalizedFind'),
    url(r'^personalized/default/?$',views.personalizedDefault,name='personalizedDefault'),
        
]