# -*- coding:utf-8 -*-

from django.contrib import admin
from . models import WaterUserType,DMABaseinfo,DmaStation,Meter,Station,SimCard,DmaGisinfo,VCommunity,VConcentrator,VWatermeter,VPressure,VSecondWater
# Register your models here.
from legacy.models import Bigmeter,District

@admin.register(WaterUserType)
class WaterUserTypeAdmin(admin.ModelAdmin):
    list_display = ['usertype','explains']


@admin.register(DmaStation)
class DmaStationAdmin(admin.ModelAdmin):
    list_display = ['dmaid','station_id','meter_type','station_type']


@admin.register(DMABaseinfo)
class DMABaseinfoAdmin(admin.ModelAdmin):
    list_display = ['dma_no','dma_level','dma_name','creator','create_date','belongto']
    search_fields = ("dma_no","dma_name" )


@admin.register(Meter)
class MeterAdmin(admin.ModelAdmin):
    list_display = ['serialnumber','simid','protocol','dn','metertype','belongto']

    search_fields = ('serialnumber',)
    list_filter = ('protocol',) 

@admin.register(VPressure)
class VPressureAdmin(admin.ModelAdmin):
    list_display = ['username','serialnumber','simid','dn','metertype','belongto']


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    actions = ['sync_bigmeter']
    list_display = ['username','usertype','biguser','focus','madedate','meter','belongto','dmametertype']

    search_fields = ("username","meter__serialnumber","meter__simid__simcardNumber" )

    def sync_bigmeter(self,request,queryset):
        # rows_updated = queryset.update(meterstate='正常')
        rows_updated = queryset.count()
        district = District.objects.first()
        districtid = district.id
        for q in queryset:
            try:
                username= q.username
                lng=q.lng
                lat=q.lat
                commaddr=q.commaddr
                simid = q.commaddr
                Bigmeter.objects.get_or_create(username=username,lng=lng,lat=lat,commaddr=commaddr,simid=simid,districtid=districtid,alarmoffline=1,alarmonline=1,
            alarmgprsvlow=1,alarmmetervlow=1,alarmuplimitflow=1,alarmgpflow=1,pressurealarm=1,dosagealarm=1) 
            except:
                print('error appear:',username)
                pass
        if rows_updated == 1:
            message_bit = "1 item was"
        else:
            message_bit = "%s items were" % rows_updated
        self.message_user(request, "%s successfully updated as nomal." % message_bit)
    sync_bigmeter.short_description = 'create bigmeter' 

    def get_form(self, request, obj=None, **kwargs):
        form = super(StationAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['dmaid'].required = False
        return form

@admin.register(SimCard)
class SimCardAdmin(admin.ModelAdmin):
    list_display = ['simcardNumber','belongto','isStart','iccid','imei','imsi','operator','simFlow','openCardTime','endTime','remark']


@admin.register(DmaGisinfo)
class DmaGisInfoAdmin(admin.ModelAdmin):
    list_display = ['dma_no','geodata','strokeColor','fillColor']

@admin.register(VConcentrator)
class VConcentratorAdmin(admin.ModelAdmin):
    list_display = ['id','name','belongto','commaddr','address','lng','lat','coortype','model','serialnumber','manufacturer','madedate']
    search_fields = ['name']


class MembershipInline(admin.TabularInline):
    model = VCommunity.vconcentrators.through


@admin.register(VCommunity)
class VCommunityAdmin(admin.ModelAdmin):
    inlines = [
        MembershipInline,
    ]
    list_display = ['id','name','belongto','commutid','amrs_commutid','address','parent','outter']

    search_fields = ['name']

@admin.register(VWatermeter)
class VWatermeterAdmin(admin.ModelAdmin):
    list_display = ['name','belongto','communityid','communityidnew','waterid','amrs_waterid','outter_communityid','concentrator','numbersth','buildingname','roomname','wateraddr','serialnumber','madedate']
    search_fields = ['name','communityid__name','id','wateraddr',]


@admin.register(VSecondWater)
class VSecondWaterAdmin(admin.ModelAdmin):
    list_display = ['name','belongto','coortype','lng','lat',]
    search_fields = ['name']