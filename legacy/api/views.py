from django.shortcuts import render
from rest_framework import viewsets
from legacy.models import Alarm
from .serializers import AlarmSerializer
from django.db.models import Count
import time


class AlarmViewSet(viewsets.ModelViewSet):
    queryset = Alarm.objects.all()
    serializer_class = AlarmSerializer

    class Meta:
        datatables_extra_json = ('get_options',)

    def get_queryset(self):
        queryset = Alarm.objects.filter(commaddr='13815100043')
        # alams_sets = Alarm.objects.values("commaddr").annotate(Count('id'))

        return queryset

    def get_options(self):
        t1 = time.time()
        alams_sets = Alarm.objects.values("commaddr").annotate(Count('id'))
        print('query alarm sets expends time:',time.time() - t1)
        return "options",alams_sets
