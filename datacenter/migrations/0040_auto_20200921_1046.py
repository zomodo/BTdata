# Generated by Django 2.2.11 on 2020-09-21 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0039_auto_20200918_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personal',
            name='sign_date',
            field=models.CharField(max_length=16, verbose_name='计入业绩日期'),
        ),
    ]