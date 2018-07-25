from django.contrib import admin
from . models import WaterUserType,DMABaseinfo,DmaStations,Meter,Station
# Register your models here.


@admin.register(WaterUserType)
class WaterUserTypeAdmin(admin.ModelAdmin):
    list_display = ['usertype','explains']


@admin.register(DmaStations)
class DmaStationsAdmin(admin.ModelAdmin):
    list_display = ['dmaid','station_id','meter_type']


@admin.register(DMABaseinfo)
class DMABaseinfoAdmin(admin.ModelAdmin):
    list_display = ['dma_no','dma_name','creator','create_date','belongto']


@admin.register(Meter)
class MeterAdmin(admin.ModelAdmin):
    list_display = ['serialnumber','simid','dn','metertype','belongto']


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ['username','usertype','biguser','focus','madedate']