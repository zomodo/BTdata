from django.contrib import admin
from apidata import models

# Register your models here.

@admin.register(models.KeyWord)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ['date','username','indus_1','indus_2','keyword']


@admin.register(models.HourData)
class HourAdmina(admin.ModelAdmin):
    list_display = ['date','username','indus_1','indus_2']


@admin.register(models.AreaData)
class AreaAdmin(admin.ModelAdmin):
    list_display = ['date','username','indus_1','indus_2','area1','area2']


@admin.register(models.NewCompany)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['date','companyName','location']

