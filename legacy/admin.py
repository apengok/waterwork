# -*- coding:utf-8 -*-

from django.contrib import admin
from . models import Bigmeter
# Register your models here.


@admin.register(Bigmeter)
class BigmeterAdmin(admin.ModelAdmin):
    list_display = ["username","commaddr","lat","lng"]

    actions = ['update_districtid','update_userid']

    def update_districtid(self,request,queryset):
        rows_updated = queryset.update(districtid=3)
        
        if rows_updated == 1:
            message_bit = "1 item was"
        else:
            message_bit = "%s items were" % rows_updated
        self.message_user(request, "%s successfully updated as nomal." % message_bit)
    update_districtid.short_description = 'update districtid ' 


    def update_userid(self,request,queryset):
        rows_updated = queryset.update(userid=1001)
        
        if rows_updated == 1:
            message_bit = "1 item was"
        else:
            message_bit = "%s items were" % rows_updated
        self.message_user(request, "%s successfully updated as nomal." % message_bit)
    update_userid.short_description = 'update userid ' 