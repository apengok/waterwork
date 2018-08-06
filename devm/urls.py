# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

from . import views

app_name = 'devm'
urlpatterns = [
    
    #使用hplus页面布局时的首页
    # url(r'^$', TemplateView.as_view(template_name='hplus.html'),name='virvo_home'),
    url(r'^$', TemplateView.as_view(template_name='_vbase.html'),name='dma_home'),




    #meters   
    url(r'^meter/repetition/$',views.repetition,name='repetition'),

    url(r'^metermanager/?$', views.MeterMangerView.as_view(), name='metermanager'),#组织和用户管理
    url(r'^meter/list/$',views.meterlist,name='meterlist'),
    url(r'^meter/add',views.MeterAddView.as_view(),name='meteradd'),
    url(r'^meter/edit/(?P<pk>\w+)/?$',views.MeterEditView.as_view(),name='meteredit'),
    url(r'^meter/delete/(?P<pk>[0-9]+)/?$',views.MeterDeleteView.as_view(),name='meterdelete'),
    url(r'^meter/deletemore',views.meterdeletemore,name='meterdeletemore'),
    url(r'^meter/getMeterSelect/$',views.getMeterSelect,name='getMeterSelect'),
    
    #simcards   
    url(r'^simcard/repetition/$',views.simcard_repetition,name='simcard_repetition'),
    url(r'^simcard/getSimcardSelect/$',views.getSimcardSelect,name='getSimcardSelect'),
    url(r'^simcard/getSimRelated/$',views.getSimRelated,name='getSimRelated'),
    url(r'^simcard/releaseRelate/$',views.releaseRelate,name='releaseRelate'),

    url(r'^simcardmanager/?$', views.SimCardMangerView.as_view(), name='simcardmanager'),#组织和用户管理
    url(r'^simcard/list/$',views.simcardlist,name='simcardlist'),
    url(r'^simcard/add',views.SimCardAddView.as_view(),name='simcardadd'),
    url(r'^simcard/edit/(?P<pk>\w+)/?$',views.SimCardEditView.as_view(),name='simcardedit'),
    url(r'^simcard/delete/(?P<pk>[0-9]+)/?$',views.SimCardDeleteView.as_view(),name='simcarddelete'),

    # url(r'^stations/export',views.stationexport,name='stationexport'),
    # url(r'^stations/import',views.StationImportView.as_view(),name='stationimport'),
    # url(r'^stations/download',views.download,name='download'),

    # url(r'^infoconfig/infoinput/importProgress',views.importProgress,name='importProgress'),

    
]