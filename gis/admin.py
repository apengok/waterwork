# -*- coding:utf-8 -*-

from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.FenceDistrict)
class FenceDistrictAdmin(admin.ModelAdmin):
    list_display = ['name','parent','belongto','ftype','createDataTime','createDataUsername','cid','pId','updateDataTime','updateDataUsername']




@admin.register(models.Polygon)
class PolygonAdmin(admin.ModelAdmin):
    list_display = ['name','polygonId','ftype','shape','pointSeqs','longitudes','latitudes','dma_no']


@admin.register(models.FenceShape)
class FenceShapeAdmin(admin.ModelAdmin):
    list_display = ['shapeId','name','zonetype','shape','dma_no','pointSeqs','longitudes','latitudes','lnglatQuery_LU','lnglatQuery_RD']

    fieldsets = (
        (None, {'fields': ('shapeId', 'name','zonetype','shape','dma_no')}),
        ('Polygon', {'fields': ('pointSeqs','longitudes','latitudes')}),
        ('Rectangle', {'fields': ('lnglatQuery_LU','lnglatQuery_RD')}),
        ('Circle', {'fields': ('centerPointLat','centerPointLng','centerRadius')}),
        ('Administrator', {'fields': ('province','city','district','administrativeLngLat')}),
    )