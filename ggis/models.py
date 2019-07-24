# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.db import models
from django.contrib.gis.db import models
from django.urls import reverse
from entm.models import Organizations
import datetime
from django.db.models import Q
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.db.models import Avg, Max, Min, Sum
from django.utils.functional import cached_property
import time
import json
from mptt.models import MPTTModel, TreeForeignKey

from ggis.GGaussCoordConvert import Mercator2lonLat
from django.contrib.gis.geos import GEOSGeometry
from django.db import connection

'''
{"name":"标注","pId":"","id":"zw_m_marker","type":"fenceParent","open":"true"},
{"name":"矩形","pId":"","id":"zw_m_rectangle","type":"fenceParent","open":"true"},
{"name":"圆形","pId":"","id":"zw_m_circle","type":"fenceParent","open":"true"},
{"name":"多边形","pId":"0","id":"zw_m_polygon","type":"fenceParent","open":"true"},
{"name":"行政区划","pId":"0","id":"zw_m_administration","type":"fenceParent","open":"true"},
'''                
class FenceDistrict(MPTTModel):
    name               = models.CharField('区域名称',max_length=100,unique=True)
    ftype               = models.CharField('区域类型',max_length=30,null=True,blank=True) #fenceParent,fence
    createDataTime      = models.CharField('创建时间',max_length=30,null=True,blank=True)
    updateDataTime      = models.CharField('修改时间',max_length=30,null=True,blank=True)
    createDataUsername         = models.CharField('创建人',max_length=30,null=True,blank=True)
    updateDataUsername         = models.CharField('修改人',max_length=30,null=True,blank=True)
    description       = models.TextField('描述',null=True,blank=True)

    cid           = models.CharField(max_length=100,null=True,blank=True)
    pId           = models.CharField(max_length=100,null=True,blank=True)

    belongto      = models.ForeignKey(Organizations,on_delete=models.CASCADE,null=True)

    parent  = TreeForeignKey('self', null=True, blank=True,on_delete=models.CASCADE, related_name='children', db_index=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        managed = True
        db_table = 'virvo_fencedistrict'

        

    def __unicode__(self):
        return self.name    

    def __str__(self):
        return self.name 



def build_feature_collection(cur,prop):
    """
    Execute a JSON-returning SQL and return HTTP response
    :type sql: SQL statement that returns a a GeoJSON Feature
    """
    features = []
    for idx,row in enumerate(cur):
        print('row data',row)
        coords = row["coordinates"][0]
        coords_trans = [[float(p[0]),float(p[1])] for p in coords]
        row["coordinates"] = [coords_trans]
        feature = {
                "geometry":row,#json.dumps(row),
                "type":"Feature",
                "properties":prop[idx]
            }
        features.append(feature)
    
    FeatureCollection = {
        "type":"FeatureCollection",
        "features":features
    }
        
    return FeatureCollection

class FenceShape(models.Model):
    shapeId   = models.CharField(max_length=255,null=True,blank=True)   # =FenceDistrict.cid 形状公用，由shape区分
    name   = models.CharField('区域名称',max_length=100,unique=True)
    zonetype   = models.CharField('区域类型',max_length=30,null=True,blank=True)
    shape   = models.CharField('形状',max_length=30,null=True,blank=True)
    
    # 增加geometry 数据类型直接保存geom
    # bounds_geom = models.PolygonField(srid=0)
    geomdata = models.GeometryField(srid=0, blank=True, null=True)
    geomjson = models.TextField(blank=True, null=True)
    

    # 多边形 各点经纬度 也应用于矩形等
    pointSeqs   = models.TextField()
    longitudes   = models.TextField()
    latitudes   = models.TextField()

    # 矩形：左上角、右下角经纬度
    lnglatQuery_LU   = models.CharField(max_length=30,null=True,blank=True)
    lnglatQuery_RD   = models.CharField(max_length=30,null=True,blank=True)

    # 圆形：中心经纬度，半径
    centerPointLat   = models.CharField(max_length=30,null=True,blank=True)
    centerPointLng   = models.CharField(max_length=30,null=True,blank=True)
    centerRadius   = models.CharField(max_length=30,null=True,blank=True)
    
    # 行政区：省、市、区
    province   = models.CharField(max_length=30,null=True,blank=True)
    city   = models.CharField(max_length=30,null=True,blank=True)
    district   = models.CharField(max_length=30,null=True,blank=True)
    administrativeLngLat = models.TextField()

    # 边框和区域填色
    strokeColor   = models.CharField(max_length=100,blank=True,null=True)
    fillColor     = models.CharField(max_length=100,blank=True,null=True)

    dma_no       = models.CharField(max_length=30,null=True,blank=True) #关联的dma分区  


    class Meta:
        managed = True
        db_table = 'virvo_fenceshape'

        

    def __unicode__(self):
        return self.name    

    def __str__(self):
        return self.name 


    def geojsondata(self):
        pointSeqs = self.pointSeqs.split(',')
        longitudes = self.longitudes.split(',')
        latitudes = self.latitudes.split(',')

        coords = [list(p) for p in zip(longitudes,latitudes)]
        coords.append([float(longitudes[0]),float(latitudes[0])])

        coords_trans = [[float(p[0]),float(p[1])] for p in coords]

        coordinates = []
        coordinates.append(coords_trans)

        # FeatureCollection = {
        #     "type":"FeatureCollection",
        #     "features":[
        #         {
        #             "type":"Feature",
        #             "geometry":{
        #                 "type":"Polygon",
        #                 "coordinates":coordinates
        #             },
        #             "properties":"null"
        #         }]
        # }

        geodata = {
            "type":"Polygon",
            "coordinates":coordinates,
            # "properties":{"name":self.name}
        }

        print('\r\n\r\n',geodata,type(geodata))

        return geodata

    def geojsondata_mercator(self):
        pointSeqs = self.pointSeqs.split(',')
        longitudes = self.longitudes.split(',')
        latitudes = self.latitudes.split(',')

        coords = [list(p) for p in zip(longitudes,latitudes)]
        coords.append([longitudes[0],latitudes[0]])

        coords_trans = [Mercator2lonLat(float(p[0]),float(p[1])) for p in coords]

        coordinates = []
        coordinates.append(coords_trans)

        # FeatureCollection = {
        #     "type":"FeatureCollection",
        #     "features":[
        #         {
        #             "type":"Feature",
        #             "geometry":{
        #                 "type":"Polygon",
        #                 "coordinates":coordinates
        #             },
        #             "properties":"null"
        #         }]
        # }

        geodata = {
            "type":"Polygon",
            "coordinates":coordinates,
            # "properties":{"name":self.name}
            
        }

        return geodata

    def featureCollection(self):
        data = []
        data_property = []
        properties = {"strokeColor":self.strokeColor,"fillColor":self.fillColor,"name":self.name}
        data.append(json.loads(self.geomdata.geojson))
        data_property.append(properties)

        return build_feature_collection(data,data_property)

    

from entm.utils import unique_shapeid_generator,unique_cid_generator

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.cid:
        # instance.slug = create_slug(instance)
        instance.cid = unique_cid_generator(instance)
        
def polygon_pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.geomjson:
        # instance.slug = create_slug(instance)
        instance.geomjson = json.dumps(instance.geojsondata())
        # instance.geomjson = json.dumps(instance.geojsondata_mercator())
        print('instance.geomjson---',instance.geomjson)
        try:
            instance.save()

            # geomdata
            jd = json.loads(instance.geomjson)
            d = jd['coordinates'][0]
            coordstr = ','.join('%s %s'%(a[0],a[1]) for a in d)
            wkt = "GeomFromText('POLYGON(({}))')".format(coordstr)
            name = instance.name
            strqerer="""update fenceshape set geomdata=%s where name='%s'  """%(wkt,name)
            with connection.cursor() as cursor:
                cursor.execute("""update fenceshape set geomdata=%s where name='%s'  """%(wkt,name))

        except Exception as e:
            print('Error shows :',e)
        
pre_save.connect(pre_save_post_receiver, sender=FenceDistrict)        
post_save.connect(polygon_pre_save_post_receiver, sender=FenceShape)

