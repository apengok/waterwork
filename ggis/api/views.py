from django.shortcuts import render
from rest_framework import viewsets,generics,filters
from entm.models import Organizations
from ggis.models import FenceDistrict,FenceShape
from .serializers import FenceDistrictSerializer,FenceShapeSerializer,FenceShapeGeoSerializer
from waterwork.filters import DatatablesFilterBackend
# from rest_framework_datatables.filters import DatatablesFilterBackend

class FenceDistrictViewSet(viewsets.ModelViewSet):
    queryset = FenceDistrict.objects.all()
    serializer_class = FenceDistrictSerializer


    def get_serializer_context(self):
        context = super(FenceDistrictViewSet,self).get_serializer_context()
        # print("get_serialier_contex:",context)
        return context


class FenceShapeViewSet(viewsets.ModelViewSet):
    queryset = FenceShape.objects.all()
    serializer_class = FenceShapeSerializer



class FenceShapeCollectionViewSet(viewsets.ModelViewSet):
    queryset = FenceShape.objects.all()
    serializer_class = FenceShapeGeoSerializer