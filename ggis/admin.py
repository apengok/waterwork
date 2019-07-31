# -*- coding:utf-8 -*-

from django.contrib import admin
from django.conf.urls import url
from django.shortcuts import render,redirect

from . import models
from waterwork.mixins import ExportCsvMixin
import json
from django.contrib.gis.db import models as gis_model
from django.contrib.gis.geos import GEOSGeometry
import traceback
from django.db import connection
from entm.forms import CsvImportForm
import unicodecsv

# Register your models here.

@admin.register(models.FenceDistrict)
class FenceDistrictAdmin(admin.ModelAdmin,ExportCsvMixin):
    list_display = ['name','parent','belongto','ftype','createDataTime','createDataUsername','cid','pId','updateDataTime','updateDataUsername']
    actions = ['export_as_csv']



@admin.register(models.FenceShape)
class FenceShapeAdmin(admin.ModelAdmin,ExportCsvMixin):
    list_display = ['shapeId','name','zonetype','shape','dma_no','geomdata','geomjson','pointSeqs','longitudes','latitudes','lnglatQuery_LU','lnglatQuery_RD']
    actions = ['export_as_csv','convert_to_geomjson','mercatro_to_geomjson','convert_to_geomdata']

    fieldsets = (
        (None, {'fields': ('shapeId', 'name','zonetype','shape','dma_no')}),
        ('Polygon', {'fields': ('pointSeqs','longitudes','latitudes')}),
        ('Rectangle', {'fields': ('lnglatQuery_LU','lnglatQuery_RD')}),
        ('Circle', {'fields': ('centerPointLat','centerPointLng','centerRadius')}),
        ('Administrator', {'fields': ('province','city','district','administrativeLngLat')}),
    )

    change_list_template = "entm/heroes_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            # ...
            url('import-csv/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            reader = unicodecsv.reader(csv_file)
            # Create Hero objects from passed in data
            # ...
            headers = next(reader)
            print(headers,len(headers))
            # data = {i: v for (i, v) in enumerate(reader)}
            
            for row in reader:
                # print(row,len(row))
                data = {headers[i]:v for (i, v) in enumerate(row)}
                del data["id"]
                del data["geomdata"]
                
                # data = ["{}={}".format(headers[i],v) for (i, v) in enumerate(row)]
                # tdata = list("{}={}".format(k,v) for k,v in data.items())
                print(data)
                
                models.FenceShape.objects.create(**data)
                # for i in range(len(row)):
                #     print("{}.{}={}".format(i,headers[i],row[i]))
            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "entm/csv_form.html", payload
        )

    def convert_to_geomjson(self,request,queryset):
        rows_updated = queryset.count()

        
        
        for q in queryset:
            try:
                jsondata = json.dumps(q.geojsondata())
                # q.save()
                wkt = "'{}'".format(jsondata)
                name = q.name
                with connection.cursor() as cursor:
                    #cursor.execute("""UPDATE fenceshape SET geomdata = %(coord)s  """, {'coord':wkt})
                    print(cursor.execute("""update virvo_fenceshape set geomjson=%s where name='%s'  """%(wkt,name)))
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
                jsondata = json.dumps(q.geojsondata_mercator())
                # q.geomjson = json.dumps(q.geojsondata_mercator())
                # q.save()
                wkt = "'{}'".format(jsondata)
                name = q.name
                with connection.cursor() as cursor:
                    #cursor.execute("""UPDATE fenceshape SET geomdata = %(coord)s  """, {'coord':wkt})
                    print(cursor.execute("""update virvo_fenceshape set geomjson=%s where name='%s'  """%(wkt,name)))
            except Exception as e:
                print('error appear:',e)
                pass
        if rows_updated == 1:
            message_bit = "1 item was"
        else:
            message_bit = "%s items were" % rows_updated
        self.message_user(request, "%s successfully updated as nomal." % message_bit)
    mercatro_to_geomjson.short_description = 'MerCato to geomjson' 


    def convert_to_geomdata(self,request,queryset):
        rows_updated = queryset.count()

        
        
        for q in queryset:
            try:
                
                # q.geomdata="GeomFromText('LINESTRING(2 1, 6 6)')"
                # poly = GEOSGeometry('POLYGON(( 10 10, 10 20, 20 20, 20 15, 10 10))')
                # wkt = "POLYGON((-12.12890625 58.768200159239576, 1.1865234375 58.49369382056807, 5.537109375 50.2612538275847, -12.9638671875 49.18170338770662, -12.12890625 58.768200159239576))"
                # wkt = "GeomFromText('POLYGON((-13.12890625 58.768200159239576, 1.1865234375 58.49369382056807, 5.537109375 50.2612538275847, -12.9638671875 49.18170338770662, -13.12890625 58.768200159239576))')"
                # q.geomdata = wkt #GEOSGeometry(json.dumps(polyg))
                print(q.geomdata)
                if q.geomjson is None:
                    continue
                jd = json.loads(q.geomjson)
                print(jd['coordinates'],type(jd))
                d = jd['coordinates'][0]
                coordstr = ','.join('%s %s'%(a[0],a[1]) for a in d)
                wkt = "GeomFromText('POLYGON(({}))')".format(coordstr)
                print("wkt:",wkt)
                name = q.name
                print('name=',name)
                strqerer="""update virvo_fenceshape set geomdata=%s where name='%s'  """%(wkt,name)
                print("sdfe:",strqerer)
                # q.save()
                # models.FenceShape.objects.raw("update fenceshape set geomdata = 'POLYGON(( 10 10, 10 20, 20 20, 20 15, 10 10))'")
                with connection.cursor() as cursor:
                    # cursor.execute("""UPDATE fenceshape SET geomdata = %(coord)s  """, {'coord':wkt})
                    cursor.execute("""update virvo_fenceshape set geomdata=%s where name='%s'  """%(wkt,name))
                    # print(cursor.execute("""update fenceshape set geomdata=%s where name='%s'  """%(wkt,name)))
            except Exception as e:
                print('error appear:',e)
                
                traceback.print_exc()
        if rows_updated == 1:
            message_bit = "1 item was"
        else:
            message_bit = "%s items were" % rows_updated
        self.message_user(request, "%s successfully updated as nomal." % message_bit)
    convert_to_geomdata.short_description = 'coordinates to geomdata' 