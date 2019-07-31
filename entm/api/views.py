from django.shortcuts import render
from rest_framework import viewsets,generics,filters
from entm.models import Organizations
from .serializers import OrganizationsSerializer
from waterwork.filters import DatatablesFilterBackend
# from rest_framework_datatables.filters import DatatablesFilterBackend

class OrganizationsViewSet(viewsets.ModelViewSet):
    queryset = Organizations.objects.all()
    serializer_class = OrganizationsSerializer


    def get_serializer_context(self):
        context = super(OrganizationsViewSet,self).get_serializer_context()
        # print("get_serialier_contex:",context)
        return context

