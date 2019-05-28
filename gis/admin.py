# -*- coding:utf-8 -*-

from django.contrib import admin
from . import models
from waterwork.mixins import ExportCsvMixin
import json

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
    list_display = ['shapeId','name','zonetype','shape','dma_no','geomjson','pointSeqs','longitudes','latitudes','lnglatQuery_LU','lnglatQuery_RD']
    actions = ['export_as_csv','convert_to_geomjson','mercatro_to_geomjson']

    fieldsets = (
        (None, {'fields': ('shapeId', 'name','zonetype','shape','dma_no')}),
        ('Polygon', {'fields': ('pointSeqs','longitudes','latitudes')}),
        ('Rectangle', {'fields': ('lnglatQuery_LU','lnglatQuery_RD')}),
        ('Circle', {'fields': ('centerPointLat','centerPointLng','centerRadius')}),
        ('Administrator', {'fields': ('province','city','district','administrativeLngLat')}),
    )

    def convert_to_geomjson(self,request,queryset):
        rows_updated = queryset.count()

        
        
        for q in queryset:
            try:
                q.geomjson = json.dumps(q.geojsondata())
                q.save()
            except Exception as e:
                print('error appear:',e)
                pass
        if rows_updated == 1:
            message_bit = "1 item was"
        else:
            message_bit = "%s items were" % rows_updated
        self.message_user(request, "%s successfully updated as nomal." % message_bit)
    convert_to_geomjson.short_description = 'coordinates to geomjson' 

    def mercatro_to_geomjson(self,request,queryset):
        rows_updated = queryset.count()

        
        
        for q in queryset:
            try:
                q.geomjson = json.dumps(q.geojsondata_mercator())
                q.save()
            except Exception as e:
                print('error appear:',e)
                pass
        if rows_updated == 1:
            message_bit = "1 item was"
        else:
            message_bit = "%s items were" % rows_updated
        self.message_user(request, "%s successfully updated as nomal." % message_bit)
    mercatro_to_geomjson.short_description = 'MerCato to geomjson' 