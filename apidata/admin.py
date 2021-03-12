from django.contrib import admin
from apidata import models

# Register your models here.

@admin.register(models.KeyWord)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ['date','username','indus_1','indus_2','keyword']

    def get_queryset(self, request):
        qs=super(KeywordAdmin, self).get_queryset(request)
        latest_date=models.KeyWord.get_latest_date()
        return qs.filter(date=latest_date)

@admin.register(models.HourData)
class HourAdmin(admin.ModelAdmin):
    list_display = ['date','username','indus_1','indus_2']
    
    def get_queryset(self, request):
        qs=super(HourAdmin, self).get_queryset(request)
        latest_date=models.HourData.get_latest_date()
        return qs.filter(date=latest_date)

@admin.register(models.AreaData)
class AreaAdmin(admin.ModelAdmin):
    list_display = ['date','username','indus_1','indus_2','area1','area2']

    def get_queryset(self, request):
        qs=super(AreaAdmin, self).get_queryset(request)
        latest_date=models.AreaData.get_latest_date()
        return qs.filter(date=latest_date)

@admin.register(models.NewCompany)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['date','companyName','location']


@admin.register(models.SearchWord)
class SearchWordAdmin(admin.ModelAdmin):
    list_display = ['date','username','indus_1','indus_2','searchword']

    def get_queryset(self, request):
        qs=super(SearchWordAdmin, self).get_queryset(request)
        latest_date=models.SearchWord.get_latest_date()
        return qs.filter(date=latest_date)