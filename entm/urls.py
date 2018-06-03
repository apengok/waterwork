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
    url(r'^role/choicePermissionTree/',views.choicePermissionTree,name='choicePermissionTree'),
    url(r'^user/oranizationtree/',views.oranizationtree,name='oranizationtree'),

    # 企业管理 --角色管理
    #组织
    url(r'^user/group/add',views.UserGroupAddView.as_view(),name='groupadd'),

    #用户
    url(r'^usermanager/?$', views.UserMangerView.as_view(), name='usermanager'),#组织和用户管理
    url(r'^user/list/$',views.userlist,name='userlist'),
    url(r'^user/add',views.useradd,name='useradd'),
    url(r'^user/edit',views.useredit,name='useredit'),
    url(r'^user/delete',views.userdelete,name='userdelete'),
    url(r'^user/deletemore',views.userdeletemore,name='userdeletemore'),

    #角色
    url(r'^role/list/$',views.rolelist,name='rolelist'),
    url(r'^role/list/add',views.roleadd,name='roleadd'),
    url(r'^role/list/edit',views.roleedit,name='roleedit'),
    url(r'^role/list/delete',views.roledelete,name='roledelete'),
    url(r'^role/list/deletemore',views.roledeletemore,name='roledeletemore'),

    
    # url(r'^roles/?$', views.RolesMangerView.as_view(), name='roles_manager'),
    # url(r'^roles/create/?$', views.RolesCreateMangerView.as_view(), name='role_create_manager'),
    # url(r'^roles/update/(?P<pk>[0-9]+)/?$', views.RolesUpdateManagerView.as_view(), name='role_edit_manager'),

    
    # url(r'^user/group/add/',views.groupadd,name='groupadd'),
    # url(r'^user/userlist/',views.userlist,name='userlist'),
    # url(r'^organ_users/?$', views.OrganUserMangerView.as_view(), name='organ_users'),#组织和用户管理
    # url(r'^user/create/?$', views.UserCreateMangerView.as_view(), name='user_create_manager'),
    # url(r'^user/update/(?P<pk>[0-9]+)/?$', views.UserUpdateManagerView.as_view(), name='user_edit_manager'),
    # url(r'^user/assign_role/(?P<pk>[0-9]+)/?$', views.AssignRoleView.as_view(), name='assign_role'),#分配角色
    # url(r'^user/auth_station/(?P<pk>[0-9]+)/?$', views.AuthStationView.as_view(), name='auth_station'),#授权站点


    
]