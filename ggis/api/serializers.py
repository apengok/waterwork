# -*- coding: utf-8 -*-
from rest_framework import serializers
from entm.models import Organizations
from ggis.models import FenceDistrict,FenceShape
import traceback
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from django.contrib.gis.geos import GEOSGeometry
from django.db import connection

class FenceDistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = FenceDistrict
        fields = '__all__'


class FenceShapeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FenceShape
        fields = '__all__'

    # def create(self, validated_data):  
    #     print(validated_data)
    #     organ_obj = FenceShape(
    #             name=validated_data.get('name'), 
    #             parent=validated_data.get('parent'))
    #     organ_obj.cid = unique_cid_generator(organ_obj,"api")
    #     organ_obj.save()
    #     return organ_obj

class FenceShapeGeoSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = FenceShape
        geo_field = 'geomdata'
        fields = ('shapeId','name','zonetype','shape','dma_no','geomdata')

    def create(self,validated_data):
        print('self.instance',self.instance)
        print(validated_data)
        obj = FenceShape(
            name=validated_data.get('name'),
            shapeId=validated_data.get('shapeId'),
            shape=validated_data.get('shape'),
        )
        obj.save()
        name = validated_data.get('name')
        geomdata = validated_data.get('geomdata')
        print('geomdata:',geomdata)
        wkt = "ST_GEOMFROMTEXT('{}')".format(geomdata)
        print('here wkt is',wkt)
        rsql = """update virvo_fenceshape set geomdata=%s where name='%s'  """%(wkt,name)
        try:
            # seem not working here
            FenceShape.objects.raw(rsql)
        except Exception as e:
            print('error:',e)
        # with connection.cursor() as cursor:
        #     cursor.execute("""update virvo_fenceshape set geomdata=%s where name='%s'  """%(wkt,name))
        return obj