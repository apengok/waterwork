# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from entm.models import Organizations

# Create your models here.

'''
个性化设置
'''
class Personalized(models.Model):
    """docstring for Personalized"""
    # topTitle loginLogo homeLogo webIco copyright websiteName recordNumber groupId type frontPage
    ptype   =   models.CharField(max_length=10)   #default or custom
    # 登录页面
    loginLogo  = models.ImageField(upload_to='resources/img/logo/')
    # 平台网页标题ico
    webIco          = models.ImageField(upload_to='resources/img/logo/')
    # 平台首页Logo
    homeLogo = models.ImageField(upload_to='resources/img/logo/')
    # 平台首页登录标题
    topTitle     = models.CharField(max_length=256,null=True,blank=True)
    # 平台首页置底信息
    # bottomTitleMsg  = models.CharField(max_length=256,null=True,blank=True)
    copyright  = models.CharField(max_length=256,null=True,blank=True)
    websiteName  = models.CharField(max_length=256,null=True,blank=True)
    recordNumber  = models.CharField(max_length=256,null=True,blank=True)
    # 平台登录页设置
    frontPageMsg    = models.CharField(max_length=256,null=True,blank=True)
    frontPageMsgUrl    = models.CharField(max_length=256,null=True,blank=True)
    updateDataUsername = models.CharField(max_length=256,null=True,blank=True)
    updateDataTime = models.DateTimeField(db_column='updateDataTime', auto_now=True)  # Field name made lowercase.
    
    belongto        = models.ForeignKey(Organizations,on_delete=models.CASCADE,blank=True,null=True)


    class Meta:
        managed = True
        db_table = 'personalized'

    def __unicode__(self):
        return self.topTitleMsg
        