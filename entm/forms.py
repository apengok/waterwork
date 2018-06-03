# -*- coding: utf-8 -*-

from django import forms
from django.utils.dateparse import parse_datetime
from django.contrib.admin import widgets
from django.contrib.admin.widgets import AdminDateWidget,AdminSplitDateTime
from django.contrib.postgres.forms.ranges import DateRangeField, RangeWidget


import datetime
from .models import Organizations

# import settings


class OrganizationsAddForm(forms.ModelForm):
    """docstring for OrganizationsAddForm"""

    class Meta:
        model = Organizations
        fields = ('name','attribute','register_date','owner_name','phone_number','firm_address')

