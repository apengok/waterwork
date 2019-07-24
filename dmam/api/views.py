from django.shortcuts import render
from rest_framework import viewsets,generics,filters
from entm.models import Organizations
from dmam.models import Station
from legacy.models import Bigmeter
from .serializers import StationSerializer,BigmeterSerializer,OranizationsSerializer


class OrganizationsViewSet(viewsets.ModelViewSet):
    queryset = Organizations.objects.all()
    serializer_class = OranizationsSerializer



class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


class StationRealtimeListView(generics.ListAPIView):
    # queryset = Station.objects.all()
    serializer_class = StationSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['bigmeter__fluxreadtime', 'username']
    ordering = ['bigmeter__fluxreadtime']

    def get_queryset(self):
        return self.request.user.station_list_queryset('')

    def get(self,request, *args, **kwargs):
        print('pwl:',self.request.user,args,kwargs)
        return self.list(request, *args, **kwargs)



class BigmeterViewSet(viewsets.ModelViewSet):
    queryset = Bigmeter.objects.all()
    serializer_class = BigmeterSerializer
    filter_backends = [filters.OrderingFilter]

    ordering_fields = ['fluxreadtime', 'username']
    ordering = ['-fluxreadtime']

    # def get_queryset(self):
    #     # stations = self.request.user.station_list_queryset('')
    #     return Bigmeter.objects.all()

    def filter_queryset(self, queryset):
        # print('i am here?')
        stations = self.request.user.station_list_queryset('')
        # print(stations.count())
        # print(queryset.filter(station__in=stations).count())
        return queryset.filter(station__in=stations)