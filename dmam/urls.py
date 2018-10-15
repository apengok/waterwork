# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

from . import views

app_name = 'dmam'
urlpatterns = [
    
    #使用hplus页面布局时的首页
    # url(r'^$', TemplateView.as_view(template_name='hplus.html'),name='virvo_home'),
    url(r'^$', TemplateView.as_view(template_name='_vbase.html'),name='dma_home'),


    # tree list etc
    
    url(r'^district/dmatree/',views.dmatree,name='dmatree'),

    # dma管理 --dma分区管理
    url(r'^districtmanager/?$', views.DistrictMangerView.as_view(), name='districtmanager'),#组织和用户管理
    url(r'^district/add/?$',views.DistrictAddView.as_view(),name='districtadd'),
    url(r'^district/edit/(?P<pId>\w+)/?$',views.DistrictEditView.as_view(),name='districtedit'),
    url(r'^district/detail/(?P<pId>\w+)/?$',views.DistrictDetailView.as_view(),name='districtdetail'),
    url(r'^district/delete/?$',views.DistrictDeleteView.as_view(),name='districtdelete'),
    url(r'^district/dmabaseinfo/?$',views.dmabaseinfo,name='dmabaseinfo'),
    url(r'^district/dmabaseinfo/edit/(?P<pk>\w+)/?$',views.DMABaseinfoEditView.as_view(),name='dmabaseinfoedit'),
    url(r'^getdmamapusedata/?$',views.getdmamapusedata,name='getdmamapusedata'),
    url(r'^verifydmano/?$',views.verifydmano,name='verifydmano'),
    url(r'^verifydmaname/?$',views.verifydmaname,name='verifydmaname'),

    #dma分区站点配置
    url(r'^district/assignstation/(?P<pk>\w+)/?$',views.DistrictAssignStationView.as_view(),name='districtassignstation'),
    url(r'^dmaStation/getdmastationsbyId/?$',views.getdmastationsbyId,name='getdmastationsbyId'),
    url(r'^dmaStation/saveDmaStation/?$',views.saveDmaStation,name='saveDmaStation'),


    

    #stations  
    url(r'^station/findUsertypes/?$',views.findUsertypes,name='findUsertypes'),
    url(r'^station/findUsertypeById/?$',views.findUsertypeById,name='findUsertypeById'),
    url(r'^station/updateOperation/?$',views.updateOperation,name='updateOperation'),
    url(r'^station/deleteOperation/?$',views.deleteOperation,name='deleteOperation'),
    url(r'^station/deleteOperationMore/?$',views.deleteOperationMore,name='deleteOperationMore'),
    
    url(r'^station/findusertypeByusertype/?$',views.findusertypeByusertype,name='findusertypeByusertype'),
    url(r'^station/findUsertypeCompare/?$',views.findUsertypeCompare,name='findUsertypeCompare'),
    
    url(r'^station/usertype/add/?$',views.usertypeadd,name='usertypeadd'),
    url(r'^station/usertype/edit/(?P<pk>[0-9]+)/?$',views.usertypeedit,name='usertypeedit'),

    url(r'^station/verifyusername/$',views.verifyusername,name='verifyusername'),
    
    url(r'^stationsmanager/?$', views.StationMangerView.as_view(), name='stationsmanager'),#组织和用户管理
    url(r'^stations/list/$',views.stationlist,name='stationlist'),
    url(r'^stations/add',views.StationAddView.as_view(),name='stationadd'),
    url(r'^stations/edit/(?P<pk>\w+)/?$',views.StationEditView.as_view(),name='stationedit'),
    url(r'^stations/delete/(?P<pk>[0-9]+)/?$',views.StationDeleteView.as_view(),name='stationdelete'),
    # url(r'^stations/deletemore',views.stationdeletemore,name='stationdeletemore'),
    url(r'^dmastations/list/(?P<pk>\w+)/$',views.dmastationlist,name='dmastationlist'),
    
    url(r'^station/getmeterlist/$',views.getmeterlist,name='getmeterlist'),
    url(r'^station/getmeterParam/$',views.getmeterParam,name='getmeterParam'),

    # url(r'^stations/export',views.stationexport,name='stationexport'),
    # url(r'^stations/import',views.StationImportView.as_view(),name='stationimport'),
    # url(r'^stations/download',views.download,name='download'),

    # url(r'^infoconfig/infoinput/importProgress',views.importProgress,name='importProgress'),

    # 二供管理
    url(r'^secondmanager/?$', views.SecondMangerView.as_view(), name='secondmanager'),
    # 视频管理
    url(r'^vediomanager/?$', views.VedioMangerView.as_view(), name='vediomanager'),
    # 车辆管理
    url(r'^vehiclemanager/?$', views.VehicleMangerView.as_view(), name='vehiclemanager'),

    # 小区管理
    url(r'^neighborhoodmanager/?$', views.NeighborhoodMangerView.as_view(), name='neighborhoodmanager'),


]