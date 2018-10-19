# -*- coding: utf-8 -*-

import json
import random
import datetime
import time 

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
from legacy.utils import generat_year_month_from

# Create your views here.

def dmatree(request):   
    organtree = []
    
    stationflag = request.GET.get("isStation") or ''
    dmaflag = request.GET.get("isDma") or ''
    
    
    organs = Organizations.objects.get(name="歙县自来水公司")
    
    print("dmatree",organs)
    for o in organs.get_descendants(include_self=True):
        if o.dma.exists():
            p_dma_no = o.dma.first().dma_no
        else:
            p_dma_no = ''
        organtree.append({
            "name":o.name,
            "id":o.cid,
            "pId":o.pId,
            "districtid":'',
            "type":"group",
            "dma_no":p_dma_no,  #如果存在dma分区，分配第一个dma分区的dma_no，点击数条目的时候使用
            "icon":"/static/virvo/resources/img/wenjianjia.png",
            "uuid":o.uuid
        })

        #dma
        if dmaflag == '1':
            for d in o.dma.all():
                organtree.append({
                "name":d.dma_name,
                "id":d.pk,
                "districtid":d.pk,
                "pId":o.cid,
                "type":"dma",
                "dma_no":d.dma_no,
                "icon":"/static/virvo/resources/img/dma.png",
                "uuid":''
            })

        #station
        if stationflag == '1':
            for s in o.station_set.all():
                # if s.dmaid is None: #已分配dma分区的不显示
                organtree.append({
                    "name":s.username,
                    "id":s.pk,
                    "districtid":'',
                    "pId":o.cid,
                    "type":"station",
                    "dma_no":'',
                    "icon":"/static/virvo/resources/img/station.png",
                    "uuid":''
                })

    # district
    # districts = District.objects.all()
    # for d in districts:
    #     organtree.append({
    #         "name":d.name,
    #         "id":d.id,
    #         "districtid":d.id,
    #         "pId":organs.cid,
    #         "type":"district",
    #         "icon":"/static/virvo/resources/img/u8836.png",
    #         "uuid":''
    #     })
        # bigmeters = Bigmeter.objects.filter(districtid=d.id)
        # for b in bigmeters:
        #     organtree.append({
        #     "name":b.username,
        #     "id":b.userid,
        #     "stationid":b.userid,
        #     "pId":d.id,
        #     "type":"station",
        #     "icon":"/static/virvo/resources/img/u8836.png",
        #     "uuid":''
        # })

    #bigmeter

    
    result = dict()
    result["data"] = organtree
    
    # print(json.dumps(result))
    
    return HttpResponse(json.dumps(organtree))


class DmastaticsView(TemplateView):
    template_name = "shexian/dmareport.html"

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
    
    # echart_data = {}
    # def month_year_iter( start_month, start_year, end_month, end_year ):
    #     ym_start= 12*start_year + start_month
    #     ym_end= 12*end_year + end_month
    #     for ym in range( ym_start, ym_end ):
    #         y, m = divmod( ym, 12 )
    #         # yield y, m+1
    #         yield '{}-{:02d}'.format(y,m+1)

    # month_list = list(month_year_iter(lastyear.month,lastyear.year,today.month,today.year))
    # # print(month_list)
    # for m in month_list:
    #     # print (m)
    #     if m not in echart_data.keys():
    #         echart_data[m] = 0
    
    # hdates = [f[-2:] for f in echart_data.keys()]
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

    hdates=[]
    # if dmas.first().dma_name == '文欣苑' or dmas.first().dma_no== '301':
    for dma in dmas:
        
        # dma = dmas.first()
        t1 = time.time()
        cre_data = datetime.datetime.strptime("2018-06-01","%Y-%m-%d")
        # cre_data = datetime.datetime.strptime(dma.create_date,"%Y-%m-%d")
        month_list = generat_year_month_from(cre_data.month,cre_data.year)
        print("create data month_list",month_list)
        hdates = [f[-2:] for f in month_list]

        dmareport = dma.dma_statistic(month_list)
        print('time elapse ',time.time() - t1)
        
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
        # print('total_influx',total_influx,water_in)
        # print('total_outflux',total_outflux,water_out)
        # print('total_total',total_total)
        # print('total_leak',total_leak)
        # print('total_uncharg',total_uncharg,water_uncount)
        # print('total_sale',total_sale,water_sale)
        # print('total_cxc',total_cxc)
        
        # dma 每个月统计
        if treetype == "dma":
            print("treetype processsdf")
            print(month_list)
            for m in month_list:
                print(m)
                m_in = monthly_in[m]/10000
                m_out = monthly_out[m]/10000
                m_sale = monthly_sale[m]/10000
                m_uncount = monthly_uncount[m]/10000
                m_total = m_in - m_out #供水量=进水总量-出水总量
                m_leak= m_total - m_sale - m_uncount # 漏损量 = 供水量-售水量-未计费水量
                m_cxc = m_total - m_sale    #产销差 = 供水量-售水量
                if m_total == 0:
                    m_cxc_percent = 0
                else:
                    m_cxc_percent = (m_cxc/m_total) * 100     #产销差率 = （供水量-售水量）/供水量*100%

                if m_total != 0 :
                    m_leak_percent = (m_leak * 100)/m_total
                else:
                    m_leak_percent = 0

                sub_dma_list.append({
                    "organ":dma.dma_name,
                    # "influx":round(influx,2),
                    "total":round(m_total,2),#供水量
                    "sale":round(m_sale,2),#售水量
                    "uncharg":round(m_uncount,2),#未计费水量
                    "leak":round(m_leak,2),#漏损量
                    "cxc":round(m_cxc,2),#产销差 = 供水量-售水量
                    "cxc_percent":round(m_cxc_percent,2),#产销差率
                    "huanbi":round(huanbi,2),
                    "leak_percent":round(m_leak_percent,2),
                    "tongbi":round(tongbi,2),
                    "mnf":round(mnf,2),
                    "back_leak":round(back_leak,2),
                    "other_leak":round(other_leak,2),
                    "statis_date":m,
                })
        else:
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
                "stationsstastic":sub_dma_list[::-1]

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


class MnfView(TemplateView):
    template_name = "shexian/mnf.html"

    def get_context_data(self, *args, **kwargs):
        context = super(MnfView, self).get_context_data(*args, **kwargs)
        context["page_menu"] = "数据监控"
        # context["page_submenu"] = "组织和用户管理"
        context["page_title"] = "最小夜间流量分析（MNF）"

        bigmeter = Bigmeter.objects.first()
        dma = DMABaseinfo.objects.first()
        context["station"] = dma.dma_name
        context["organ"] = dma.belongto
        

        return context      



def flowdata_mnf(request):

    print("shexian flowdata_mnf:",request.POST)

    stationid = request.GET.get("station") # DMABaseinfo pk
    treetype = request.GET.get("treetype")
    startTime = request.GET.get("startTime")
    endTime = request.GET.get("endTime")

    data = []

    if treetype == 'dma':
        # distict = District.objects.get(id=int(stationid))
        # bigmeter = distict.bigmeter.first()
        dmas = DMABaseinfo.objects.filter(pk=int(stationid))
        
        
    else:
        # dma = DMABaseinfo.objects.first()
        # dmastation = dma.dmastation.first()
        # comaddr = dmastation.station_id

        if treetype == '':
            organ = Organizations.objects.filter(name="歙县自来水公司").first()

        if treetype == 'group':
            organ = Organizations.objects.get(cid=stationid)

        organs = organ.get_descendants(include_self=True)

        dmas = None
        for o in organs:
            if dmas is None:
                dmas = o.dma.all()
            else:
                dmas |= o.dma.all()
    # print('dmas:',dmas)

    ret = {"exceptionDetailMsg":"null",
            "msg":"没有dma分区信息",
            "obj":{
                "online":data, #reverse
                
            },
            "success":0}

    if len(dmas) == 0:
        return HttpResponse(json.dumps(ret))

    # if stationid != '':
    #     # distict = District.objects.get(id=int(stationid))
    #     # bigmeter = distict.bigmeter.first()
    #     dma = DMABaseinfo.objects.get(pk=int(stationid))
    #     print('DMA',dma,dma.dmastation)
    #     dmastation = dma.dmastation.first()
    #     comaddr = dmastation.station_id
    # else:
    #     dma = DMABaseinfo.objects.first()
    #     dmastation = dma.dmastation.first()
    #     comaddr = dmastation.station_id


    dma = dmas.first()
    if dma.station_set.count() == 0:
        return HttpResponse(json.dumps(ret))

    meter_in = dma.station_set.filter(dmametertype='进水表')
    if meter_in.exists():
        dmastation = meter_in.first()
    else:
        meter_out = dma.station_set.filter(dmametertype='出水表')
        if meter_out.exists():
            dmastation = meter_out.first()
        else:
            meter_sale = dma.station_set.filter(dmametertype='贸易结算表')
            if meter_sale.exists():
                dmastation = meter_sale.first()
            else:
                meter_uncount = dma.station_set.filter(dmametertype='未计费水表')
                if meter_uncount.exists():
                    dmastation = meter_uncount.first()
                else:
                    dmastation = None
    if dmastation is None:
        return HttpResponse(json.dumps(ret))

    comaddr = dmastation.meter.simid.simcardNumber
    
    
    
    # if comaddr:
        # comaddr = bigmeter.commaddr
    flowday_stastic = HdbFlowDataDay.objects.filter(commaddr=comaddr)
    flowday = HdbFlowData.objects.filter(commaddr=comaddr).filter(readtime__range=[startTime,endTime])

    #pressure
    pressures = HdbPressureData.objects.filter(commaddr=comaddr).filter(readtime__range=[startTime,endTime])
    press = [round(float(f.pressure),2) for f in pressures]
    # print('pressures:',pressures)

    flows = [f.flux for f in flowday]
    hdates = [f.readtime for f in flowday]

    # print('mnf hdates',hdates)
    show_flag=1
    tmp = ''
    count_cnt = 1
    for i in range(len(hdates)):
        if i == 0:
            continue
        h = hdates[i]
        if tmp != h[:10]:
            tmp = h[:10]
            count_cnt += 1
            if count_cnt == 5:
                hdates[i] = h[:10] + " 00:00:00"
            else:
                hdates[i]=''
        


    flows_float = [round(float(f),2) for f in flows]
    flows_float = flows_float[::-1]
    

    #参考MNF
    ref_mnf = 4.46
    #MNF
    mnf = 8.63
    #表具信息
    
    #MNF/ADD
    mnf_add = 51
    #背景漏损
    back_leak = 4.46
    
    #设定报警
    alarm_set = 12

    #staticstic data
    #当天用水量
    today_use = 0
    #昨日用水量
    yestoday_use = 0
    #去年同期用水量
    last_year_same = 0
    #同比增长
    tongbi = 0
    #环比增长
    huanbi = 0
    #最大值
    maxflow = 0
    #最小值
    minflow = 0
    #平均值
    average = 0

    maxflow = max(flows_float) if len(flows_float)>0 else 0
    minflow = min(flows_float) if len(flows_float)>0 else 0
    average = sum(flows_float)/len(flows) if len(flows_float)>0 else 0
    mnf = minflow
    ref_mnf = mnf/2
    back_leak = ref_mnf * 0.8

    for i in range(len(flows_float)):
        data.append({
            "hdate":hdates[i],
            "dosage":flows_float[i],
            "assignmentName":dma.dma_name,
            "color":"红色",
            "ratio":"null",
            "maxflow":maxflow,
            "average":average,
            "mnf":mnf,
            "ref_mnf":ref_mnf,
            "press":press[i] if i < len(press) else 0
            })
            
    

    today = datetime.date.today()
    today_str = today.strftime("%Y-%m-%d")
    today_flow = HdbFlowDataDay.objects.filter(hdate=today_str)
    
    if today_flow.exists():
        today_use = today_flow.first().dosage

    yestoday = today - datetime.timedelta(days=1)
    yestoday_str = yestoday.strftime("%Y-%m-%d")
    yestoday_flow = HdbFlowDataDay.objects.filter(hdate=yestoday_str)
    if yestoday_flow.exists():
        yestoday_use = yestoday_flow.first().dosage

    lastyear = datetime.datetime(year=today.year-1,month=today.month,day=today.day)
    lastyear_str = lastyear.strftime("%Y-%m-%d")
    lastyear_flow = HdbFlowDataDay.objects.filter(hdate=lastyear_str)
    if lastyear_flow.exists():
        last_year_same = lastyear_flow.first().dosage
    tongbi = float(today_use) - float(last_year_same)
    huanbi = float(today_use) - float(yestoday_use)
    



    ret = {"exceptionDetailMsg":"null",
            "msg":"null",
            "obj":{
                "online":data, #reverse
                "today_use":round(float(today_use),2),
                "yestoday_use":round(float(yestoday_use),2),
                "last_year_same":round(float(last_year_same),2),
                "tongbi":round(tongbi,2),
                "huanbi":round(huanbi,2),
                "maxflow":round(maxflow,2),
                "minflow":round(minflow,2),
                "average":round(average,2),
                "mnf":round(mnf,2),
                "mnf_add":round(mnf_add,2),
                "ref_mnf":round(ref_mnf,2),
                "back_leak":round(back_leak,2),
                "alarm_set":round(alarm_set,2),


            },
            "success":1}

    
    
    return HttpResponse(json.dumps(ret))