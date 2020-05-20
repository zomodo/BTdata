from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from datacenter.resources import AccountResource,TotalResource,FeedResource,OtherProResource
from datacenter.resources import Industry1Resource,Industry2Resource

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

@admin.register(models.QuarterTask)
class QuarterTaskAdmin(ImportExportModelAdmin):
    list_display = ['date','name','qconsume_task']

@admin.register(models.Industry1)
class Industry1Admin(ImportExportModelAdmin):
    resource_class = Industry1Resource
    list_display = ['indus1_name']

@admin.register(models.Industry2)
class Industry2Admin(ImportExportModelAdmin):
    resource_class = Industry2Resource
    list_display = ['indus1_name','indus2_name']