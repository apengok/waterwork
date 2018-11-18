# -*- coding:utf-8 -*-

"""leakage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include,handler404,handler500
from django.contrib import admin

from entm.views import i18n_javascript,error_404,error_500,StaticView,faviconredirect
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.urls import  path  # For django versions from 2.0 and up

from django.conf.urls.static import static
from accounts.views import LoginView, RegisterView

urlpatterns = [
    # url(r'^favicon\.ico$', RedirectView.as_view(url='/static/virvo/resources/img/favicon.ico')),
    url(r'^favicon\.ico$', faviconredirect,name='faviconredirect'),
    url(r'^admin/jsi18n', i18n_javascript),
    url(r'^admin/', admin.site.urls),
    url(r'^$',LoginView.as_view(), name='login'),
    # url(r'^$',TemplateView.as_view(template_name='_vbase.html'),name='home'),

    url(r'^(?P<page>.+\.html)$', StaticView.as_view()),
    url(r'^echarts/map/province/(?P<page>.+\.json)$', StaticView.as_view()),

    #使用hplus页面布局是iframe加载的首页项
    url(r'^index/$', TemplateView.as_view(template_name='_hplus_vbase.html'), name='index'),

    url(r'^accounts/$', RedirectView.as_view(url='/account')),
    url(r'^account/', include("accounts.urls", namespace='account')),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    

    #monitor

    #waterwork
    url(r'^prodschedule/', include('prodschedule.urls', namespace='prodschedule')),
    url(r'^monitor/', include('monitor.urls', namespace='monitor')),
    url(r'^analysis/', include('analysis.urls', namespace='analysis')),
    url(r'^alarm/', include('alarm.urls', namespace='alarm')),
    url(r'^baseanalys/', include('baseanalys.urls', namespace='baseanalys')),
    url(r'^gis/', include('gis.urls', namespace='gis')),
    url(r'^entm/', include('entm.urls', namespace='entm')),
    url(r'^devm/', include('devm.urls', namespace='devm')),
    url(r'^dmam/', include('dmam.urls', namespace='dmam')),
    url(r'^wirelessm/', include('wirelessm.urls', namespace='wirelessm')),
    url(r'^reports/', include('reports.urls', namespace='reports')),
    url(r'^sysm/', include('sysm.urls', namespace='sysm')),

    url(r'^shexian/', include('shexian.urls', namespace='shexian')),
    # url(r'^testapp/', include('testapp.urls')),
    
    # url(r'^celery-progress/', include('celery_progress.urls')),  # the endpoint is configurable
    
]

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#         path('__debug__/', include(debug_toolbar.urls)),

#         # For django versions before 2.0:
#         # url(r'^__debug__/', include(debug_toolbar.urls)),

#     ] + urlpatterns


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    

handler404 = error_404
handler500 = error_500

if not settings.DEBUG:
    import waterwork.jobs