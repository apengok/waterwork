# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from entm.models import Organizations
# from legacy.models import Bigmeter
# Create your models here.

'''
用水性质
'''
class WaterUserType(models.Model):
    """docstring for WaterUserType"""
    usertype = models.CharField(max_length=256,null=False,blank=False)
    explains = models.CharField(max_length=1000,null=True,blank=True)

    class Meta:
        managed = True
        db_table = 'waterusertype'

    def __unicode__(self):
        return self.usertype
        

class DMABaseinfo(models.Model):
    dma_no        = models.CharField('分区编号',max_length=50, unique=True)
    dma_name      = models.CharField('分区名称',max_length=50, unique=True)

    pepoles_num   = models.CharField('服务人口',max_length=50, null=True,blank=True)
    acreage       = models.CharField('服务面积',max_length=50, null=True,blank=True)
    user_num      = models.CharField('用户数量',max_length=50, null=True,blank=True)
    pipe_texture  = models.CharField('管道材质',max_length=50, null=True, blank=True)
    pipe_length   = models.CharField('管道总长度(m)',max_length=50, null=True, blank=True)
    pipe_links    = models.CharField('管道连接总数(个)',max_length=50,null=True, blank=True)
    pipe_years    = models.CharField('管道最长服务年限(年)',max_length=50,null=True, blank=True)
    pipe_private  = models.CharField('私人拥有水管长度(m)',max_length=50,blank=True,null=True)
    ifc           = models.CharField('IFC参数',max_length=250, null=True, blank=True)
    aznp          = models.CharField('AZNP',max_length=250,null=True, blank=True)
    night_use     = models.CharField('正常夜间用水量',max_length=50,null=True, blank=True)
    cxc_value     = models.CharField('产销差目标值',max_length=50, null=True, blank=True)

    creator      = models.CharField('负责人',max_length=50, null=True, blank=True) 
    create_date  = models.CharField('建立日期',max_length=30, null=True, blank=True) 

    belongto = models.ForeignKey(
        Organizations,
        on_delete=models.CASCADE,
        related_name='dma',
        # primary_key=True,
    )

    class Meta:
        managed=True
        unique_together = ('dma_no', )
        db_table = 'dmabaseinfo'

        

    def get_absolute_url(self): #get_absolute_url
        # return "/organ/{}".format(self.pk)
        return reverse('dma:dma_manager', kwargs={'pk': self.pk})

    def __unicode__(self):
        return self.dma_name

    def __str__(self):
        return self.dma_name        



class DmaStations(models.Model):
    dmaid       = models.ForeignKey(DMABaseinfo,related_name='dmastation',blank=True, null=True,on_delete=models.CASCADE) 
    # station_id  = models.ForeignKey(Bigmeter,related_name='underdma',blank=True, null=True,on_delete=models.CASCADE) 
    station_id  = models.CharField(max_length=30)   #store Bigmeter commaddr 
    meter_type  = models.CharField(max_length=30)

    class Meta:
        managed=True
        db_table = 'dmastations'  

    def __unicode__(self):
        return self.dmaid.dma_name

    def __str__(self):
        return self.dmaid.dma_name   


class SimCard(models.Model):
    simcardNumber       = models.CharField(db_column='SIMID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    belongto            = models.ForeignKey(Organizations,on_delete=models.CASCADE,related_name='simcard')
    isStart             = models.CharField(db_column='state', max_length=64, blank=True, null=True)  # Field name made lowercase.
    iccid               = models.CharField(db_column='ICCID', max_length=30, blank=True, null=True)  # Field name made lowercase.型号
    imei                = models.CharField(db_column='IMEI', max_length=30, blank=True, null=True)  # Field name made lowercase.
    imsi                = models.CharField(db_column='IMSI', max_length=30, blank=True, null=True)  # Field name made lowercase.
    operator            = models.CharField(db_column='operator', max_length=30, blank=True, null=True)  # Field name made lowercase.
    simFlow             = models.CharField(db_column='simFlow', max_length=30, blank=True, null=True)  # Field name made lowercase.
    openCardTime        = models.CharField(db_column='openCardTime', max_length=64, blank=True, null=True)  # Field name made lowercase.
    endTime             = models.CharField(db_column='endTime', max_length=64, blank=True, null=True)  # Field name made lowercase.
    create_date         = models.CharField(db_column='create_date', max_length=64, blank=True, null=True)  # Field name made lowercase.
    update_date         = models.CharField(db_column='update_date', max_length=64, blank=True, null=True)  # Field name made lowercase.
    remark              = models.CharField(db_column='remark', max_length=64, blank=True, null=True)  # Field name made lowercase.
    

    class Meta:
        managed = True
        db_table = 'simcard'

    def __unicode__(self):
        return '%s'%(self.simcardNumber)    


class Meter(models.Model):
    serialnumber= models.CharField(db_column='SerialNumber', max_length=30, blank=True, null=True)  # Field name made lowercase.
    # simid       = models.CharField(db_column='SIMID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    simid       = models.ForeignKey(SimCard,on_delete=models.CASCADE,related_name='meter') # Field name made lowercase.
    version     = models.CharField(db_column='version', max_length=30, blank=True, null=True)  # Field name made lowercase.型号
    dn          = models.CharField(db_column='Dn', max_length=30, blank=True, null=True)  # Field name made lowercase.
    metertype   = models.CharField(db_column='MeterType', max_length=30, blank=True, null=True)  # Field name made lowercase.
    belongto    = models.ForeignKey(Organizations,on_delete=models.CASCADE,related_name='meter')
    mtype       = models.CharField(db_column='Type', max_length=30, blank=True, null=True)  # Field name made lowercase.
    manufacturer= models.CharField(db_column='Manufacturer', max_length=30, blank=True, null=True)  # Field name made lowercase.
    protocol    = models.CharField(db_column='Protocol', max_length=64, blank=True, null=True)  # Field name made lowercase.
    R           = models.CharField(db_column='R', max_length=64, blank=True, null=True)  # Field name made lowercase.
    q3          = models.CharField(db_column='Q3', max_length=64, blank=True, null=True)  # Field name made lowercase.
    q1          = models.CharField(db_column='Q1', max_length=64, blank=True, null=True)  # Field name made lowercase.
    check_cycle = models.CharField(db_column='check cycle', max_length=64, blank=True, null=True)  # Field name made lowercase.
    state       = models.CharField(db_column='state', max_length=64, blank=True, null=True)  # Field name made lowercase.


    class Meta:
        managed = True
        db_table = 'meter'

    def __unicode__(self):
        return '%s'%(self.serialnumber)    

class Station(models.Model):
    username    = models.CharField(db_column='UserName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=30, blank=True, null=True)  # Field name made lowercase.
    usertype    = models.CharField(db_column='UserType', max_length=128, blank=True, null=True)  # Field name made lowercase.
    madedate    = models.CharField(db_column='MadeDate', max_length=30, blank=True, null=True)  # Field name made lowercase.
    lng         = models.CharField(db_column='Lng', max_length=30, blank=True, null=True)  # Field name made lowercase.
    lat         = models.CharField(db_column='Lat', max_length=30, blank=True, null=True)  # Field name made lowercase.
    coortype    = models.CharField(db_column='CoorType', max_length=30, blank=True, null=True)  # Field name made lowercase.
    # commaddr = models.CharField(db_column='CommAddr', primary_key=True, max_length=30)  # Field name made lowercase.
    # districtid = models.IntegerField(db_column='DistrictId', blank=True, null=True)  # Field name made lowercase.
    # districtid = models.ForeignKey(District,db_column='DistrictId',related_name='bigmeter',blank=True, null=True,on_delete=models.CASCADE) 
    biguser     = models.CharField(db_column='biguser', max_length=30, blank=True, null=True)  # Field name made lowercase.
    focus       = models.CharField(db_column='focus', max_length=30, blank=True, null=True)  # Field name made lowercase.
    locate      = models.CharField(db_column='locate', max_length=30, blank=True, null=True)  # Field name made lowercase.
    belongto    = models.ForeignKey(Organizations,on_delete=models.CASCADE,related_name='station') #所属组织
    meter       = models.ForeignKey(Meter,on_delete=models.CASCADE,related_name='station') #关联表具
    dmaid       = models.ForeignKey(DMABaseinfo,related_name='station',blank=True, null=True,on_delete=models.CASCADE) #所在dma分区

    dmametertype     = models.CharField(db_column='MeterType', max_length=30, blank=True, null=True)  # Field name made lowercase.


    class Meta:
        managed = True
        db_table = 'station'

    def __unicode__(self):
        return '%s'%(self.username)        