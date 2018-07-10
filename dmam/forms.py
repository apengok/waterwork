# -*- coding: utf-8 -*-

from django import forms
from django.utils.dateparse import parse_datetime
from django.contrib.admin import widgets
from django.contrib.admin.widgets import AdminDateWidget,AdminSplitDateTime
from django.contrib.postgres.forms.ranges import DateRangeField, RangeWidget



from .models import WaterUserType
import datetime





class WaterUserTypeForm(object):
    
    class Meta:
        model = WaterUserType
        fields = '__all__'
                        