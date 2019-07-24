# -*- coding: utf-8 -*-

from django.contrib import admin
from django.conf.urls import url
from . forms import CsvImportForm
from django.shortcuts import render,redirect
from . models import Personalized
from entm.models import Organizations
from waterwork.mixins import ExportCsvMixin
import unicodecsv

# Register your models here.


@admin.register(Personalized)
class PersonalizedAdmin(admin.ModelAdmin,ExportCsvMixin):
    list_display = ['belongto','ptype','loginLogo', 'webIco','homeLogo','topTitle','copyright','websiteName','recordNumber','frontPageMsg','frontPageMsgUrl']

    actions = ['export_as_csv']

    change_list_template = "heroes_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            # ...
            url('import-csv/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            reader = unicodecsv.reader(csv_file)
            # Create Hero objects from passed in data
            # ...
            headers = next(reader)
            print(headers,len(headers))
            # data = {i: v for (i, v) in enumerate(reader)}
            organ = Organizations.objects.first()
            for row in reader:
                # print(row,len(row))
                data = {headers[i]:v for (i, v) in enumerate(row)}
                
                # data = ["{}={}".format(headers[i],v) for (i, v) in enumerate(row)]
                # tdata = list("{}={}".format(k,v) for k,v in data.items())
                print(data)
                belongto_name = data["belongto"]
                try:
                    belongto = Organizations.objects.get(name=belongto_name)
                    data["belongto"] = belongto
                except:
                    data["belongto"] = organ
                    pass

                
                Personalized.objects.create(**data)
                # for i in range(len(row)):
                #     print("{}.{}={}".format(i,headers[i],row[i]))
            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "csv_form.html", payload
        )
    