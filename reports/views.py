# -*- coding: utf-8 -*-

import json
import random
import datetime

from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView,DeleteView,FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin,UserPassesTestMixin
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect

from waterwork.mixins import AjaxableResponseMixin
from legacy.models import District,Bigmeter,HdbFlowData,HdbFlowDataDay,HdbFlowDataMonth,HdbPressureData

from accounts.models import User,MyRoles
from legacy.models import District,Bigmeter,HdbFlowData,HdbFlowDataDay,HdbFlowDataMonth,HdbPressureData,HdbWatermeterDay,HdbWatermeterMonth,Concentrator,Watermeter
from dmam.models import DMABaseinfo,DmaStations,Station
from entm.models import Organizations

# Create your views here.

class QuerylogView(LoginRequiredMixin,TemplateView):
    template_name = "reports/querylog.html"

    def get_context_data(self, *args, **kwargs):
        context = super(QuerylogView, self).get_context_data(*args, **kwargs)
        context["page_title"] = "日志查询"
        context["page_menu"] = "统计报表"
        
        return context  

class AlarmView(LoginRequiredMixin,TemplateView):
    template_name = "reports/alarm.html"

    def get_context_data(self, *args, **kwargs):
        context = super(AlarmView, self).get_context_data(*args, **kwargs)
        context["page_title"] = "报警报表"
        context["page_menu"] = "统计报表"
        
        return context  

class BiguserView(LoginRequiredMixin,TemplateView):
    template_name = "reports/biguser.html"

    def get_context_data(self, *args, **kwargs):
        context = super(BiguserView, self).get_context_data(*args, **kwargs)
        context["page_title"] = "大用户报表"
        context["page_menu"] = "统计报表"
        
        return context  

class DmastaticsView(LoginRequiredMixin,TemplateView):
    template_name = "reports/dmastatics.html"

    def get_context_data(self, *args, **kwargs):
        context = super(DmastaticsView, self).get_context_data(*args, **kwargs)
        context["page_title"] = "DMA报表"
        context["page_menu"] = "统计报表"

        bigmeter = Bigmeter.objects.first()
        context["station"] = bigmeter.username
        context["organ"] = "歙县自来水公司"
        
        return context  


def dmareport(request):
    print("dmareport:",request.POST)

    stationid = request.POST.get("station") or '' # DMABaseinfo pk
    endTime = request.POST.get("endTime") or ''
    treetype = request.POST.get("treetype") or ''

    today = datetime.date.today()
    endTime = today.strftime("%Y-%m")
    
    lastyear = datetime.datetime(year=today.year-1,month=today.month,day=today.day)
    startTime = lastyear.strftime("%Y-%m")

    data = []
    sub_dma_list = []
    print(startTime,'-',endTime)
    # etime = datetime.datetime.strptime(endTime.strip(),"%Y-%m-%d")
    # stime = etime - datetime.timedelta(days=10)
    # startTime = stime.strftime("%Y-%m-%d")
    echart_data = {}
    def month_year_iter( start_month, start_year, end_month, end_year ):
        ym_start= 12*start_year + start_month
        ym_end= 12*end_year + end_month
        for ym in range( ym_start, ym_end ):
            y, m = divmod( ym, 12 )
            # yield y, m+1
            yield '{}-{:02d}'.format(y,m+1)

    month_list = month_year_iter(lastyear.month,lastyear.year,today.month,today.year)
    print(month_list)
    for m in month_list:
        # print (m)
        if m not in echart_data.keys():
            echart_data[m] = 0
    
    hdates = [f[-2:] for f in echart_data.keys()]
    # hdates = hdates[::-1]
    if treetype == 'dma':
        # distict = District.objects.get(id=int(stationid))
        # bigmeter = distict.bigmeter.first()
        dmas = DMABaseinfo.objects.filter(pk=int(stationid))
        
        
    else:
        # dma = DMABaseinfo.objects.first()
        # dmastation = dma.dmastation.first()
        # comaddr = dmastation.station_id

        if treetype == '':
            organ = Organizations.objects.first()

        if treetype == 'group':
            organ = Organizations.objects.get(cid=stationid)

        organs = organ.get_descendants(include_self=True)

        dmas = None
        for o in organs:
            if dmas is None:
                dmas = o.dma.all()
            else:
                dmas |= o.dma.all()
    print('dmas:',dmas)

    

    total_influx       = 0
    total_outflux       = 0
    total_total        = 0
    total_leak         = 0
    total_uncharg      = 0
    total_sale         = 0
    total_cxc          = 0
    total_cxc_percent  = 0
    total_leak_percent = 0
    total_broken_pipe  = 0
    total_mnf          = 0
    total_back_leak    = 0
    huanbi=0
    tongbi=0
    mnf=1.2
    back_leak=1.8
    broken_pipe=0
    other_leak = 0

    if len(dmas) == 0:
        ret = {"exceptionDetailMsg":"null",
            "msg":"没有dma分区信息",
            "obj":{
                "online":data, #reverse
                "influx":round(total_influx,2),
                "total":round(total_total,2),
                "leak":round(total_leak,2),
                "uncharg":round(total_uncharg,2),
                "sale":round(total_sale,2),
                "cxc":round(total_cxc,2),
                "cxc_percent":round(total_cxc_percent,2),
                "broken_pipe":broken_pipe,
                "back_leak":back_leak,
                "mnf":mnf,
                "leak_percent":round(total_leak_percent,2),
                "stationsstastic":sub_dma_list

            },
            "success":0}

    
    
        return HttpResponse(json.dumps(ret))

    
    # if dmas.first().dma_name == '文欣苑' or dmas.first().dma_no== '301':
    for dma in dmas:
        print('dma static',dma)

        # dma = dmas.first()
        dmareport = dma.dma_statistic()
        print('dmareport',dmareport)

        water_in = dmareport['water_in']
        water_out = dmareport['water_out']
        water_sale = dmareport['water_sale']
        water_uncount = dmareport['water_uncount']
        monthly_in = dmareport['monthly_in']    #进水表每月流量
        monthly_out = dmareport['monthly_out']  #出水表每月流量
        monthly_sale = dmareport['monthly_sale']  #贸易结算表每月流量
        monthly_uncount = dmareport['monthly_uncount'] #未计费水表每月流量

        
        

        if len(monthly_in) == 0:
            monthly_in_flow = [0 for i in range(12)]
        else:
            monthly_in_flow = [monthly_in[k] for k in monthly_in.keys()]
        if len(monthly_out) == 0:
            monthly_out_flow = [0 for i in range(12)]
        else:
            monthly_out_flow = [monthly_out[k] for k in monthly_out.keys()]
        # 供水量  （分区内部进水表要减去自己内部出水表才等于这个分区的供水量）
        monthly_water = [monthly_in_flow[i]-monthly_out_flow[i] for i in range(len(monthly_in_flow))]
        # 售水量
        if len(monthly_sale) == 0:
            monthly_sale_flow = [0 for i in range(12)]
        else:
            monthly_sale_flow = [monthly_sale[k] for k in monthly_sale.keys()]
        # 未计费水量
        if len(monthly_uncount) == 0:
            monthly_uncount_flow = [0 for i in range(12)]
        else:
            monthly_uncount_flow =[monthly_uncount[k] for k in monthly_uncount.keys()]

        # 漏损量 = 供水量-售水量-未计费水量
        monthly_leak_flow = [monthly_water[i]-monthly_sale_flow[i]-monthly_uncount_flow[i] for i in range(len(monthly_water))]

        
        
        influx = sum(monthly_in_flow)   #进水总量
        influx /=10000
        outflux = sum(monthly_out_flow) #出水总量
        outflux /=10000
        total = influx - outflux    #供水量
        # total /= 10000
        sale = sum(monthly_sale_flow)   #售水量
        sale /= 10000
        uncharg = sum(monthly_uncount_flow) #未计费水量
        uncharg /=10000
        leak = sum(monthly_leak_flow)   #漏损量
        leak /=10000
        
        cxc = total - sale  #产销差 = 供水量-售水量
        #产销差率 = （供水量-售水量）/月供水量*100%
        if total != 0:
            cxc_percent = (cxc / total)*100 
        else:
            cxc_percent = 0
        huanbi=0
        if total != 0 :
            leak_percent = (leak * 100)/total
        else:
            leak_percent = 0
        tongbi=0
        mnf=1.2
        back_leak=1.8
        broken_pipe=0
        other_leak = 0

        total_influx += influx
        total_outflux += outflux
        total_total += total
        total_leak += leak
        total_uncharg += uncharg
        total_sale += sale
        total_cxc += cxc
        print('total_influx',total_influx,water_in)
        print('total_outflux',total_outflux,water_out)
        print('total_total',total_total)
        print('total_leak',total_leak)
        print('total_uncharg',total_uncharg,water_uncount)
        print('total_sale',total_sale,water_sale)
        print('total_cxc',total_cxc)
        

        #记录每个dma分区的统计信息
        sub_dma_list.append({
                    "organ":dma.dma_name,
                    # "influx":round(influx,2),
                    "total":round(total,2),
                    "sale":round(sale,2),
                    "uncharg":round(uncharg,2),
                    "leak":round(leak,2),
                    "cxc":round(cxc,2),
                    "cxc_percent":round(cxc_percent,2),
                    "huanbi":round(huanbi,2),
                    "leak_percent":round(leak_percent,2),
                    "tongbi":round(tongbi,2),
                    "mnf":round(mnf,2),
                    "back_leak":round(back_leak,2),
                    "other_leak":round(other_leak,2),
                    "statis_date":endTime,
                })
    
    
        

    # 产销差 = （供水量-售水量）/月供水量*100%        
    dma_name = '歙县自来水公司'
    for i in range(len(monthly_in_flow)):
        cp = 0
        if monthly_water[i] != 0:
            cp = (monthly_water[i] - monthly_sale_flow[i])/monthly_water[i] *100
        data.append({
            "hdate":hdates[i],
            "dosage":monthly_sale_flow[i]/10000,
            "assignmentName":dma_name,
            "color":"红色",
            "ratio":"null",
            "leak":monthly_leak_flow[i]/10000,
            "uncharged":monthly_uncount_flow[i]/10000,
            "cp_month":round(cp,2)
            })    
    

    
    if total_total != 0:
        total_cxc = total_total - total_sale
        total_cxc_percent = (total_cxc / total_total)*100
        total_leak_percent = (total_leak * 100)/total_total

    ret = {"exceptionDetailMsg":"null",
            "msg":"null",
            "obj":{
                "online":data, #reverse
                "influx":round(total_influx,2),
                "outflux":round(total_outflux,2),
                "total":round(total_total,2),
                "leak":round(total_leak,2),
                "uncharg":round(total_uncharg,2),
                "sale":round(total_sale,2),
                "cxc":round(total_cxc,2),
                "cxc_percent":round(total_cxc_percent,2),
                "broken_pipe":broken_pipe,
                "back_leak":back_leak,
                "mnf":mnf,
                "leak_percent":round(total_leak_percent,2),
                "stationsstastic":sub_dma_list

            },
            "success":1}

    
    
    return HttpResponse(json.dumps(ret))


class WenxinyuanView(TemplateView):
    template_name = "reports/wenxinyuan.html"

    def get_context_data(self, *args, **kwargs):
        context = super(WenxinyuanView, self).get_context_data(*args, **kwargs)
        context["page_title"] = "DMA报表"
        context["page_menu"] = "统计报表"

        bigmeter = Bigmeter.objects.first()
        context["station"] = bigmeter.username
        context["organ"] = "歙县自来水公司"
        
        return context  

class FlowsView(LoginRequiredMixin,TemplateView):
    template_name = "reports/flows.html"

    def get_context_data(self, *args, **kwargs):
        context = super(FlowsView, self).get_context_data(*args, **kwargs)
        context["page_title"] = "流量报表"
        context["page_menu"] = "统计报表"
        
        return context  

class WatersView(LoginRequiredMixin,TemplateView):
    template_name = "reports/waters.html"

    def get_context_data(self, *args, **kwargs):
        context = super(WatersView, self).get_context_data(*args, **kwargs)
        context["page_title"] = "水量报表"
        context["page_menu"] = "统计报表"
        
        return context  

class BiaowuView(LoginRequiredMixin,TemplateView):
    template_name = "reports/biaowu.html"

    def get_context_data(self, *args, **kwargs):
        context = super(BiaowuView, self).get_context_data(*args, **kwargs)
        context["page_title"] = "表务表况"
        context["page_menu"] = "统计报表"
        
        return context  

class VehicleView(LoginRequiredMixin,TemplateView):
    template_name = "reports/vehicle.html"

    def get_context_data(self, *args, **kwargs):
        context = super(VehicleView, self).get_context_data(*args, **kwargs)
        context["page_title"] = "车辆报表"
        context["page_menu"] = "统计报表"
        
        return context  

class BigdataView(LoginRequiredMixin,TemplateView):
    template_name = "reports/bigdata.html"

    def get_context_data(self, *args, **kwargs):
        context = super(BigdataView, self).get_context_data(*args, **kwargs)
        context["page_title"] = "大数据报表"
        context["page_menu"] = "统计报表"
        
        return context  

