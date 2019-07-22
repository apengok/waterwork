from django.shortcuts import render
from rest_framework import viewsets
from legacy.models import Alarm
from .serializers import AlarmSerializer



class AlarmViewSet(viewsets.ModelViewSet):
    queryset = Alarm.objects.all()
    serializer_class = AlarmSerializer