
from rest_framework import serializers
from accounts.models import User,MyRoles
from entm.models import Organizations
from dmam.models import Station,DMABaseinfo,WaterUserType,DmaStation,SimCard,Meter,VConcentrator,VCommunity,VWatermeter,VPressure,VSecondWater

class  UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"



class StationSerializer(serializers.ModelSerializer):
    belongto_name = serializers.ReadOnlyField(source='belongto.name')

    class Meta:
        model = Station
        fields = ['id','username','usertype','biguser','focus','madedate','meter','belongto_name','dmametertype']


class DMABaseinfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DMABaseinfo
        fields = '__all__'