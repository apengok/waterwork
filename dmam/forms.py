# -*- coding: utf-8 -*-

from django import forms
from django.utils.dateparse import parse_datetime
from django.contrib.admin import widgets
from django.contrib.admin.widgets import AdminDateWidget,AdminSplitDateTime
from django.contrib.postgres.forms.ranges import DateRangeField, RangeWidget



from .models import Bigmeter
import datetime




"""
Stations edit, manager
"""
class StationsForm(forms.ModelForm):
    description = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(StationsForm, self).__init__(*args, **kwargs)
        

    class Meta:
        model = Bigmeter    
        fields= ('username','districtid','usertype','metertype','serialnumber','simid','dn','createdate','lng','lat')