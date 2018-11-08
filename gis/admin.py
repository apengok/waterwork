# -*- coding:utf-8 -*-

from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.FenceDistrict)
class FenceDistrictAdmin(admin.ModelAdmin):
    list_display = ['name','parent','ftype','createDataTime','createDataUsername','cid','pId','updateDataTime','updateDataUsername']




@admin.register(models.Polygon)
class PolygonAdmin(admin.ModelAdmin):
    list_display = ['name','polygonId','ftype','shape','pointSeqs','longitudes','latitudes','dma_no']