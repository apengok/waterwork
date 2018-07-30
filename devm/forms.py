# -*- coding: utf-8 -*-

from django import forms
from django.utils.dateparse import parse_datetime
from django.contrib.admin import widgets
from django.contrib.admin.widgets import AdminDateWidget,AdminSplitDateTime
from django.contrib.postgres.forms.ranges import DateRangeField, RangeWidget


from entm.models import Organizations
from dmam.models import WaterUserType,DMABaseinfo,Station,Meter,SimCard
import datetime




class MeterAddForm(forms.ModelForm):
    belongto  = forms.CharField()
    simid  = forms.CharField()

    class Meta:
        model = Meter
        fields = ['serialnumber','version','dn','metertype','mtype','manufacturer','protocol','R','q3','q1','check_cycle','state']

    # def __init__(self,*args,**kwargs):
    #     super(MeterAddForm, self).__init__(*args, **kwargs)

    #     # self.fields['password'].widget = forms.PasswordInput()
    #     self.fields['belongto'].initial = self.instance.belongto.name
        

class MeterEditForm(forms.ModelForm):
    belongto  = forms.CharField()
    simid  = forms.CharField()

    class Meta:
        model = Meter
        fields = ['serialnumber','version','dn','metertype','mtype','manufacturer','protocol','R','q3','q1','check_cycle','state']

    def __init__(self,*args,**kwargs):
        super(MeterEditForm, self).__init__(*args, **kwargs)

        # self.fields['password'].widget = forms.PasswordInput()
        self.fields['belongto'].initial = self.instance.belongto.name
        self.fields['simid'].initial = self.instance.simid.simcardNumber


class SimCardAddForm(forms.ModelForm):
    belongto  = forms.CharField()

    class Meta:
        model = SimCard
        fields = ['simcardNumber','isStart','iccid','imei','imsi','operator','simFlow','openCardTime','endTime','remark']

    
        

class SimCardEditForm(forms.ModelForm):
    belongto  = forms.CharField()

    class Meta:
        model = SimCard
        fields = ['simcardNumber','isStart','iccid','imei','imsi','operator','simFlow','openCardTime','endTime','remark']

    def __init__(self,*args,**kwargs):
        super(SimCardEditForm, self).__init__(*args, **kwargs)

        # self.fields['password'].widget = forms.PasswordInput()
        self.fields['belongto'].initial = self.instance.belongto.name