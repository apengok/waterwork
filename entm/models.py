# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
# Create your models here.

class Organizations(MPTTModel):
    name               = models.CharField('组织机构名称',max_length=300,null=True)
    attribute          = models.CharField('组织机构性质',max_length=300,null=True,blank=True)
    register_date      = models.CharField('注册日期',max_length=30,null=True,blank=True)
    owner_name         = models.CharField('负责人',max_length=300,null=True,blank=True)
    phone_number       = models.CharField('电话号码',max_length=300,null=True,blank=True)
    firm_address       = models.CharField('地址',max_length=300,null=True,blank=True)

    cid           = models.CharField(max_length=300,null=True,blank=True)
    pId           = models.CharField(max_length=300,null=True,blank=True)
    is_org        = models.BooleanField(max_length=300,blank=True)
    uuid          = models.CharField(max_length=300,null=True,blank=True)

    parent  = TreeForeignKey('self', null=True, blank=True,on_delete=models.CASCADE, related_name='children', db_index=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        managed = True
        db_table = 'organizations'

        permissions = (
            

            # 企业管理 sub
            ('firmmanager','企业管理'),
            ('rolemanager_firmmanager','角色管理'),
            ('rolemanager_firmmanager_edit','角色管理_可写'),
            ('organusermanager_firmmanager','组织和用户管理'),
            ('organusermanager_firmmanager_edit','组织和用户管理_可写'),

            
        )

    def __unicode__(self):
        return self.name    

    def __str__(self):
        return self.name 

    def sub_organizations(self,include_self=False):
        return self.get_descendants(include_self)


class PorgressBar(models.Model):
    totoal      = models.IntegerField(default=1)
    progress    = models.IntegerField(default=0)


    def progress_add(self):
        self.progress += 1

    def progress_set(self,n):
        self.totoal = n

    def progress_reset(self):
        self.totoal = 1
        self.progress = 0
