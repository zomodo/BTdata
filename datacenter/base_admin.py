from datacenter import models
from import_export.admin import ImportExportModelAdmin

class BaseDateAdmin(ImportExportModelAdmin):
    def get_queryset(self, request):
        qs=super(BaseDateAdmin, self).get_queryset(request)
        latest_date=models.Account.get_latest_date()
        return qs.filter(date=latest_date)

class BaseInvalidAdmin(ImportExportModelAdmin):
    def get_queryset(self, request):
        qs=super(BaseInvalidAdmin, self).get_queryset(request)
        latest_date=models.Invalid.get_latest_date()
        return qs.filter(date=latest_date)
