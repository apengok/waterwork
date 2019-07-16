
from rest_framework import serializers

from dmam.models import Station,DMABaseinfo


class StationSerializer(serializers.ModelSerializer):
    belongto_name = serializers.ReadOnlyField(source='belongto.name')

    class Meta:
        model = Station
        fields = ['id','username','usertype','biguser','focus','madedate','meter','belongto_name','dmametertype']


class DMABaseinfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DMABaseinfo
        fields = '__all__'