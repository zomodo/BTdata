from django.contrib import admin
from peixuncenter import models

# Register your models here.

@admin.register(models.CategoryInfo)
class CategoryInfoAdmin(admin.ModelAdmin):
    list_display = ['name','status','created_time']
    list_filter = ['status','created_time']

@admin.register(models.ResourceInfo)
class ResourcesInfoAdmin(admin.ModelAdmin):
    list_display = ['title','status','category','is_top','link']
    exclude = ['author']
    list_filter = ['title','is_top','category','status']

    def save_model(self, request, obj, form, change):
        obj.author=request.user
        return super(ResourcesInfoAdmin, self).save_model(request,obj,form,change)


@admin.register(models.ShareCategory)
class ShareCategory(admin.ModelAdmin):
    list_display = ['name','status','created_time']
    list_filter = ['status','created_time']


@admin.register(models.ShareFile)
class ShareFile(admin.ModelAdmin):
    list_display = ['title','status','category','is_top','author','created_time']
    exclude = ['author']
    list_filter = ['title','status','is_top','category']

    def save_model(self, request, obj, form, change):
        obj.author=request.user
        return super(ShareFile, self).save_model(request,obj,form,change)