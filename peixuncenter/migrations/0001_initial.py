# Generated by Django 2.2.11 on 2020-06-19 01:52

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='分类名称')),
                ('status', models.PositiveIntegerField(choices=[(1, '显示'), (0, '不显示')], default=1, verbose_name='状态')),
                ('created_time', models.DateField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '培训资源分类',
                'verbose_name_plural': '培训资源分类',
            },
        ),
        migrations.CreateModel(
            name='ResourceInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='标题')),
                ('link', models.URLField(verbose_name='文章链接')),
                ('qrcode', models.ImageField(upload_to='peixun/QRcode/', verbose_name='二维码')),
                ('desc', ckeditor_uploader.fields.RichTextUploadingField(blank=True, help_text='选填', null=True, verbose_name='描述')),
                ('status', models.PositiveIntegerField(choices=[(1, '显示'), (0, '不显示')], default=1, verbose_name='状态')),
                ('created_time', models.DateField(auto_now_add=True, verbose_name='创建时间')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='作者')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='peixuncenter.CategoryInfo', verbose_name='分类')),
            ],
            options={
                'verbose_name': '培训资源',
                'verbose_name_plural': '培训资源',
                'ordering': ['-created_time'],
            },
        ),
    ]
