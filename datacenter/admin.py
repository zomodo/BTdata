from django.contrib import admin
from django.db import transaction
from import_export.admin import ImportExportModelAdmin
from datacenter.resources import AccountResource,TotalResource,FeedResource,OtherProResource
from datacenter.resources import Industry1Resource,Industry2Resource,InvalidResource
from datacenter.resources import PersonalResource,KAPersonalResource

from datacenter import models
from datacenter.base_admin import BaseDateAdmin,BaseInvalidAdmin

# Register your models here.

@admin.register(models.Account)
class AccountAdmin(BaseDateAdmin):
    resource_class = AccountResource
    list_display = ['date','username','company_name','website_url']

@admin.register(models.Feed)
class FeedAdmin(BaseDateAdmin):
    resource_class = FeedResource
    list_display = ['date','username','account_indus_1','account_indus_2','feed_allconsume']

@admin.register(models.Total)
class TotalAdmin(BaseDateAdmin):
    resource_class = TotalResource
    list_display = ['date','username','register_province','register_city','allconsume']

@admin.register(models.OtherPro)
class OtherProAdmin(BaseDateAdmin):
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

@admin.register(models.Invalid)
class InvalidAdmin(BaseInvalidAdmin):
    resource_class = InvalidResource
    list_display = ['date','username','company_name','account_firstdate','depart']

@admin.register(models.Personal)
class PersonalAdmin(ImportExportModelAdmin):
    resource_class = PersonalResource
    list_display = ['date','userid','company_name','frame1']

@admin.register(models.KAPersonal)
class KAPersonalAdmin(ImportExportModelAdmin):
    resource_class = KAPersonalResource
    list_display = ['date','userid','company_name','frame1']

@admin.register(models.MEGIndustry1)
class MEGIndustry1Admin(admin.ModelAdmin):
    list_display = ['meg_indus1_name']

@admin.register(models.MEGIndustry2)
class MEGIndustry2Admin(admin.ModelAdmin):
    list_display = ['meg_indus1_name','meg_indus2_name']