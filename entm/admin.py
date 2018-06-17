from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Organizations)
class OrganizationsAdmin(admin.ModelAdmin):
    list_display = ['name','parent','attribute','register_date','owner_name','phone_number','firm_address','cid','pId','is_org','uuid']