# -*- coding:utf-8 -*-

from django.contrib import admin
from . models import Bigmeter
# Register your models here.


@admin.register(Bigmeter)
class BigmeterAdmin(admin.ModelAdmin):
    list_display = ["username","commaddr","lat","lng"]

    actions = ['update_districtid','update_default']

    def update_districtid(self,request,queryset):
        rows_updated = queryset.update(districtid=3)
        
        if rows_updated == 1:
            message_bit = "1 item was"
        else:
            message_bit = "%s items were" % rows_updated
        self.message_user(request, "%s successfully updated as nomal." % message_bit)
    update_districtid.short_description = 'update districtid ' 


    def update_default(self,request,queryset):
        rows_updated = queryset.update(alarmoffline=1,alarmonline=1,
            alarmgprsvlow=1,alarmmetervlow=1,alarmuplimitflow=1,alarmgpflow=1,pressurealarm=1,dosagealarm=1)
        
        if rows_updated == 1:
            message_bit = "1 item was"
        else:
            message_bit = "%s items were" % rows_updated
        self.message_user(request, "%s successfully updated as nomal." % message_bit)
    update_default.short_description = 'update default ' 