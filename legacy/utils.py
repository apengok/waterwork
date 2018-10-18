# -*- coding:utf-8 -*-

import json
import datetime
import time
from django.db.models import Avg, Max, Min, Sum

from legacy.models import (District,Bigmeter,HdbFlowData,HdbFlowDataDay,HdbFlowDataMonth,HdbPressureData,
                            HdbWatermeterDay,HdbWatermeterMonth,Concentrator,Watermeter,
                            HdbWatermeterDay,HdbWatermeterMonth)


# .exclude(plustotalflux__icontains='429490176') 因为抄表系统处理负数的问题，数据库写入很多不正确的数据，负值貌似都写入了429490176，所以排除这些数据


def HdbFlow_day_use(commaddr,day):
    '''
        返回日用水量
        取出当日所有数据，用最后一笔数据的正向流量值减去第一条数据的差值得出当日用水量的值
    '''
    day_use = 0
    flows = HdbFlowData.objects.search(commaddr,day).exclude(plustotalflux__icontains='429490176').values_list('readtime','plustotalflux')
    print(flows)
    n=flows.count()
    if n > 0:
        day_use = float(flows[n-1][1]) - float(flows[0][1])
    return round(day_use,2)

def HdbFlow_day_hourly(commaddr,day):
    '''
        返回日整点用水量
        当前整点正向流量-上一整点正向流量
    '''
    flow_data = []
    
    etime = datetime.datetime.strptime(day.strip(),"%Y-%m-%d")
    stime = etime + datetime.timedelta(days=1)
    startTime =day + ' 00:00:00'
    endTime = stime.strftime("%Y-%m-%d") + ' 00:00:00'
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
    # print('zhengdian_value',zhengdian_value)
    diff_value=[]
    for i in range(len(zhengdian_value)-1):
        v = float(zhengdian_value[i+1]) - float(zhengdian_value[i])
        diff_value.append(round(v,2))

    # print('diff_value',diff_value)

    return diff_value

# 统计大表月用水量，从流量历史数据查询当月的数据，最后一条记录减去第一条记录的差值
def HdbFlow_month_use(commaddr,day):
    '''
        返回月用水量
        取出当月所有数据，用最后一笔数据的正向流量值减去第一条数据的差值得出当月用水量的值
    '''
    month_use = 0
    t1=time.time()
    flows = HdbFlowData.objects.search(commaddr,day).exclude(plustotalflux__icontains='429490176').values_list('readtime','plustotalflux')
    t2=time.time()
    # print('HdbFlow_month_use time elpse',t2-t1)
    # print(flows)
    n=flows.count()
    if n > 0:
        month_use = float(flows[n-1][1]) - float(flows[0][1])
    return round(month_use,2)



def HdbFlow_monthly(commaddr):
    '''
        返回过去一年内每月用水量
        取出当月所有数据，用最后一笔数据的正向流量值减去第一条数据的差值得出当月用水量的值
    '''
    today = datetime.date.today()
    endTime = today.strftime("%Y-%m")
    
    lastyear = datetime.datetime(year=today.year-1,month=today.month,day=today.day)
    startTime = lastyear.strftime("%Y-%m")

    data = []
    sub_dma_list = []
    
    monthly_data = {}
    def month_year_iter( start_month, start_year, end_month, end_year ):
        ym_start= 12*start_year + start_month
        ym_end= 12*end_year + end_month
        for ym in range( ym_start, ym_end ):
            y, m = divmod( ym, 12 )
            # yield y, m+1
            yield '{}-{:02d}'.format(y,m+1)
    
    month_list = list(month_year_iter(lastyear.month,lastyear.year,today.month,today.year))
    # mon = ['2017-11', '2017-12', '2018-01', '2018-02', '2018-03', '2018-04', '2018-05', '2018-06', '2018-07', '2018-08', '2018-09', '2018-10']
    today = datetime.date.today()
    # flows = HdbFlowData.objects.filter(commaddr=commaddr).filter(readtime__range=[month_list[0],today]).exclude(plustotalflux__icontains='429490176').values_list('readtime','plustotalflux')
    flows = HdbFlowData.objects.filter(commaddr=commaddr).filter(readtime__range=[month_list[0],today]).values_list('readtime','plustotalflux')
    # 一次获取整年的数据再按月统计，减少查询数据库次数，查询数据库比较耗时
    # print(list(month_list))
    t=0
    for m in month_list:

        if m not in monthly_data.keys():
            monthly_data[m] = 0
        
        month_flow_list = [float(f[1]) for f in flows if f[0][:7] == m]
        
        if len(month_flow_list) == 0:
            month_use = 0
        else:
            month_use = month_flow_list[-1] - month_flow_list[0] #HdbFlow_month_use(commaddr,m)
        
        monthly_data[m] = round(month_use,2)
    
    return monthly_data


# 直接从hdb_flow_month读取月用水量返回
def Hdbflow_from_hdbflowmonth(commaddr):
    '''
        返回过去一年内每月用水量
        取出当月所有数据，用最后一笔数据的正向流量值减去第一条数据的差值得出当月用水量的值
    '''
    today = datetime.date.today()
    endTime = today.strftime("%Y-%m")
    
    lastyear = datetime.datetime(year=today.year-1,month=today.month,day=today.day)
    startTime = lastyear.strftime("%Y-%m")

    data = []
    sub_dma_list = []
    
    monthly_data = {}
    def month_year_iter( start_month, start_year, end_month, end_year ):
        ym_start= 12*start_year + start_month
        ym_end= 12*end_year + end_month
        for ym in range( ym_start, ym_end ):
            y, m = divmod( ym, 12 )
            # yield y, m+1
            yield '{}-{:02d}'.format(y,m+1)
    
    month_list = list(month_year_iter(lastyear.month,lastyear.year,today.month,today.year))
    # mon = ['2017-11', '2017-12', '2018-01', '2018-02', '2018-03', '2018-04', '2018-05', '2018-06', '2018-07', '2018-08', '2018-09', '2018-10']
    today = datetime.date.today()
    # flows = HdbFlowData.objects.filter(commaddr=commaddr).filter(readtime__range=[month_list[0],today]).exclude(plustotalflux__icontains='429490176').values_list('readtime','plustotalflux')
    flows = HdbFlowDataMonth.objects.filter(commaddr=commaddr).filter(hdate__range=[month_list[0],today]).values_list('hdate','dosage')
    # 一次获取整年的数据再按月统计，减少查询数据库次数，查询数据库比较耗时
    # print(list(month_list))
    dict_month = dict(flows)
    t=0
    for m in month_list:

        if m not in monthly_data.keys():
            monthly_data[m] = 0
        
        
        if dict_month[m] is None:
            month_use = 0
        else:
            month_use = float(dict_month[m]) #HdbFlow_month_use(commaddr,m)
        
        monthly_data[m] = round(month_use,2)
    
    return monthly_data

# 计算小区月用水量：月统计表里面属于这个小区的表数据加起来
def hdb_watermeter_month(communityid,hdate):
    flows=HdbWatermeterMonth.objects.filter(communityid=communityid,hdate=hdate).aggregate(Sum('dosage'))
    flow=flows['dosage__sum']
    if flow is None:
        flow = 0
    return round(float(flow),2)

def hdb_watermeter_flow_monthly(communityid):
    today = datetime.date.today()
    endTime = today.strftime("%Y-%m")
    
    lastyear = datetime.datetime(year=today.year-1,month=today.month,day=today.day)
    startTime = lastyear.strftime("%Y-%m")
    monthly_data = {}
    def month_year_iter( start_month, start_year, end_month, end_year ):
        ym_start= 12*start_year + start_month
        ym_end= 12*end_year + end_month
        for ym in range( ym_start, ym_end ):
            y, m = divmod( ym, 12 )
            # yield y, m+1
            yield '{}-{:02d}'.format(y,m+1)
    
    month_list = list(month_year_iter(lastyear.month,lastyear.year,today.month,today.year))
    # mon = ['2017-11', '2017-12', '2018-01', '2018-02', '2018-03', '2018-04', '2018-05', '2018-06', '2018-07', '2018-08', '2018-09', '2018-10']
    today = datetime.date.today()
    
    for m in month_list:
        f = hdb_watermeter_month(communityid,m)
        monthly_data[m] = f

    return monthly_data