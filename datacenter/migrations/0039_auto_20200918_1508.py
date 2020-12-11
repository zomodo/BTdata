# Generated by Django 2.2.11 on 2020-09-18 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0038_auto_20200918_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='personal',
            name='sf_name',
            field=models.CharField(default=555, max_length=64, verbose_name='SF二级账号'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='personal',
            name='sign_date',
            field=models.DateField(verbose_name='计入业绩日期'),
        ),
    ]