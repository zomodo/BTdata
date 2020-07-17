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
    fieldsets = (
        ('分类',{
            'fields':(
                'category',
            ),
        }),
        ('配置',{
            'fields':(
                ('is_top','status'),
            ),
        }),
        ('详细信息',{
            'fields':(
                'title',
                'link',
                'image',
                'qrcode',
                'desc',
                'context',
            ),
        }),
    )

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
    fieldsets = (
        ('分类',{
            'fields':(
                'category',
            ),
        }),
        ('配置',{
            'fields':(
                ('is_top','status'),
            ),
        }),
        ('内容',{
            'fields':(
                'title',
                'upload_file',
            ),
        }),
        ('描述',{
            'fields':(
                'desc',
            ),
        })
    )

    def save_model(self, request, obj, form, change):
        obj.author=request.user
        return super(ShareFile, self).save_model(request,obj,form,change)