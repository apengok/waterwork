# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

from . import views

app_name = 'monitor'
urlpatterns = [
    
    url(r'^$', TemplateView.as_view(template_name='monitor/mapmonitor.html'),name='monitor_home'),

    # 站点地图
    url(r'^mapstation/?$',views.MapStationView.as_view(),name='mapstation'),
    url(r'^getmapstationlist/$',views.getmapstationlist,name='getmapstationlist'),
    
    # 实时曲线
    url(r'^realcurlv/?$',views.RealcurlvView.as_view(),name='realcurlv'),

    # 实时数据
    url(r'^realtimedata/?$',views.RealTimeDataView.as_view(),name='realtimedata'),

    # 车辆监控
    url(r'^vehicle/?$',views.VehicleView.as_view(),name='vehicle'),
    # 实时视频
    url(r'^vedio/?$',views.VedioView.as_view(),name='vedio'),
    # 二次供水 
    url(r'^secondwater/?$',views.SecondwaterView.as_view(),name='secondwater'),
    url(r'^getmapsecondwaterlist/$',views.getmapsecondwaterlist,name='getmapsecondwaterlist'),
    
    # 数据监控 --地图监控
    url(r'^mapmonitor2/?$',views.MapMonitorView.as_view(),name='mapmonitor2'),
    url(r'^mapmonitor/?$',views.MapMonitorView2.as_view(),name='mapmonitor'),
    url(r'^maprealdata/?$',views.maprealdata,name='maprealdata'),
    
    
    url(r'^station/list/?$',views.stationlist,name='stationlist'),

    # api
    url(r'^api/station/$',views.station_list,name='station_list'),
    url(r'^api/station/(?P<pk>[0-9]+)/?$',views.station_detail,name='station_detail'),
    
    url(r'^api/alarm/(?P<pk>[0-9]+)/?$',views.alarm_detail,name='alarm_detail'),

        
]