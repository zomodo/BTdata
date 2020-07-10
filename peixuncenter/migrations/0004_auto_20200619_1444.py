# Generated by Django 2.2.11 on 2020-06-19 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peixuncenter', '0003_auto_20200619_1021'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resourceinfo',
            name='qrcode',
        ),
        migrations.AddField(
            model_name='resourceinfo',
            name='image',
            field=models.ImageField(default=1, upload_to='peixun/cover/', verbose_name='封面图片'),
            preserve_default=False,
        ),
    ]