from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class CategoryInfo(models.Model):
    STATUS_ITEMS=(
        (1,'显示'),
        (0,'不显示')
    )
    name=models.CharField(max_length=64,verbose_name='分类名称')
    status=models.PositiveIntegerField(choices=STATUS_ITEMS,default=1,verbose_name='状态')
    created_time=models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    class Meta:
        verbose_name=verbose_name_plural='培训资源分类'
        ordering=['-created_time']

    def __str__(self):
        return self.name

class ResourceInfo(models.Model):
    IS_TOP_ITEMS=(
        (1,'置顶'),
        (0,'不置顶'),
    )

    STATUS_ITEMS=(
        (1,'显示'),
        (0,'不显示')
    )
    title=models.CharField(max_length=64,verbose_name='标题')
    link=models.URLField(verbose_name='小鹅通链接',null=True,blank=True,help_text='选填')
    is_top=models.PositiveIntegerField(choices=IS_TOP_ITEMS,default=0,verbose_name='是否置顶',help_text='默认不置顶')
    image=models.ImageField(upload_to='peixun/cover/',verbose_name='封面图片')
    qrcode=models.ImageField(upload_to='peixun/qrcode/',verbose_name='二维码')
    desc=models.TextField(max_length=128,verbose_name='描述')
    status=models.PositiveIntegerField(choices=STATUS_ITEMS,default=1,verbose_name='状态')
    author=models.ForeignKey(User,on_delete=models.DO_NOTHING,verbose_name='作者')
    context=RichTextUploadingField(verbose_name='专栏详细信息')
    category=models.ForeignKey(CategoryInfo,on_delete=models.DO_NOTHING,verbose_name='分类')
    created_time=models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    class Meta:
        verbose_name=verbose_name_plural='培训资源'
        ordering=['-is_top','-created_time']

    def __str__(self):
        return self.title


class ShareCategory(models.Model):
    STATUS_ITEMS=(
        (1,'显示'),
        (0,'不显示')
    )
    name=models.CharField(max_length=64,verbose_name='分类名称')
    status=models.PositiveIntegerField(choices=STATUS_ITEMS,default=1,verbose_name='状态')
    created_time=models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    class Meta:
        verbose_name=verbose_name_plural='资讯分类'
        ordering = ['-created_time']

    def __str__(self):
        return self.name


class ShareFile(models.Model):
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
    is_top=models.PositiveIntegerField(choices=IS_TOP_ITEMS,default=0,verbose_name='是否置顶',help_text='默认不置顶')
    author=models.ForeignKey(User,on_delete=models.DO_NOTHING,verbose_name='作者')
    category=models.ForeignKey(ShareCategory,on_delete=models.DO_NOTHING,verbose_name='资讯分类')
    desc=RichTextUploadingField(verbose_name='描述',help_text='选填',null=True,blank=True)
    upload_file = models.FileField(upload_to='peixun/share_file/', verbose_name='上传文件', help_text='仅限PDF文件')
    created_time=models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    class Meta:
        verbose_name=verbose_name_plural='资讯速分享'
        ordering=['-is_top','-created_time']

    def __str__(self):
        return self.title