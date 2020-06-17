from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from rbac.AdminForm import PermissionAdminForm
from rbac import models
# Register your models here.

@admin.register(models.User)
class UserAdmin(ImportExportModelAdmin):
    list_display = ['username','realname','email','show_roles']
    filter_horizontal = ['roles']

    def show_roles(self,obj):
        return [role for role in obj.roles.all()]

    show_roles.short_description = '用户角色'


@admin.register(models.Action)
class ActionAdmin(ImportExportModelAdmin):
    list_display = ['title','code']


@admin.register(models.Role)
class RoleAdmin(ImportExportModelAdmin):
    list_display = ['title','show_permissions']
    filter_horizontal = ['permissions']

    def show_permissions(self,obj):
        return [per for per in obj.permissions.all()]

    show_permissions.short_description = '角色权限'


@admin.register(models.Permission)
class PermissionAdmin(ImportExportModelAdmin):
    form = PermissionAdminForm

    list_display = ['title','url','show_action','menu']

    def show_action(self,obj):
        return [act for act in obj.action.all()]

    show_action.short_description = '操作动作'


@admin.register(models.Menu)
class MenuAdmin(ImportExportModelAdmin):
    list_display = ['title','parent']


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['type','author','show','title']
    list_filter = ['type','show']
    exclude = ['author']

    def save_model(self, request, obj, form, change):
        obj.author=request.user
        return super(MessageAdmin, self).save_model(request,obj,form,change)


admin.site.site_title='业务运营后台管理'
admin.site.site_header='业务运营后台管理'