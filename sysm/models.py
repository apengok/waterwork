# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse

# Create your models here.

'''
个性化设置
'''
class Personalized(models.Model):
    """docstring for Personalized"""
    # 登录页面
    logoPagesPhoto  = models.ImageField(upload_to='resources/img/logo/')
    # 平台网页标题ico
    WebIco          = models.ImageField(upload_to='resources/img/logo/')
    # 平台首页Logo
    indexPagesPhoto = models.ImageField(upload_to='resources/img/logo/')
    # 平台首页登录标题
    topTitleMsg     = models.CharField(max_length=256,null=True,blank=True)
    # 平台首页置底信息
    bottomTitleMsg  = models.CharField(max_length=256,null=True,blank=True)
    # 平台登录页设置
    frontPageMsg    = models.CharField(max_length=256,null=True,blank=True)


    class Meta:
        managed = True
        db_table = 'personalized'

    def __unicode__(self):
        return self.topTitleMsg
        