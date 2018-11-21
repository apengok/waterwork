# -*- coding: utf-8 -*-

from django import forms
from django.utils.dateparse import parse_datetime
from django.contrib.admin import widgets
from django.contrib.admin.widgets import AdminDateWidget,AdminSplitDateTime
from django.contrib.postgres.forms.ranges import DateRangeField, RangeWidget


from entm.models import Organizations
from dmam.models import WaterUserType,DMABaseinfo,Station,Meter,SimCard,VConcentrator,VCommunity,VWatermeter
import datetime




class MeterAddForm(forms.ModelForm):
    belongto  = forms.CharField()
    simid  = forms.CharField()

    class Meta:
        model = Meter
        fields = ['serialnumber','version','dn','metertype','mtype','manufacturer','protocol','R','q4','q3','q2','q1','check_cycle','state']

    # def __init__(self,*args,**kwargs):
    #     super(MeterAddForm, self).__init__(*args, **kwargs)

    #     # self.fields['password'].widget = forms.PasswordInput()
    #     self.fields['belongto'].initial = self.instance.belongto.name
        

class MeterEditForm(forms.ModelForm):
    belongto  = forms.CharField()
    simid  = forms.CharField()

    class Meta:
        model = Meter
        fields = ['serialnumber','version','dn','metertype','mtype','manufacturer','protocol','R','q4','q3','q2','q1','check_cycle','state']

    def __init__(self,*args,**kwargs):
        super(MeterEditForm, self).__init__(*args, **kwargs)

        # self.fields['password'].widget = forms.PasswordInput()
        self.fields['belongto'].initial = self.instance.belongto.name
        self.fields['simid'].initial = self.instance.simid.simcardNumber if self.instance.simid else ''


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


class VConcentratorAddForm(forms.ModelForm):
    belongto  = forms.CharField()
    
    class Meta:
        model = VConcentrator
        fields = ['name','lng','lat','coortype','model','serialnumber','manufacturer','madedate','commaddr','address']


class VConcentratorEditForm(forms.ModelForm):
    belongto  = forms.CharField()
    
    class Meta:
        model = VConcentrator
        fields = ['name','lng','lat','coortype','model','serialnumber','manufacturer','madedate','commaddr','address']

    def __init__(self,*args,**kwargs):
        super(VConcentratorEditForm, self).__init__(*args, **kwargs)

        self.fields['belongto'].initial = self.instance.belongto.name



class VCommunityAddForm(forms.ModelForm):
    belongto  = forms.CharField()
    vconcentrator1 = forms.CharField(required=False)
    vconcentrator2 = forms.CharField(required=False)
    vconcentrator3 = forms.CharField(required=False)
    vconcentrator4 = forms.CharField(required=False)
    
    class Meta:
        model = VCommunity
        fields = ['name','address']


class VCommunityEditForm(forms.ModelForm):
    belongto  = forms.CharField()
    vconcentrator1 = forms.CharField(required=False)
    vconcentrator2 = forms.CharField(required=False)
    vconcentrator3 = forms.CharField(required=False)
    vconcentrator4 = forms.CharField(required=False)
    
    class Meta:
        model = VCommunity
        fields = ['name','address']

    def __init__(self,*args,**kwargs):
        super(VCommunityEditForm, self).__init__(*args, **kwargs)

        self.fields['belongto'].initial = self.instance.belongto.name
        vconcents = self.instance.vconcentrators.all()
        v_count = vconcents.count()
        self.fields['vconcentrator1'].initial = vconcents[0].name
        if v_count == 2:
            self.fields['vconcentrator2'].initial = vconcents[1].name

        if v_count == 3:
            self.fields['vconcentrator2'].initial = vconcents[1].name
            self.fields['vconcentrator3'].initial = vconcents[2].name

        if v_count == 4:
            self.fields['vconcentrator2'].initial = vconcents[1].name
            self.fields['vconcentrator3'].initial = vconcents[2].name
            self.fields['vconcentrator4'].initial = vconcents[3].name


class VWatermeterAddForm(forms.ModelForm):
    communityid  = forms.CharField()
    concentrator = forms.CharField()

    class Meta:
        model = VWatermeter
        fields = ['name','numbersth','buildingname','roomname','username','usertel','dn','serialnumber','manufacturer','madedate','ValveMeter']


class VWatermeterEditForm(forms.ModelForm):
    communityid  = forms.CharField()
    concentrator = forms.CharField()
    
    class Meta:
        model = VWatermeter
        fields = ['name','numbersth','buildingname','roomname','username','usertel','dn','serialnumber','manufacturer','madedate','ValveMeter']

    def __init__(self,*args,**kwargs):
        super(VWatermeterEditForm, self).__init__(*args, **kwargs)

        self.fields['communityid'].initial = self.instance.communityid.name
        self.fields['concentrator'].initial = self.instance.concentrator.name
