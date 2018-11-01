# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from entm.models import Organizations
import datetime
from django.db.models import Q
from legacy.models import Bigmeter,District,Community,HdbFlowData,HdbFlowDataHour,HdbFlowDataDay,HdbFlowDataMonth,HdbPressureData
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.db.models import Avg, Max, Min, Sum
from legacy.models import Bigmeter,District
from django.utils.functional import cached_property
import time
from legacy.utils import (HdbFlow_day_use,HdbFlow_day_hourly,HdbFlow_month_use,HdbFlow_monthly,hdb_watermeter_flow_monthly,
        Hdbflow_from_hdbflowmonth,
        ZERO_monthly_dict,generat_year_month_from)
from mptt.models import MPTTModel, TreeForeignKey

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

    def station_assigned(self):
        dmastations = self.dmastation_set.all()
        return dmastations

    def station_set_all(self):
        
        dmastations = self.dmastation_set.all()
        commaddr_list = []
        for d in dmastations:
            commaddr = d.station_id
            commaddr_list.append(commaddr)
        stationlist = Station.objects.filter(meter__simid__simcardNumber__in=commaddr_list)
            
        return stationlist

    def dma_statistic(self,month_list1):
        """
            month_list1 是一整年的月份列表
            month_list 是dma创建日期的月份其实列表，统计数据是从创建日期开始计算的
        """
        dmastations_list = self.station_set.all()
        
        # dmastations_list2 = self.station_set.values_list('meter__simid__simcardNumber','dmametertype')
        cre_data = datetime.datetime.strptime(self.create_date,"%Y-%m-%d")
        month_list = generat_year_month_from(cre_data.month,cre_data.year)
        # print("create data month_list",month_list)
        
        # meter_types = ["出水表","进水表","贸易结算表","未计费水表","官网检测表"] 管网监测表
        # 进水表  加和---> 进水总量
        water_in = 0
        monthly_in = ZERO_monthly_dict(month_list1)
        meter_in = dmastations_list.filter(dmametertype='进水表')
        
        for m in meter_in:
            commaddr = m.commaddr
            
            monthly_use = Hdbflow_from_hdbflowmonth(commaddr,month_list) #HdbFlow_monthly(commaddr)
            
            # print(m.username,commaddr,monthly_use)
            for k in monthly_in.keys():
                if k in monthly_use.keys():
                    monthly_in[k] += monthly_use[k]
                # else:
                #     monthly_in[k] = 0
        water_in = sum([monthly_in[k] for k in monthly_in.keys()])
        
        # 出水表 加和--->出水总量
        water_out = 0
        monthly_out = ZERO_monthly_dict(month_list1)
        meter_out = dmastations_list.filter(dmametertype='出水表')
        for m in meter_out:
            commaddr = m.commaddr
            monthly_use = Hdbflow_from_hdbflowmonth(commaddr,month_list) #HdbFlow_monthly(commaddr)
            # print(m.username,commaddr,monthly_use)
            for k in monthly_out.keys():
                if k in monthly_use.keys():
                    monthly_out[k] += monthly_use[k]
                # else:
                #     monthly_out[k] = monthly_use[k]
        water_out = sum([monthly_out[k] for k in monthly_out.keys()])
        
        # 售水量 = 所有贸易结算表的和
        water_sale = 0
        monthly_sale = ZERO_monthly_dict(month_list1)
        meter_sale = dmastations_list.filter(dmametertype='贸易结算表')

        for m in meter_sale:
            commaddr = m.commaddr
            if m.username == "文欣苑户表总表":
                monthly_use = hdb_watermeter_flow_monthly(105,month_list)

            else:
                monthly_use = Hdbflow_from_hdbflowmonth(commaddr,month_list) #HdbFlow_monthly(commaddr)
            # print(m.username,commaddr,monthly_use)
            for k in monthly_sale.keys():
                if k in monthly_use.keys():
                    monthly_sale[k] += monthly_use[k]
                # else:
                #     monthly_sale[k] = monthly_use[k]

        water_sale += sum([monthly_sale[k] for k in monthly_sale.keys()])
        
        # 未计量水量 = 所有未计费水表的和
        water_uncount = 0
        monthly_uncount = ZERO_monthly_dict(month_list1)
        meter_uncount = dmastations_list.filter(dmametertype='未计费水表')
        for m in meter_uncount:
            commaddr = m.commaddr
            monthly_use = Hdbflow_from_hdbflowmonth(commaddr,month_list) #HdbFlow_monthly(commaddr)
            # print(m.username,commaddr,monthly_use)
            for k in monthly_uncount.keys():
                if k in monthly_use.keys():
                    monthly_uncount[k] += monthly_use[k]
                # else:
                #     monthly_uncount[k] = monthly_use[k]
        water_uncount = sum([monthly_uncount[k] for k in monthly_uncount.keys()])
        
        # 漏损量 = 供水量-售水量-未计费水量 分区内部进水表要减去自己内部出水表才等于这个分区的供水量

        return {
            'water_in':water_in,
            'monthly_in':monthly_in,
            'water_out':water_out,
            'monthly_out':monthly_out,
            'water_sale':water_sale,
            'monthly_sale':monthly_sale,
            'water_uncount':water_uncount,
            'monthly_uncount':monthly_uncount,

        }


    def dma_statistic2(self,month_list1):
        """
            month_list1 是一整年的月份列表
            month_list 是dma创建日期的月份其实列表，统计数据是从创建日期开始计算的
        """
        dmastations_list = self.station_assigned()
        
        # dmastations_list2 = self.station_set.values_list('meter__simid__simcardNumber','dmametertype')
        cre_data = datetime.datetime.strptime(self.create_date,"%Y-%m-%d")
        month_list = generat_year_month_from(cre_data.month,cre_data.year)
        # print("create data month_list",month_list)
        
        # meter_types = ["出水表","进水表","贸易结算表","未计费水表","官网检测表"] 管网监测表
        # 进水表  加和---> 进水总量
        water_in = 0
        monthly_in = ZERO_monthly_dict(month_list1)
        meter_in = dmastations_list.filter(meter_type='进水表')
        
        for m in meter_in:
            commaddr = m.station_id
            
            monthly_use = Hdbflow_from_hdbflowmonth(commaddr,month_list) #HdbFlow_monthly(commaddr)
            
            # print(m.username,commaddr,monthly_use)
            for k in monthly_in.keys():
                if k in monthly_use.keys():
                    monthly_in[k] += monthly_use[k]
                # else:
                #     monthly_in[k] = 0
        water_in = sum([monthly_in[k] for k in monthly_in.keys()])
        
        # 出水表 加和--->出水总量
        water_out = 0
        monthly_out = ZERO_monthly_dict(month_list1)
        meter_out = dmastations_list.filter(meter_type='出水表')
        for m in meter_out:
            commaddr = m.station_id
            monthly_use = Hdbflow_from_hdbflowmonth(commaddr,month_list) #HdbFlow_monthly(commaddr)
            # print(m.username,commaddr,monthly_use)
            for k in monthly_out.keys():
                if k in monthly_use.keys():
                    monthly_out[k] += monthly_use[k]
                # else:
                #     monthly_out[k] = monthly_use[k]
        water_out = sum([monthly_out[k] for k in monthly_out.keys()])
        
        # 售水量 = 所有贸易结算表的和
        water_sale = 0
        monthly_sale = ZERO_monthly_dict(month_list1)
        meter_sale = dmastations_list.filter(meter_type='贸易结算表')

        for m in meter_sale:
            commaddr = m.station_id
            # if m.username == "文欣苑户表总表":
            if commaddr == '4022':
                monthly_use = hdb_watermeter_flow_monthly(105,month_list)

            else:
                monthly_use = Hdbflow_from_hdbflowmonth(commaddr,month_list) #HdbFlow_monthly(commaddr)
            # print(m.username,commaddr,monthly_use)
            for k in monthly_sale.keys():
                if k in monthly_use.keys():
                    monthly_sale[k] += monthly_use[k]
                # else:
                #     monthly_sale[k] = monthly_use[k]

        water_sale += sum([monthly_sale[k] for k in monthly_sale.keys()])
        
        # 未计量水量 = 所有未计费水表的和
        water_uncount = 0
        monthly_uncount = ZERO_monthly_dict(month_list1)
        meter_uncount = dmastations_list.filter(meter_type='未计费水表')
        for m in meter_uncount:
            commaddr = m.station_id
            monthly_use = Hdbflow_from_hdbflowmonth(commaddr,month_list) #HdbFlow_monthly(commaddr)
            # print(m.username,commaddr,monthly_use)
            for k in monthly_uncount.keys():
                if k in monthly_use.keys():
                    monthly_uncount[k] += monthly_use[k]
                # else:
                #     monthly_uncount[k] = monthly_use[k]
        water_uncount = sum([monthly_uncount[k] for k in monthly_uncount.keys()])
        
        # 漏损量 = 供水量-售水量-未计费水量 分区内部进水表要减去自己内部出水表才等于这个分区的供水量

        return {
            'water_in':water_in,
            'monthly_in':monthly_in,
            'water_out':water_out,
            'monthly_out':monthly_out,
            'water_sale':water_sale,
            'monthly_sale':monthly_sale,
            'water_uncount':water_uncount,
            'monthly_uncount':monthly_uncount,

        }

'''
obsolete 
直接在Station 用ManyToManyField关联到dmabaseinfo
一个站点可能在多个dma中分担角色，‘直接在Station 用ManyToManyField关联到dmabaseinfo’不能区分该站点是数据哪个dma的表，
所以还是启用该table
'''
class DmaStation(models.Model):
    dmaid           = models.ForeignKey(DMABaseinfo,blank=True, null=True,on_delete=models.CASCADE) 
    station_id      = models.CharField(max_length=30)   # 大表 通讯地址commaddr 或者 小区关联的集中器commaddr，由station_type 标识
    meter_type      = models.CharField(max_length=30)   # dma计算类型 ["出水表","进水表","贸易结算表","未计费水表","管网检测表"]
    station_type    = models.CharField(max_length=30)   # 大表还是小区 1-大表 2-小区

    class Meta:
        managed=True
        db_table = 'dmastation'  

    def __unicode__(self):
        return self.dmaid.dma_name

    def __str__(self):
        return self.dmaid.dma_name   


class SimCardQuerySet(models.query.QuerySet):
    def search(self, query): #RestaurantLocation.objects.all().search(query) #RestaurantLocation.objects.filter(something).search()
        if query:
            query = query.strip()
            return self.filter(
                Q(meter__station__username__icontains=query)|
                Q(meter__serialnumber__icontains=query)|
                Q(simcardNumber__icontains=query)
                # Q(meter__simid__simcardNumber__iexact=query)
                ).distinct()
        return self


class SimCardManager(models.Manager):
    def get_queryset(self):
        return SimCardQuerySet(self.model, using=self._db)

    def search(self, query): #RestaurantLocation.objects.search()
        return self.get_queryset().search(query)

class SimCard(models.Model):
    simcardNumber       = models.CharField(db_column='SIMID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    belongto            = models.ForeignKey(Organizations,on_delete=models.CASCADE)
    isStart             = models.CharField(db_column='state', max_length=64, blank=True, null=True)  # Field name made lowercase.
    iccid               = models.CharField(db_column='ICCID', max_length=30, blank=True, null=True)  # Field name made lowercase.型号
    imei                = models.CharField(db_column='IMEI', max_length=30, blank=True, null=True)  # Field name made lowercase.
    imsi                = models.CharField(db_column='IMSI', max_length=30, blank=True, null=True)  # Field name made lowercase.
    operator            = models.CharField(db_column='operator', max_length=30, blank=True, null=True)  # Field name made lowercase.
    simFlow             = models.CharField(db_column='simFlow', max_length=30, blank=True, null=True)  # Field name made lowercase.
    openCardTime        = models.CharField(db_column='openCardTime', max_length=64, blank=True, null=True)  # Field name made lowercase.
    endTime             = models.CharField(db_column='endTime', max_length=64, blank=True, null=True)  # Field name made lowercase.
    create_date         = models.DateTimeField(db_column='create_date', auto_now_add=True)  # Field name made lowercase.
    update_date         = models.DateTimeField(db_column='update_date', auto_now=True)  # Field name made lowercase.
    remark              = models.CharField(db_column='remark', max_length=64, blank=True, null=True)  # Field name made lowercase.
    
    objects = SimCardManager()


    class Meta:
        managed = True
        db_table = 'simcard'

    def __unicode__(self):
        return '%s'%(self.simcardNumber)    

    def __str__(self):
        return '%s'%(self.simcardNumber)    


class MeterQuerySet(models.query.QuerySet):
    def search(self, query): #RestaurantLocation.objects.all().search(query) #RestaurantLocation.objects.filter(something).search()
        if query:
            query = query.strip()
            return self.filter(
                Q(station__username__icontains=query)|
                Q(serialnumber__icontains=query)|
                Q(simid__simcardNumber__icontains=query)
                ).distinct()
        return self


class MeterManager(models.Manager):
    def get_queryset(self):
        return MeterQuerySet(self.model, using=self._db)

    def search(self, query): #RestaurantLocation.objects.search()
        return self.get_queryset().search(query)

class Meter(models.Model):
    serialnumber= models.CharField(db_column='SerialNumber', max_length=30, blank=True, null=True)  # Field name made lowercase.
    # simid       = models.CharField(db_column='SIMID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    simid       = models.ForeignKey(SimCard,on_delete=models.SET_NULL,related_name='meter', blank=True, null=True) # Field name made lowercase.
    version     = models.CharField(db_column='version', max_length=30, blank=True, null=True)  # Field name made lowercase.型号
    dn          = models.CharField(db_column='Dn', max_length=30, blank=True, null=True)  # Field name made lowercase.
    metertype   = models.CharField(db_column='MeterType', max_length=30, blank=True, null=True)  # Field name made lowercase.
    belongto    = models.ForeignKey(Organizations,on_delete=models.CASCADE)
    mtype       = models.CharField(db_column='Type', max_length=30, blank=True, null=True)  # Field name made lowercase.
    manufacturer= models.CharField(db_column='Manufacturer', max_length=30, blank=True, null=True)  # Field name made lowercase.
    protocol    = models.CharField(db_column='Protocol', max_length=64, blank=True, null=True)  # Field name made lowercase.
    R           = models.CharField(db_column='R', max_length=64, blank=True, null=True)  # Field name made lowercase.
    q4          = models.CharField(db_column='Q4', max_length=64, blank=True, null=True)  # Field name made lowercase.
    q3          = models.CharField(db_column='Q3', max_length=64, blank=True, null=True)  # Field name made lowercase.
    q2          = models.CharField(db_column='Q2', max_length=64, blank=True, null=True)  # Field name made lowercase.
    q1          = models.CharField(db_column='Q1', max_length=64, blank=True, null=True)  # Field name made lowercase.
    check_cycle = models.CharField(db_column='check cycle', max_length=64, blank=True, null=True)  # Field name made lowercase.
    state       = models.CharField(db_column='state', max_length=64, blank=True, null=True)  # Field name made lowercase.


    objects = MeterManager()

    class Meta:
        managed = True
        db_table = 'meter'

    def __unicode__(self):
        return '%s'%(self.serialnumber)   

    def __str__(self):
        return '%s'%(self.serialnumber)    



# station manager


class StationQuerySet(models.query.QuerySet):
    def search(self, query): #RestaurantLocation.objects.all().search(query) #RestaurantLocation.objects.filter(something).search()
        if query:
            query = query.strip()
            return self.filter(
                Q(username__icontains=query)|
                Q(meter__serialnumber__icontains=query)|
                Q(meter__simid__simcardNumber__icontains=query)
                ).distinct()
        return self


class StationManager(models.Manager):
    def get_queryset(self):
        return StationQuerySet(self.model, using=self._db)

    def search(self, query): #RestaurantLocation.objects.search()
        return self.get_queryset().search(query)


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
    belongto    = models.ForeignKey(Organizations,on_delete=models.CASCADE) #所属组织
    meter       = models.ForeignKey(Meter,on_delete=models.SET_NULL, blank=True, null=True) #关联表具
    # dmaid       = models.ForeignKey(DMABaseinfo,blank=True, null=True,on_delete=models.CASCADE) #所在dma分区
    dmaid       = models.ManyToManyField(DMABaseinfo)

    dmametertype     = models.CharField(db_column='MeterType', max_length=30, blank=True, null=True)  # Field name made lowercase.

    # bigmeter = models.OneToOneField(Bigmeter,on_delete=models.CASCADE,null=True)

    objects = StationManager()

    class Meta:
        managed = True
        db_table = 'station'

    def __unicode__(self):
        return '%s'%(self.username)  

    def __str__(self):
        return '%s'%(self.username)        

    @property
    def commaddr(self):
        if self.meter is None:
            return None
        if self.meter.simid is None:
            return None
        if self.meter.simid.simcardNumber == "":
            return None
        return self.meter.simid.simcardNumber

    def flowData(self,startTime,endTime):
        flow_data = []
        if self.commaddr is None:
            return flow_data
        flows = HdbFlowData.objects.filter(commaddr=self.commaddr).filter(readtime__range=[startTime,endTime]).values_list("readtime","flux")

        return flows

    def flowData_day_hourly(self,startTime,endTime):
        flow_data = []
        if self.commaddr is None:
            return flow_data
        commaddr='064811210390'
        startTime='2018-09-24 00:00:00'
        endTime='2018-09-25 00:00:00'
        flows = HdbFlowData.objects.filter(commaddr=commaddr).filter(readtime__range=[startTime,endTime]).values_list("readtime","plustotalflux")
        f_dict =dict(flows)
        hours = ['00:00:00','01:00:00','02:00:00','03:00:00','04:00:00','05:00:00','06:00:00','07:00:00','08:00:00','09:00:00','10:00:00','11:00:00','12:00:00','13:00:00','14:00:00','15:00:00','16:00:00','17:00:00','18:00:00','19:00:00','20:00:00','21:00:00','22:00:00','23:00:00']
        zhengdian_value = []
        for h in hours:
            th=startTime[:11] + h
            v=f_dict[th]
            zhengdian_value.append(v)

        end_value = f_dict[endTime[:11]+"00:00:00"]
        zhengdian_value.append(end_value)
        print('zhengdian_value',zhengdian_value)
        diff_value=[]
        for i in range(len(zhengdian_value)-1):
            v = float(zhengdian_value[i+1]) - float(zhengdian_value[i])
            diff_value.append(round(v,2))

        print('diff_value',diff_value)

        return diff_value

    def flowData_Hour(self,startTime,endTime):
        flow_data = {}
        if self.commaddr is None:
            return flow_data

        # print(self.commaddr,startTime,endTime)
        hours = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','00']
        flows = HdbFlowDataHour.objects.filter(commaddr=self.commaddr).filter(hdate__range=[startTime,endTime]).values_list("hdate","dosage")
        if flows.count() == 0:
            for h in hours:
                fh = endTime[:11] + h
                flow_data[fh] = '-'
            return flow_data
        flow_dict = dict(flows)
        # print('flow_dict',flow_dict)
        flows_keys = [k[11:] for k,v in flows ]
        
        # print("print first",flows.first())
        tmp=flows.first()[0]
        for h in hours:
            if h in flows_keys:
                fh = tmp[:11]+h
                flow_data[fh] = round(float(flow_dict[fh]),2)
            else:
                fh = tmp[:11]+h
                flow_data[fh] = 0
        
        return flow_data


    def press_Data(self,startTime,endTime):
        press_data = {}
        if self.commaddr is None:
            return press_data
        pressures = HdbPressureData.objects.filter(commaddr=self.commaddr).filter(readtime__range=[startTime,endTime]).values_list("readtime","pressure")

        if pressures.count() == 0:
            return press_data
        # print('pressures:',pressures)
        press_data = dict(pressures)
        

        
        return press_data

    def daterange(self,start, end, step=datetime.timedelta(1)):
        curr = start
        while curr <= end:
            yield curr.strftime("%Y-%m-%d")
            curr += step
        
    def flowData_Day(self,startTime,endTime):
        flow_data = {}
        if self.commaddr is None:
            return flow_data

        flows = HdbFlowDataDay.objects.filter(commaddr=self.commaddr).filter(hdate__range=[startTime,endTime]).values_list("hdate","dosage")
        print('flowdata day:',flows)
        if flows.count() == 0:
            return flow_data
        flow_dict = dict(flows)
        print('flow_dict',flow_dict)
        flows_keys = [k for k,v in flows ]
        dates = self.daterange(startTime,endTime)
        print("print first",flows.first())
        tmp=flows.first()[0]
        for h in dates:
            if h in flows_keys:
                print (h,flow_dict[h])
                flow_data[h] = round(float(flow_dict[h]),2)
            else:
                flow_data[h] = 0
        
        return flow_data

        '''
            querydate --- datetime object
            return 日用水量
        '''
    def flow_day_dosage(self,querydate):
        ret_str = "-"
        datestr = querydate.strftime("%Y-%m-%d")
        startTime = datestr + " 00:00:00"
        endTime = datestr + " 23:59:59"

        flow = HdbFlowDataHour.objects.filter(commaddr=self.commaddr).filter(hdate__range=[startTime,endTime]).aggregate(Sum('dosage'))
        flow_value = flow['dosage__sum']
        if flow_value is not None:
            ret_str = "{} m³".format(round(float(flow_value),2))
        return ret_str

# 按小时统计的聚合Alarm.objects.values('commaddr').annotate(Count('id'))
    def flow_hour_aggregate(self,startTime,endTime):

        avg_str = "-"
        max_str = "-"
        min_str = "-"
        avg_flow = HdbFlowDataHour.objects.filter(commaddr=self.commaddr).filter(hdate__range=[startTime,endTime]).aggregate(Avg('dosage'))
        avg_value = avg_flow['dosage__avg']
        if avg_value is not None:
            avg_str = "{} m³".format(round(float(avg_value),2))

        max_flow = HdbFlowDataHour.objects.filter(commaddr=self.commaddr).filter(hdate__range=[startTime,endTime]).aggregate(Max('dosage'))
        max_value = max_flow['dosage__max']
        # 最大值instance
        max_date = ""
        if max_value is not None:
            max_item = HdbFlowDataHour.objects.filter(commaddr=self.commaddr).filter(hdate__range=[startTime,endTime]).filter(dosage=max_value)
            max_date = max_item[0].hdate
            max_str = "{} m³ ({}:00)".format(round(float(max_value),2),max_date[-2:])

        min_flow = HdbFlowDataHour.objects.filter(commaddr=self.commaddr).filter(hdate__range=[startTime,endTime]).aggregate(Min('dosage'))
        min_value = min_flow['dosage__min']
        # 最xiao值instance
        min_date = ""
        if min_value is not None:
            min_item = HdbFlowDataHour.objects.filter(commaddr=self.commaddr).filter(hdate__range=[startTime,endTime]).filter(dosage=min_value)
            min_date = min_item[0].hdate
            min_str = "{} m³ ({}:00)".format(round(float(min_value),2),min_date[-2:])

        return avg_str,max_str,min_str


    # 按日统计的聚合
    def flow_day_aggregate(self,startTime,endTime):

        avg_str = "-"
        max_str = "-"
        min_str = "-"
        avg_flow = HdbFlowDataDay.objects.filter(commaddr=self.commaddr).filter(hdate__range=[startTime,endTime]).aggregate(Avg('dosage'))
        avg_value = avg_flow['dosage__avg']
        if avg_value is not None:
            avg_str = "{} m³".format(round(float(avg_value),2))

        max_flow = HdbFlowDataDay.objects.filter(commaddr=self.commaddr).filter(hdate__range=[startTime,endTime]).aggregate(Max('dosage'))
        max_value = max_flow['dosage__max']
        # 最大值instance
        max_date = ""
        if max_value is not None:
            max_item = HdbFlowDataDay.objects.filter(commaddr=self.commaddr).filter(hdate__range=[startTime,endTime]).filter(dosage=max_value)
            max_date = max_item[0].hdate
            max_str = "{} m³ ({}:00)".format(round(float(max_value),2),max_date[-2:])

        min_flow = HdbFlowDataDay.objects.filter(commaddr=self.commaddr).filter(hdate__range=[startTime,endTime]).aggregate(Min('dosage'))
        min_value = min_flow['dosage__min']
        # 最xiao值instance
        min_date = ""
        if min_value is not None:
            min_item = HdbFlowDataDay.objects.filter(commaddr=self.commaddr).filter(hdate__range=[startTime,endTime]).filter(dosage=min_value)
            min_date = min_item[0].hdate
            min_str = "{} m³ ({}:00)".format(round(float(min_value),2),min_date[-2:])

        return avg_str,max_str,min_str


    @cached_property 
    def realtimedata(self):
        t1=time.time()
        if self.commaddr is None:
            return None

        if self.commaddr is not None:
            rtflow = HdbFlowData.objects.filter(commaddr=self.commaddr).last()
            press = HdbPressureData.objects.filter(commaddr=self.commaddr).last()
        else:
            print("commaddr is None",self.username)
            rtflow = None
            press = None
        # obj= Model.objects.filter(testfield=12).order_by('-id')[0]
        t2=time.time()-t1
        print("one query time",t2)
        return {
            "stationname":self.username,
            "belongto":self.belongto.name if self.belongto else '-',
            "serialnumber":self.meter.serialnumber if self.meter else '-',
            "alarm":0,
            "status":self.meter.state if self.meter else '-',
            "dn":self.meter.dn if self.meter else '-',
            "readtime":rtflow.readtime if rtflow is not None else '-',
            "collectperiod":self.meter.collectperiod if self.meter else '-',
            "updataperiod":self.meter.updataperiod if self.meter else '-',
            "influx":rtflow.flux if rtflow else '-',
            "plusflux":rtflow.plustotalflux if rtflow else '-',
            "revertflux":rtflow.reversetotalflux if rtflow else '-',
            "press":press.pressure if press else 0,
            "baseelectricity":0,
            "remoteelectricity":0,
            "signal":0,
            
        }

    def historydata(self,startTime,endTime):
        flow_data = []
        if self.commaddr is None:
            return flow_data
        rtflow = HdbFlowData.objects.filter(commaddr=self.commaddr).filter(readtime__range=[startTime,endTime])
        press = HdbPressureData.objects.filter(commaddr=self.commaddr).filter(readtime__range=[startTime,endTime])
        # obj= Model.objects.filter(testfield=12).order_by('-id')[0]

        if rtflow.exists():
            for r in rtflow:
                flow_data.append( {
                
                "readtime":r.readtime,
                
                "influx":r.flux,
                "plusflux":r.plustotalflux,
                "revertflux":r.reversetotalflux,
                "totalflux":r.totalflux,
                # "press":press.pressure if press else 0,
                
            })
        return flow_data



@receiver(post_save, sender=Station)
def ensure_bigmeter_exists(sender, **kwargs):
    district = District.objects.first()
    districtid = district.id
    if kwargs.get('created', False):
        instance=kwargs.get('instance')
        username= instance.username
        lng=instance.lng
        lat=instance.lat
        commaddr=instance.commaddr
        simid = instance.commaddr

        Bigmeter.objects.get_or_create(username=username,lng=lng,lat=lat,commaddr=commaddr,simid=simid,districtid=districtid,alarmoffline=1,alarmonline=1,
            alarmgprsvlow=1,alarmmetervlow=1,alarmuplimitflow=1,alarmgpflow=1,pressurealarm=1,dosagealarm=1)   
    else:
        print("ensure_bigmeter_exists edit")
        instance=kwargs.get('instance')
        username= instance.username
        lng=instance.lng
        lat=instance.lat
        commaddr=instance.commaddr
        simid = instance.commaddr
        bigm = Bigmeter.objects.filter(commaddr=instance.commaddr)
        if bigm.exists():
            # print(instance.username,bigm.first().username)
            b=bigm.first()
            b.username= instance.username
            b.lng=instance.lng
            b.lat=instance.lat
            b.commaddr=instance.commaddr
            b.simid = instance.commaddr
            # bigm.first().alarmoffline = 1
            # bigm.first().alarmonline = 1
            # bigm.first().alarmgprsvlow = 1
            # bigm.first().alarmmetervlow = 1
            # bigm.first().alarmuplimitflow = 1
            # bigm.first().alarmgpflow = 1
            # bigm.first().pressurealarm = 1
            # bigm.first().dosagealarm = 1
            b.save()
        else:
            Bigmeter.objects.create(username=username,lng=lng,lat=lat,commaddr=commaddr,simid=simid)  



# 小区
class VCommunity(MPTTModel):
    name = models.CharField(db_column='Name', max_length=64, blank=True, null=True)  # Field name made lowercase.
    parent  = TreeForeignKey('self', null=True, blank=True,on_delete=models.CASCADE, related_name='children', db_index=True)
    
    address = models.CharField(db_column='Address', max_length=128, blank=True, null=True)  # Field name made lowercase.

    belongto = models.ForeignKey(
        Organizations,
        on_delete=models.CASCADE,
        related_name='community',
        # primary_key=True,
    )

    commutid = models.IntegerField( blank=True, null=True) #对应抄表系统Community表的id

    class Meta:
        managed = True
        db_table = 'vcommunity'

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


# 集中器
class VConcentrator(models.Model):
    name = models.CharField(db_column='Name', max_length=64, blank=True, null=True)  # Field name made lowercase.
    commaddr = models.CharField('通讯识别码',max_length=50, null=True,blank=True)
    belongto = models.ForeignKey(
        Organizations,
        on_delete=models.CASCADE,
        related_name='concentrator',
        # primary_key=True,
    )

    communityid = models.ManyToManyField( VCommunity )

    class Meta:
        managed = True
        db_table = 'vconcentrator'


    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


# 水表 小表
class VWatermeter(models.Model):
    name = models.CharField(db_column='Name', max_length=64, blank=True, null=True)  # Field name made lowercase.
    # 适应歙县小表watermeterid
    waterid = models.IntegerField(db_column='WaterId', blank=True, null=True)  # Field name made lowercase.
    wateraddr = models.CharField(db_column='WaterAddr', max_length=30, blank=True, null=True)  # Field name made lowercase.
    belongto = models.ForeignKey(
        Organizations,
        on_delete=models.CASCADE,
        related_name='watermeter',
        # primary_key=True,
    )

    communityid = models.ForeignKey( VCommunity ,on_delete=models.CASCADE,
        related_name='watermeter',)

    class Meta:
        managed = True
        db_table = 'vwatermeter'


    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
