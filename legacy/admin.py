from django.contrib import admin
from . models import Bigmeter
# Register your models here.


@admin.register(Bigmeter)
class BigmeterAdmin(admin.ModelAdmin):
    list_display = ["username","commaddr","lat","lng"]