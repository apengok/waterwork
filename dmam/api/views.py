from django.shortcuts import render
from rest_framework import viewsets,generics,filters
from entm.models import Organizations
from dmam.models import Station
from legacy.models import Bigmeter
from .serializers import StationSerializer,BigmeterSerializer,OranizationsSerializer
from waterwork.filters import DatatablesFilterBackend
# from rest_framework_datatables.filters import DatatablesFilterBackend

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
    filter_backends = [DatatablesFilterBackend]

    ordering_fields = ['fluxreadtime', 'username']
    ordering = ['-fluxreadtime']

    class Meta:
        datatables_extra_json = ('get_options',)

    def get_options(self):
        return "options",{"success":True}

    def get_queryset(self):
        getter = self.request.query_params.get
        groupName = getter("groupName")
        queryset = Bigmeter.objects.all()
        stations = self.request.user.station_list_queryset('')
        pressures = self.request.user.pressure_list_queryset('')
        if groupName != "":
            stations = stations.filter(belongto__uuid=groupName)
            pressures = pressures.filter(belongto__uuid=groupName)
        return queryset.filter(station__in=stations).order_by('-fluxreadtime')

    # def filter_queryset(self, queryset):
    #     print('i am here?')
    #     stations = self.request.user.station_list_queryset('')
    #     # print(stations.count())
    #     # print(queryset.filter(station__in=stations).count())
    #     return queryset.filter(station__in=stations).order_by('-fluxreadtime')

    