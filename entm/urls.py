# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

from . import views

app_name = 'entm'
urlpatterns = [
    
    url(r'^$', TemplateView.as_view(template_name='_vbase.html'),name='virvo_home'),

    url(r'^(?P<page>.+\.html)$', views.StaticView.as_view()),

    # url(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),

    # tree list etc
    url(r'^role/choicePermissionTree',views.choicePermissionTree,name='choicePermissionTree'),
    url(r'^user/oranizationtree/',views.oranizationtree,name='oranizationtree'),

    # 企业管理 --角色管理
    #组织
    url(r'^user/group/add/?$',views.UserGroupAddView.as_view(),name='groupadd'),
    url(r'^user/group/edit/(?P<pId>\w+)/?$',views.UserGroupEditView.as_view(),name='groupedit'),
    url(r'^user/group/detail/(?P<pId>\w+)/?$',views.UserGroupDetailView.as_view(),name='groupdetail'),
    url(r'^user/group/delete/?$',views.UserGroupDeleteView.as_view(),name='groupdelete'),
    url(r'^group/findOperations',views.findOperations,name='findOperations'),

    #用户
    url(r'^user/verifyUserName/?$',views.verifyUserName,name='verifyUserName'),
    url(r'^user/verification/?$',views.verification,name='verification'),
    url(r'^user/roleList_/(?P<pk>[0-9]+)/?$',views.AssignRoleView.as_view(),name='roleList_'),
    url(r'^user/assign_stn/(?P<pk>[0-9]+)/?$',views.AssignStnView.as_view(),name='assign_stn'),
    url(r'^usermanager/?$', views.UserMangerView.as_view(), name='usermanager'),#组织和用户管理
    url(r'^user/list/$',views.userlist,name='userlist'),
    url(r'^user/add',views.UserAddView.as_view(),name='useradd'),
    url(r'^user/edit/(?P<pk>[0-9]+)/?$',views.UserEditView.as_view(),name='useredit'),
    url(r'^user/delete/(?P<pk>[0-9]+)/?$',views.UserDeleteView.as_view(),name='userdelete'),
    url(r'^user/deletemore',views.userdeletemore,name='userdeletemore'),

    #角色
    url(r'^rolemanager/?$',views.RolesMangerView.as_view(),name='rolemanager'),
    url(r'^role/list/$',views.rolelist,name='rolelist'),
    url(r'^role/add/',views.RolesAddView.as_view(),name='roleadd'),
    url(r'^role/edit/(?P<pk>\w+)/?$',views.RoleEditView.as_view(),name='roleedit'),
    url(r'^role/delete_/(?P<pk>[0-9]+)/?$',views.RoleDeleteView.as_view(),name='roledelete'),
    url(r'^role/deletemore',views.roledeletemore,name='roledeletemore'),

    
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