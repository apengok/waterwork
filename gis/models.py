# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from entm.models import Organizations
import datetime
from django.db.models import Q
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.db.models import Avg, Max, Min, Sum
from django.utils.functional import cached_property
import time

from mptt.models import MPTTModel, TreeForeignKey

'''
{"name":"标注","pId":"","id":"zw_m_marker","type":"fenceParent","open":"true"},
{"name":"矩形","pId":"","id":"zw_m_rectangle","type":"fenceParent","open":"true"},
{"name":"圆形","pId":"","id":"zw_m_circle","type":"fenceParent","open":"true"},
{"name":"多边形","pId":"0","id":"zw_m_polygon","type":"fenceParent","open":"true"},
{"name":"行政区划","pId":"0","id":"zw_m_administration","type":"fenceParent","open":"true"},
'''                
class FenceDistrict(MPTTModel):
    name               = models.CharField('区域名称',max_length=100,unique=True)
    ftype               = models.CharField('区域类型',max_length=30,null=True,blank=True) #fenceParent,fence
    createDataTime      = models.CharField('创建时间',max_length=30,null=True,blank=True)
    updateDataTime      = models.CharField('修改时间',max_length=30,null=True,blank=True)
    createDataUsername         = models.CharField('创建人',max_length=30,null=True,blank=True)
    updateDataUsername         = models.CharField('修改人',max_length=30,null=True,blank=True)
    description       = models.TextField('描述',null=True,blank=True)

    cid           = models.CharField(max_length=100,null=True,blank=True)
    pId           = models.CharField(max_length=100,null=True,blank=True)

    belongto      = models.ForeignKey(Organizations,on_delete=models.CASCADE,null=True)

    parent  = TreeForeignKey('self', null=True, blank=True,on_delete=models.CASCADE, related_name='children', db_index=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        managed = True
        db_table = 'fencedistrict'

        

    def __unicode__(self):
        return self.name    

    def __str__(self):
        return self.name 


class Polygon(models.Model):
    polygonId   = models.CharField(max_length=255,null=True,blank=True)
    name   = models.CharField('区域名称',max_length=100,unique=True)
    ftype   = models.CharField('区域类型',max_length=30,null=True,blank=True)
    shape   = models.CharField('形状',max_length=30,null=True,blank=True)
    pointSeqs   = models.TextField()
    longitudes   = models.TextField()
    latitudes   = models.TextField()

    dma_no       = models.CharField(max_length=30,null=True,blank=True) #关联的dma分区  


    class Meta:
        managed = True
        db_table = 'polygon'

        

    def __unicode__(self):
        return self.name    

    def __str__(self):
        return self.name 

class FenceShape(models.Model):
    shapeId   = models.CharField(max_length=255,null=True,blank=True)   #形状公用，由shape区分
    name   = models.CharField('区域名称',max_length=100,unique=True)
    zonetype   = models.CharField('区域类型',max_length=30,null=True,blank=True)
    shape   = models.CharField('形状',max_length=30,null=True,blank=True)
    
    # 多边形 各点经纬度 也应用于矩形等
    pointSeqs   = models.TextField()
    longitudes   = models.TextField()
    latitudes   = models.TextField()

    # 矩形：左上角、右下角经纬度
    lnglatQuery_LU   = models.CharField(max_length=30,null=True,blank=True)
    lnglatQuery_RD   = models.CharField(max_length=30,null=True,blank=True)

    # 圆形：中心经纬度，半径
    centerPointLat   = models.CharField(max_length=30,null=True,blank=True)
    centerPointLng   = models.CharField(max_length=30,null=True,blank=True)
    centerRadius   = models.CharField(max_length=30,null=True,blank=True)
    
    # 行政区：省、市、区
    province   = models.CharField(max_length=30,null=True,blank=True)
    city   = models.CharField(max_length=30,null=True,blank=True)
    district   = models.CharField(max_length=30,null=True,blank=True)
    administrativeLngLat = models.TextField()

    # 边框和区域填色
    strokeColor   = models.CharField(max_length=100,blank=True,null=True)
    fillColor     = models.CharField(max_length=100,blank=True,null=True)

    dma_no       = models.CharField(max_length=30,null=True,blank=True) #关联的dma分区  


    class Meta:
        managed = True
        db_table = 'fenceshape'

        

    def __unicode__(self):
        return self.name    

    def __str__(self):
        return self.name 
    

from entm.utils import unique_shapeid_generator,unique_cid_generator

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.cid:
        # instance.slug = create_slug(instance)
        instance.cid = unique_cid_generator(instance)
        
# def polygon_pre_save_post_receiver(sender, instance, *args, **kwargs):
#     if not instance.polygonId:
#         # instance.slug = create_slug(instance)
#         instance.polygonId = unique_shapeid_generator(instance)
        
pre_save.connect(pre_save_post_receiver, sender=FenceDistrict)        
# pre_save.connect(polygon_pre_save_post_receiver, sender=Polygon)

