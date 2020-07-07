# Generated by Django 2.2.11 on 2020-06-17 08:18

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chanpincenter', '0003_shareexample_shareexamplecategory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Insight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='文章标题')),
                ('status', models.PositiveIntegerField(choices=[(1, '显示'), (0, '不显示')], default=1, verbose_name='状态')),
                ('desc', ckeditor_uploader.fields.RichTextUploadingField(blank=True, help_text='选填', null=True, verbose_name='描述')),
                ('upload_file', models.FileField(help_text='仅限PDF文件', upload_to='chanpin/insight/', verbose_name='上传文件')),
                ('created_time', models.DateField(auto_now_add=True, verbose_name='创建时间')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='作者')),
            ],
            options={
                'verbose_name': '案例分享',
                'verbose_name_plural': '案例分享',
                'ordering': ['-created_time'],
            },
        ),
    ]
