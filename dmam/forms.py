# -*- coding: utf-8 -*-

from django import forms
from django.utils.dateparse import parse_datetime
from django.contrib.admin import widgets
from django.contrib.admin.widgets import AdminDateWidget,AdminSplitDateTime
from django.contrib.postgres.forms.ranges import DateRangeField, RangeWidget


from entm.models import Organizations
from .models import WaterUserType,DMABaseinfo,Station,Meter
import datetime


class DMACreateForm(forms.ModelForm):

    class Meta:
        model = DMABaseinfo
        fields = ['dma_no','dma_name','creator','create_date']



class DMABaseinfoForm(forms.ModelForm):
    belongto  = forms.CharField()

    class Meta:
        model = DMABaseinfo
        fields = ['dma_no','pepoles_num','acreage','user_num','pipe_texture','pipe_length','pipe_links','pipe_years','pipe_private','ifc','aznp','night_use','cxc_value']

    def __init__(self,*args,**kwargs):
        super(DMABaseinfoForm, self).__init__(*args, **kwargs)

        # self.fields['password'].widget = forms.PasswordInput()
        self.fields['belongto'].initial = self.instance.belongto.name
        
    def clean_belongto(self):
        organ_name = self.cleaned_data.get("belongto")
        print('organ_name:',organ_name)
        organ = Organizations.objects.get(name=organ_name)
        return organ

class WaterUserTypeForm(forms.ModelForm):
    
    class Meta:
        model = WaterUserType
        fields = ['usertype','explains']

    def __init__(self,instance,*args,**kwargs):
        super(WaterUserTypeForm, self).__init__(*args, **kwargs)
                        

class StationsForm(forms.ModelForm):
    description = forms.CharField(required = False)
    belongto = forms.CharField()
    serialnumber = forms.CharField()
    simid = forms.CharField(required = False)
    dn = forms.CharField()
    metertype = forms.CharField()


    def __init__(self, *args, **kwargs):
        super(StationsForm, self).__init__(*args, **kwargs)
        

    class Meta:
        model = Station    
        fields= ('username','description','usertype','madedate','lng','lat','locate')


class StationsEditForm(forms.ModelForm):
    description = forms.CharField(required = False)
    belongto = forms.CharField()
    serialnumber = forms.CharField()
    simid = forms.CharField(required = False)
    dn = forms.CharField()
    metertype = forms.CharField()
    meter = forms.CharField()


    def __init__(self, *args, **kwargs):
        super(StationsEditForm, self).__init__(*args, **kwargs)

        self.fields['belongto'].initial = self.instance.belongto.name
        self.fields['meter'].initial = self.instance.meter.serialnumber

        if self.instance.meter:
            self.fields['serialnumber'].initial = self.instance.meter.serialnumber
            self.fields['dn'].initial = self.instance.meter.dn
            self.fields['metertype'].initial = self.instance.meter.metertype
            
            if self.instance.meter.simid:
                self.fields['simid'].initial = self.instance.meter.simid.simcardNumber
        

    class Meta:
        model = Station    
        fields= ('username','description','usertype','madedate','lng','lat','locate')


class AssignStationForm(forms.Form):
    stationassign = forms.CharField()

    # class Meta:
    #     model = DMABaseinfo
    #     fields = ('dma_no',)


class StationAssignForm(forms.ModelForm):
    stationassign = forms.CharField()

    class Meta:
        model = DMABaseinfo
        fields = ('dma_no',)