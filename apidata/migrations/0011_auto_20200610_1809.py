# Generated by Django 2.2.11 on 2020-06-10 10:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apidata', '0010_auto_20200609_1053'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newcompany',
            options={'get_latest_by': 'date', 'ordering': ['-date'], 'verbose_name': '新注册公司数据', 'verbose_name_plural': '新注册公司数据'},
        ),
    ]
