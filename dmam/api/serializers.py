# -*- coding: utf-8 -*-

from rest_framework import serializers
from entm.models import Organizations
from dmam.models import Station
from legacy.models import Bigmeter



class StationSerializer(serializers.ModelSerializer):
    # bigmeter = BigmeterSerializer()
    belongto_name = serializers.ReadOnlyField(source='belongto.name')
    serialnumber = serializers.ReadOnlyField(source='meter.serialnumber')
    dn = serializers.ReadOnlyField(source='meter.dn')
    # commaddr = serializers.SerializerMethodField()
    

    class Meta:
        model = Station
        fields = ('username','usertype','biguser','focus','madedate','serialnumber','dn',
        'belongto_name','dmametertype')



class BigmeterSerializer(serializers.ModelSerializer):
    # stations = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    station = StationSerializer(many=True,read_only=True)
    belongto_name = serializers.ReadOnlyField(source='station.username')

    class Meta:
        model = Bigmeter
        fields = ('username','commaddr','commstate','fluxreadtime','pickperiod','reportperiod','station','belongto_name',
        'flux','plustotalflux','reversetotalflux','pressure','meterv','gprsv','signlen','pressurereadtime')



class OranizationsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    station = StationSerializer(many=True,read_only=True)

    class Meta:
        model = Organizations
        fields = ('id','name','parent','attribute','organlevel','register_date','owner_name','phone_number','firm_address',
            'coorType','longitude','latitude','zoomIn','islocation','location','province','city','district','adcode','districtlevel',
            'cid','pId','is_org','uuid','station')