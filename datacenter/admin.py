from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from datacenter.resources import AccountResource,TotalResource,FeedResource,OtherProResource

from datacenter import models

# Register your models here.

@admin.register(models.Account)
class AccountAdmin(ImportExportModelAdmin):
    resource_class = AccountResource
    list_display = ['date','username','company_name','website_url']

@admin.register(models.Feed)
class FeedAdmin(ImportExportModelAdmin):
    resource_class = FeedResource
    list_display = ['date','username','account_indus_1','account_indus_2','feed_allconsume']

@admin.register(models.Total)
class TotalAdmin(ImportExportModelAdmin):
    resource_class = TotalResource
    list_display = ['date','username','register_province','register_city','allconsume']

@admin.register(models.OtherPro)
class OtherProAdmin(ImportExportModelAdmin):
    resource_class = OtherProResource
    list_display = ['date','username','account_indus_1','account_indus_2','op_allconsume']