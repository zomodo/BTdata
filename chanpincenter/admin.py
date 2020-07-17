from django.contrib import admin
from chanpincenter import models

# Register your models here.

@admin.register(models.ResourceCategory)
class ResourceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name','status','created_time']
    list_filter = ['status']

@admin.register(models.Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['title','status','author','category','is_top','created_time']
    exclude = ['author']
    list_filter = ['title','status','category','is_top']
    fieldsets = (
        ('分类',{
            'fields':(
                'category',
            )
        }),
        ('配置',{
            'fields':(
                ('is_top','status'),
            )
        }),
        ('内容', {
            'fields': (
                'title',
                'upload_file',
            )
        }),
        ('描述', {
            'fields': (
                'desc',
            )
        }),

    )

    def save_model(self, request, obj, form, change):
        obj.author=request.user
        return super(ResourceAdmin, self).save_model(request,obj,form,change)


@admin.register(models.ShareExampleCategory)
class ShareExampleCategoryAdmin(admin.ModelAdmin):
    list_display = ['name','status','created_time']

@admin.register(models.ShareExample)
class ShareExampleAdmin(admin.ModelAdmin):
    list_display = ['title', 'status','author','category','is_top', 'created_time']
    exclude = ['author']
    list_filter = ['title', 'status', 'category', 'is_top']
    fieldsets = (
        ('分类',{
            'fields':(
                'category',
            )
        }),
        ('配置',{
            'fields':(
                ('is_top','status'),
            )
        }),
        ('内容', {
            'fields': (
                'title',
                'upload_file',
            )
        }),
        ('描述', {
            'fields': (
                'desc',
            )
        }),

    )

    def save_model(self, request, obj, form, change):
        obj.author=request.user
        return super(ShareExampleAdmin, self).save_model(request,obj,form,change)


@admin.register(models.Insight)
class InsightAdmin(admin.ModelAdmin):
    list_display = ['title', 'status','author','is_top','created_time']
    exclude = ['author']
    list_filter = ['title', 'status', 'is_top']
    fieldsets = (
        ('配置',{
            'fields':(
                ('is_top','status'),
            ),
        }),
        ('内容', {
            'fields': (
                'title',
                'upload_file',
            )
        }),
        ('描述', {
            'fields': (
                'desc',
            )
        }),

    )

    def save_model(self, request, obj, form, change):
        obj.author=request.user
        return super(InsightAdmin, self).save_model(request,obj,form,change)


@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'status','author','is_top','created_time']
    exclude = ['author']
    list_filter = ['title', 'status', 'is_top']
    fieldsets = (
        ('配置',{
            'fields':(
                ('is_top','status'),
            ),
        }),
        ('内容', {
            'fields': (
                'title',
                'upload_file',
            )
        }),
        ('描述', {
            'fields': (
                'desc',
            )
        }),

    )

    def save_model(self, request, obj, form, change):
        obj.author=request.user
        return super(ItemAdmin, self).save_model(request,obj,form,change)