from django.contrib import admin
from . models import WaterUserType
# Register your models here.


@admin.register(WaterUserType)
class OrganizationsAdmin(admin.ModelAdmin):
    list_display = ['usertype','explains']
