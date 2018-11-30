# -*- coding: utf-8 -*-

from django import forms
from django.utils.dateparse import parse_datetime,parse_date
from django.contrib.admin import widgets
from django.contrib.admin.widgets import AdminDateWidget,AdminSplitDateTime
from django.contrib.postgres.forms.ranges import DateRangeField, RangeWidget


import datetime
from .models import Organizations

# import settings


class OrganizationsAddForm(forms.ModelForm):
    """docstring for OrganizationsAddForm"""
    parent_attribute = forms.CharField()
    parent_organlevel = forms.CharField()

    class Meta:
        model = Organizations
        fields = ('name','attribute','organlevel','register_date','owner_name','phone_number','firm_address','cid','pId',
            'coorType','zoomIn','longitude','latitude','islocation','location','province','city','district','adcode','districtlevel')

    def __init__(self,*args,**kwargs):
        print('form init',args,kwargs)
        super(OrganizationsAddForm, self).__init__(*args, **kwargs)
        self.fields['register_date'].widget.attrs['input_formats'] =['%Y-%m-%d',]


    


class OrganizationsEditForm(forms.ModelForm):
    """docstring for OrganizationsEditForm"""

    parent_attribute = forms.CharField()
    parent_organlevel = forms.CharField()

    class Meta:
        model = Organizations
        fields = ('name','attribute','organlevel','register_date','owner_name','phone_number','firm_address','cid','pId',
            'coorType','zoomIn','longitude','latitude','islocation','location','province','city','district','adcode','districtlevel')


    def __init__(self,*args,**kwargs):
        super(OrganizationsEditForm, self).__init__(*args, **kwargs)
        if self.instance.parent:
            self.fields['parent_organlevel'].initial = self.instance.parent.organlevel
            self.fields['parent_attribute'].initial = self.instance.parent.attribute

    


        