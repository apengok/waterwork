
from rest_framework import serializers

from django.db.models import Count
from legacy.models import Alarm

import time

class AlarmCountSerializer(serializers.Serializer):
    commaddrcount = serializers.SerializerMethodField()

    # class Meta:
    #     model = Alarm
    #     fields = ('commaddrcount',)

    def get_commaddrcount(self,obj):
        alams_sets = Alarm.objects.values("commaddr").annotate(Count('id'))
        print("i am here??")
        return alams_sets


class AlarmSerializer(serializers.ModelSerializer):
    # counts = AlarmCountSerializer()
    class Meta:
        model = Alarm
        fields = '__all__'

