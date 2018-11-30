# -*- coding:utf-8 -*-

from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Organizations)
class OrganizationsAdmin(admin.ModelAdmin):
    list_display = ['name','parent','attribute','organlevel','register_date','owner_name','phone_number','firm_address','cid','pId','is_org','uuid']
    list_filter = ('organlevel','attribute')
    search_fields = ['name']

    actions = ['set_sublevel']

    def set_sublevel(self,request,queryset):
        # rows_updated = queryset.update(meterstate='正常')
        rows_updated = queryset.count()

        def set_level(q):
            if q.parent:
                level = q.parent.organlevel
                attr = q.parent.attribute
                if attr == "自来水公司":
                    q.attribute = attr
                    q.organlevel = int(level)+1
                    q.save()
                else:
                    q.attribute = "非自来水公司"
                    q.save()
        
        for q in queryset:
            try:
                for s in q.sub_organizations(include_self=False):
                    print(s)
                    set_level(s)
            except Exception as e:
                print('error appear:',e)
                pass
        if rows_updated == 1:
            message_bit = "1 item was"
        else:
            message_bit = "%s items were" % rows_updated
        self.message_user(request, "%s successfully updated as nomal." % message_bit)
    set_sublevel.short_description = 'set sub organization level' 