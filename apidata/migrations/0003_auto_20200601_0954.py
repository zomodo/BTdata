# Generated by Django 2.2.11 on 2020-06-01 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apidata', '0002_auto_20200601_0953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hourdata',
            name='hour',
            field=models.CharField(max_length=4, verbose_name='时段'),
        ),
    ]