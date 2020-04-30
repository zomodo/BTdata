from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from datacenter.resources import AccountResource,TotalResource

from datacenter import models

# Register your models here.

@admin.register(models.Account)
class AccountAdmin(ImportExportModelAdmin):
    resource_class = AccountResource
    list_display = ['date','username','company_name','website_url']

@admin.register(models.Feed)
class FeedAdmin(ImportExportModelAdmin):
    list_display = ['date','username']

@admin.register(models.Total)
class TotalAdmin(ImportExportModelAdmin):
    resource_class = TotalResource
    list_display = ['date','username']

@admin.register(models.OtherPro)
class OtherProAdmin(ImportExportModelAdmin):
    list_display = ['date','username']