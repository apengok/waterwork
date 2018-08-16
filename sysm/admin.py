# -*- coding: utf-8 -*-

from django.contrib import admin
from . models import Personalized
# Register your models here.


@admin.register(Personalized)
class PersonalizedAdmin(admin.ModelAdmin):
    list_display = ['belongto','loginLogo', 'webIco','homeLogo','topTitle','copyright','websiteName','recordNumber','frontPageMsg']