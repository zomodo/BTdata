from django.db import models
from django.contrib.auth.models import User

from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

class ResourceCategory(models.Model):
    STATUS_ITEMS=(
        (1,'显示'),
        (0,'不显示')
    )
    name=models.CharField(max_length=64,verbose_name='分类名称')
    status=models.PositiveIntegerField(choices=STATUS_ITEMS,default=1,verbose_name='状态')
    created_time=models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    class Meta:
        verbose_name=verbose_name_plural='产品资源分类'
        ordering=['-created_time']

    def __str__(self):
        return self.name

class Resource(models.Model):
    IS_TOP_ITEMS=(
        (1,'置顶'),
        (0,'不置顶'),
    )
    STATUS_ITEMS=(
        (1,'显示'),
        (0,'不显示')
    )
    title=models.CharField(max_length=64,verbose_name='标题')
    desc=RichTextUploadingField(verbose_name='描述',help_text='选填',null=True,blank=True)
    status=models.PositiveIntegerField(choices=STATUS_ITEMS,default=1,verbose_name='状态')
    is_top = models.PositiveIntegerField(choices=IS_TOP_ITEMS, default=0, verbose_name='是否置顶', help_text='默认不置顶')
    author=models.ForeignKey(User,on_delete=models.DO_NOTHING,verbose_name='作者')
    category=models.ForeignKey(ResourceCategory,on_delete=models.DO_NOTHING,verbose_name='分类')
    upload_file=models.FileField(upload_to='chanpin/resources/',verbose_name='上传文件',help_text='仅限PDF文件')
    created_time=models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    class Meta:
        verbose_name=verbose_name_plural='产品资源'
        ordering=['-is_top','-created_time']

    def __str__(self):
        return self.title


class ShareExampleCategory(models.Model):
    STATUS_ITEMS=(
        (1,'显示'),
        (0,'不显示')
    )
    name=models.CharField(max_length=64,verbose_name='分类名称')
    status=models.PositiveIntegerField(choices=STATUS_ITEMS,default=1,verbose_name='状态')
    created_time=models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    class Meta:
        verbose_name=verbose_name_plural='案例分享分类'
        ordering = ['-created_time']

    def __str__(self):
        return self.name


class ShareExample(models.Model):
    IS_TOP_ITEMS=(
        (1,'置顶'),
        (0,'不置顶'),
    )
    STATUS_ITEMS=(
        (1,'显示'),
        (0,'不显示')
    )
    title=models.CharField(max_length=64,verbose_name='文章标题')
    category=models.ForeignKey(ShareExampleCategory, on_delete=models.DO_NOTHING, verbose_name='分类')
    status=models.PositiveIntegerField(choices=STATUS_ITEMS,default=1,verbose_name='状态')
    is_top = models.PositiveIntegerField(choices=IS_TOP_ITEMS, default=0, verbose_name='是否置顶', help_text='默认不置顶')
    author=models.ForeignKey(User,on_delete=models.DO_NOTHING,verbose_name='作者')
    desc=RichTextUploadingField(verbose_name='描述',help_text='选填',null=True,blank=True)
    upload_file = models.FileField(upload_to='chanpin/share_example/', verbose_name='上传文件', help_text='仅限PDF文件')
    created_time=models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    class Meta:
        verbose_name=verbose_name_plural='案例分享'
        ordering=['-is_top','-created_time']

    def __str__(self):
        return self.title

class Insight(models.Model):
    IS_TOP_ITEMS=(
        (1,'置顶'),
        (0,'不置顶'),
    )
    STATUS_ITEMS=(
        (1,'显示'),
        (0,'不显示')
    )
    title=models.CharField(max_length=64,verbose_name='文章标题')
    status=models.PositiveIntegerField(choices=STATUS_ITEMS,default=1,verbose_name='状态')
    author=models.ForeignKey(User,on_delete=models.DO_NOTHING,verbose_name='作者')
    is_top = models.PositiveIntegerField(choices=IS_TOP_ITEMS, default=0, verbose_name='是否置顶', help_text='默认不置顶')
    desc=RichTextUploadingField(verbose_name='描述',help_text='选填',null=True,blank=True)
    upload_file = models.FileField(upload_to='chanpin/insight/', verbose_name='上传文件', help_text='仅限PDF文件')
    created_time=models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    class Meta:
        verbose_name=verbose_name_plural='营销洞察'
        ordering=['-is_top','-created_time']

    def __str__(self):
        return self.title


class Item(models.Model):
    IS_TOP_ITEMS=(
        (1,'置顶'),
        (0,'不置顶'),
    )
    STATUS_ITEMS=(
        (1,'显示'),
        (0,'不显示')
    )
    title=models.CharField(max_length=64,verbose_name='文章标题')
    status=models.PositiveIntegerField(choices=STATUS_ITEMS,default=1,verbose_name='状态')
    author=models.ForeignKey(User,on_delete=models.DO_NOTHING,verbose_name='作者')
    is_top = models.PositiveIntegerField(choices=IS_TOP_ITEMS, default=0, verbose_name='是否置顶', help_text='默认不置顶')
    desc=RichTextUploadingField(verbose_name='描述',help_text='选填',null=True,blank=True)
    upload_file = models.FileField(upload_to='chanpin/item/', verbose_name='上传文件', help_text='仅限PDF文件')
    created_time=models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    class Meta:
        verbose_name=verbose_name_plural='活动专题'
        ordering=['-is_top','-created_time']

    def __str__(self):
        return self.title
