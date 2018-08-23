# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from entm.models import Organizations
import datetime
from legacy.models import Bigmeter,District,Community,HdbFlowData,HdbFlowDataHour,HdbFlowDataDay,HdbFlowDataMonth,HdbPressureData
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.db.models import Avg, Max, Min, Sum
from legacy.models import Bigmeter

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


'''
obsolete 
直接在Station 用ManyToManyField关联到dmabaseinfo
'''
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
    

    class Meta:
        managed = True
        db_table = 'simcard'

    def __unicode__(self):
        return '%s'%(self.simcardNumber)    

    def __str__(self):
        return '%s'%(self.simcardNumber)    


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

    # 通讯参数
    # TCP消息重发次数：
    tcpresendcount           = models.CharField(db_column='tcpresendcount', max_length=64, blank=True, null=True)  # Field name made lowercase.
    # TCP消息应答超时时间（s）
    tcpresponovertime           = models.CharField(db_column='tcpresponovertime', max_length=64, blank=True, null=True)  # Field name made lowercase.
    # UDP消息重发次数
    udpresendcount           = models.CharField(db_column='udpresendcount', max_length=64, blank=True, null=True)  # Field name made lowercase.
    # UDP消息应答超时时间（s）
    udpresponovertime           = models.CharField(db_column='udpresponovertime', max_length=64, blank=True, null=True)  # Field name made lowercase.
    # SMS消息重发次数
    smsresendcount           = models.CharField(db_column='smsresendcount', max_length=64, blank=True, null=True)  # Field name made lowercase.
    # SMS消息应答超时时间（s）
    smsresponovertime           = models.CharField(db_column='smsresponovertime', max_length=64, blank=True, null=True)  # Field name made lowercase.
    # 终端心跳发送间隔（s）
    heartbeatperiod           = models.CharField(db_column='heartbeatperiod', max_length=64, blank=True, null=True)  # Field name made lowercase.

    # 终端参数
    # IP地址
    ipaddr           = models.CharField(db_column='ipaddr', max_length=64, blank=True, null=True)  # Field name made lowercase.
    # 端口号
    port           = models.CharField(db_column='port', max_length=64, blank=True, null=True)  # Field name made lowercase.
    # 接入点
    entrypoint           = models.CharField(db_column='entrypoint', max_length=64, blank=True, null=True)  # Field name made lowercase.
    # 流量零点修正值
    flowzerovalue           = models.CharField(db_column='flowzerovalue', max_length=64, blank=True, null=True)  # Field name made lowercase.

    # 采集指令
    # 上报起始时间
    updatastarttime           = models.CharField(db_column='updatastarttime', max_length=64, blank=True, null=True)  # Field name made lowercase.
    # 上报方式选择 -- 间隔 定时 实时
    updatamode           = models.CharField(db_column='updatamode', max_length=64, blank=True, null=True)  # Field name made lowercase.
    # 采集间隔（分钟）5 10 15 30
    collectperiod           = models.CharField(db_column='collectperiod', max_length=64, blank=True, null=True)  # Field name made lowercase.
    # 上报间隔（小时）2 4 6 8 12
    updataperiod           = models.CharField(db_column='updataperiod', max_length=64, blank=True, null=True)  # Field name made lowercase.
    # 上报时间一
    updatatime1           = models.CharField(db_column='updatatime1', max_length=64, blank=True, null=True)  # Field name made lowercase.
    # 上报时间二
    updatatime2           = models.CharField(db_column='updatatime2', max_length=64, blank=True, null=True)  # Field name made lowercase.
    # 上报时间三
    updatatime3           = models.CharField(db_column='updatatime3', max_length=64, blank=True, null=True)  # Field name made lowercase.
    # 上报时间四
    updatatime4           = models.CharField(db_column='updatatime4', max_length=64, blank=True, null=True)  # Field name made lowercase.

    # 基表设置
    # 仪表口径
    # dn           = models.CharField(db_column='dn', max_length=64, blank=True, null=True)  # Field name made lowercase.
    # 传感器系数
    transimeterfactor           = models.CharField(db_column='transimeterfactor', max_length=64, blank=True, null=True)  # Field name made lowercase.
    # 厂商标识代码
    manufacturercode           = models.CharField(db_column='manufacturercode', max_length=64, blank=True, null=True)  # Field name made lowercase.
    # 流量零点修正值
    # flowzerovalue           = models.CharField(db_column='flowzerovalue', max_length=64, blank=True, null=True)  # Field name made lowercase.
    # 小信号切除点
    smallsignalcutpoint           = models.CharField(db_column='smallsignalcutpoint', max_length=64, blank=True, null=True)  # Field name made lowercase.
    # 压力测量允许
    pressurepermit           = models.CharField(db_column='pressurepermit', max_length=64, blank=True, null=True)  # Field name made lowercase.
    # 流体测量方向
    flowdorient           = models.CharField(db_column='flowdorient', max_length=64, blank=True, null=True)  # Field name made lowercase.
    # 仪表维护日期
    maintaindate           = models.CharField(db_column='maintaindate', max_length=64, blank=True, null=True)  # Field name made lowercase.
    # 正向累积预置
    plusaccumupreset           = models.CharField(db_column='plusaccumupreset', max_length=64, blank=True, null=True)  # Field name made lowercase.
    # 流量测量单位
    flowmeasureunit           = models.CharField(db_column='flowmeasureunit', max_length=64, blank=True, null=True)  # Field name made lowercase.


    class Meta:
        managed = True
        db_table = 'meter'

    def __unicode__(self):
        return '%s'%(self.serialnumber)   

    def __str__(self):
        return '%s'%(self.serialnumber)    



# station manager



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

    # bgm = models.OneToOneField(Bigmeter,related_name='bigm',on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'station'

    def __unicode__(self):
        return '%s'%(self.username)  

    def __str__(self):
        return '%s'%(self.username)        

    @property
    def commaddr(self):
        if not self.meter and not selr.meter.simid and self.meter.simid.simcardNumber == "":
            return None
        return self.meter.simid.simcardNumber

    def flowData(self,startTime,endTime):
        flow_data = []
        if self.commaddr is None:
            return flow_data
        flows = HdbFlowData.objects.filter(commaddr=self.commaddr).filter(readtime__range=[startTime,endTime]).values_list("readtime","flux")

        return flows

    def flowData_Hour(self,startTime,endTime):
        flow_data = {}
        if self.commaddr is None:
            return flow_data

        hours = ['00','01','02','03','04','05','06','07','08','09,','10','11','12','13','14','15','16','17','18','19,','20','21','22','23']
        flows = HdbFlowDataHour.objects.filter(commaddr=self.commaddr).filter(hdate__range=[startTime,endTime]).values_list("hdate","dosage")
        if flows.count() == 0:
            for h in hours:
                fh = endTime[:11] + h
                flow_data[fh] = '-'
            return flow_data
        flow_dict = dict(flows)
        print('flow_dict',flow_dict)
        flows_keys = [k[11:] for k,v in flows ]
        
        print("print first",flows.first())
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
        print('pressures:',pressures)
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

# 按小时统计的聚合
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



    def realtimedata(self):

        rtflow = HdbFlowData.objects.filter(commaddr=self.commaddr).last()
        press = HdbPressureData.objects.filter(commaddr=self.commaddr).last()
        # obj= Model.objects.filter(testfield=12).order_by('-id')[0]

        return {
            "stationname":self.username,
            "belongto":self.belongto.name,
            "serialnumber":self.meter.serialnumber,
            "alarm":0,
            "status":self.meter.state,
            "dn":self.meter.dn,
            "readtime":rtflow.readtime if rtflow else '-',
            "collectperiod":self.meter.collectperiod,
            "updataperiod":self.meter.updataperiod,
            "influx":rtflow.flux if rtflow else '-',
            "plusflux":rtflow.plustotalflux if rtflow else '-',
            "revertflux":rtflow.reversetotalflux if rtflow else '-',
            "press":press.pressure if press else 0,
            "baseelectricity":0,
            "remoteelectricity":0,
            "signal":0,
            
        }



@receiver(post_save, sender=Station)
def ensure_bigmeter_exists(sender, **kwargs):
    if kwargs.get('created', False):
        instance=kwargs.get('instance')
        username= instance.username
        lng=instance.lng
        lat=instance.lat
        commaddr=instance.commaddr
        simid = instance.commaddr
        Bigmeter.objects.get_or_create(username=username,lng=lng,lat=lat,commaddr=commaddr,simid=simid)   
    else:
        # print("ensure_bigmeter_exists edit")
        instance=kwargs.get('instance')
        username= instance.username
        lng=instance.lng
        lat=instance.lat
        commaddr=instance.commaddr
        simid = instance.commaddr
        bigm = Bigmeter.objects.filter(commaddr=instance.commaddr)
        if bigm.exists():
        
            bigm.first().username= instance.username
            bigm.first().lng=instance.lng
            bigm.first().lat=instance.lat
            bigm.first().commaddr=instance.commaddr
            bigm.first().simid = instance.commaddr
            bigm.first().save()
        else:
            Bigmeter.objects.create(username=username,lng=lng,lat=lat,commaddr=commaddr,simid=simid)  
