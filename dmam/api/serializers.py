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
    fluxreadtime = serializers.ReadOnlyField(source='bigmeter.fluxreadtime')
    commstate = serializers.ReadOnlyField(source='bigmeter.commstate')
    pickperiod = serializers.ReadOnlyField(source='bigmeter.pickperiod')
    reportperiod = serializers.ReadOnlyField(source='bigmeter.reportperiod')
    flux = serializers.ReadOnlyField(source='bigmeter.flux')
    plustotalflux = serializers.ReadOnlyField(source='bigmeter.plustotalflux')
    reversetotalflux = serializers.ReadOnlyField(source='bigmeter.reversetotalflux')
    pressure = serializers.ReadOnlyField(source='bigmeter.pressure')
    meterv = serializers.ReadOnlyField(source='bigmeter.meterv')
    gprsv = serializers.ReadOnlyField(source='bigmeter.gprsv')
    signlen = serializers.ReadOnlyField(source='bigmeter.signlen')
    pressurereadtime = serializers.ReadOnlyField(source='bigmeter.pressurereadtime')

    class Meta:
        model = Station
        fields = ('fluxreadtime','username','usertype','biguser','focus','madedate','serialnumber','dn',
        'belongto_name','dmametertype','commaddr','commstate','pickperiod','reportperiod',
        'flux','plustotalflux','reversetotalflux','pressure','meterv','gprsv','signlen','pressurereadtime')



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