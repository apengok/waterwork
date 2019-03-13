# -*- coding:utf-8 -*-

from django.contrib import admin
from . import models
from waterwork.mixins import ExportCsvMixin

# Register your models here.

@admin.register(models.FenceDistrict)
class FenceDistrictAdmin(admin.ModelAdmin,ExportCsvMixin):
    list_display = ['name','parent','belongto','ftype','createDataTime','createDataUsername','cid','pId','updateDataTime','updateDataUsername']
    actions = ['export_as_csv']




@admin.register(models.Polygon)
class PolygonAdmin(admin.ModelAdmin):
    list_display = ['name','polygonId','ftype','shape','pointSeqs','longitudes','latitudes','dma_no']


@admin.register(models.FenceShape)
class FenceShapeAdmin(admin.ModelAdmin,ExportCsvMixin):
    list_display = ['shapeId','name','zonetype','shape','dma_no','pointSeqs','longitudes','latitudes','lnglatQuery_LU','lnglatQuery_RD']
    actions = ['export_as_csv']

    fieldsets = (
        (None, {'fields': ('shapeId', 'name','zonetype','shape','dma_no')}),
        ('Polygon', {'fields': ('pointSeqs','longitudes','latitudes')}),
        ('Rectangle', {'fields': ('lnglatQuery_LU','lnglatQuery_RD')}),
        ('Circle', {'fields': ('centerPointLat','centerPointLng','centerRadius')}),
        ('Administrator', {'fields': ('province','city','district','administrativeLngLat')}),
    )