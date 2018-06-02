# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

from . import views

app_name = 'entm'
urlpatterns = [
    
    # url(r'^$', TemplateView.as_view(template_name='dma/home.html'),name='virvo_home'),

    url(r'^(?P<page>.+\.html)$', views.StaticView.as_view()),

    # tree list etc

    # 企业管理 --角色管理
    #组织

    #用户

    #角色

    # url(r'^role/choicePermissionTree/',views.choicePermissionTree,name='choicePermissionTree'),
    # url(r'^role/rolelist/',views.rolelist,name='rolelist'),
    # url(r'^roles/?$', views.RolesMangerView.as_view(), name='roles_manager'),
    # url(r'^roles/create/?$', views.RolesCreateMangerView.as_view(), name='role_create_manager'),
    # url(r'^roles/update/(?P<pk>[0-9]+)/?$', views.RolesUpdateManagerView.as_view(), name='role_edit_manager'),

    # url(r'^user/oranizationtree/',views.oranizationtree,name='oranizationtree'),
    # url(r'^user/group/add/',views.groupadd,name='groupadd'),
    # url(r'^user/userlist/',views.userlist,name='userlist'),
    # url(r'^organ_users/?$', views.OrganUserMangerView.as_view(), name='organ_users'),#组织和用户管理
    # url(r'^user/create/?$', views.UserCreateMangerView.as_view(), name='user_create_manager'),
    # url(r'^user/update/(?P<pk>[0-9]+)/?$', views.UserUpdateManagerView.as_view(), name='user_edit_manager'),
    # url(r'^user/assign_role/(?P<pk>[0-9]+)/?$', views.AssignRoleView.as_view(), name='assign_role'),#分配角色
    # url(r'^user/auth_station/(?P<pk>[0-9]+)/?$', views.AuthStationView.as_view(), name='auth_station'),#授权站点


    
]