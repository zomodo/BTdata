# Generated by Django 2.2.11 on 2020-06-19 08:30

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peixuncenter', '0004_auto_20200619_1444'),
    ]

    operations = [
        migrations.AddField(
            model_name='resourceinfo',
            name='context',
            field=ckeditor_uploader.fields.RichTextUploadingField(default=1, verbose_name='专栏详细信息'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='resourceinfo',
            name='qrcode',
            field=models.ImageField(default=1, upload_to='peixun/qrcode/', verbose_name='二维码'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='resourceinfo',
            name='desc',
            field=models.TextField(default=1, max_length=128, verbose_name='描述'),
            preserve_default=False,
        ),
    ]