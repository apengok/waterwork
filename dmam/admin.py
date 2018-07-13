from django.contrib import admin
from . models import WaterUserType,DMABaseinfo
# Register your models here.


@admin.register(WaterUserType)
class WaterUserTypeAdmin(admin.ModelAdmin):
    list_display = ['usertype','explains']



@admin.register(DMABaseinfo)
class DMABaseinfoAdmin(admin.ModelAdmin):
    list_display = ['dma_no','dma_name','creator','create_date','belongto']
