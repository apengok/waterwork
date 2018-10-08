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
    print("flowdata_cxc:",request.POST)

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
    # print(month_list)
    for m in month_list:
        # print (m)
        if m not in echart_data.keys():
            echart_data[m] = 0
    

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
        print('special process 文欣苑')

        # dma = dmas.first()
        dmareport = dma.dma_statistic()
        print('dmareport',dmareport)

        flowday = HdbWatermeterMonth.objects.filter(communityid=105).filter(hdate__range=[startTime,endTime])
        print("wm_flowday count",flowday.count())

        #fill echart data
        for de,value in flowday.values_list('hdate','dosage'):
            if de in echart_data.keys():
                o_data = echart_data[de]
                echart_data[de] = o_data + float(value)/10000

        

        flows = [f.dosage for f in flowday]
        hdates = [f.hdate[-2:] for f in flowday]
        hdates = hdates[::-1]

        flows_float = [float(f) for f in flows]
        flows_float = flows_float[::-1]
        flows_leak = [random.uniform(float(f)/10,float(f)/5 ) for f in flows]
        uncharged =[random.uniform(float(f)/10,float(f)/5 ) for f in flows]

        #表具信息
        
        total = sum(flows_float)
        total /= 10000
        influx = sum(flows_float)
        influx /=10000
        leak = sum(flows_leak)
        leak /=10000
        uncharg = sum(uncharged)
        uncharg /=10000
        sale = total - leak - uncharg
        cxc = total - sale
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
        total_total += total
        total_leak += leak
        total_uncharg += uncharg
        total_sale += sale
        total_cxc += cxc
        # total_cxc_percent += cxc_percent
        # total_leak_percent += leak_percent

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
    
    
        

        
    dma_name = '歙县自来水公司'
    for k in echart_data:
        v = echart_data[k]
        l = v/5
        u = v/4
        cp = 0
        if v != 0:
            cp = (l+u)/v * 100;
        print(k,v,l,u,cp)
        data.append({
            "hdate":k[-2:],
            "dosage":round(v-l-u,2),
            "assignmentName":dma_name,
            "color":"红色",
            "ratio":"null",
            "leak":round(l,2),
            "uncharged":round(u,2),
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

