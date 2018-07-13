# -*- coding: utf-8 -*-

from django import forms
from django.utils.dateparse import parse_datetime
from django.contrib.admin import widgets
from django.contrib.admin.widgets import AdminDateWidget,AdminSplitDateTime
from django.contrib.postgres.forms.ranges import DateRangeField, RangeWidget



from .models import WaterUserType,DMABaseinfo
import datetime


class DMACreateForm(forms.ModelForm):

    class Meta:
        model = DMABaseinfo
        fields = ['dma_no','dma_name','creator','create_date']



class WaterUserTypeForm(forms.ModelForm):
    
    class Meta:
        model = WaterUserType
        fields = ['usertype','explains']

    def __init__(self,instance,*args,**kwargs):
        super(WaterUserTypeForm, self).__init__(*args, **kwargs)
                        