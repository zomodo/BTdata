# Generated by Django 2.2.11 on 2020-06-09 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apidata', '0009_auto_20200605_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newcompany',
            name='companyStatus',
            field=models.CharField(max_length=32, verbose_name='经营状态'),
        ),
        migrations.AlterField(
            model_name='newcompany',
            name='companyType',
            field=models.CharField(max_length=64, verbose_name='企业类型'),
        ),
        migrations.AlterField(
            model_name='newcompany',
            name='founder',
            field=models.CharField(max_length=64, verbose_name='法人代表'),
        ),
        migrations.AlterField(
            model_name='newcompany',
            name='location',
            field=models.CharField(max_length=64, verbose_name='注册地点'),
        ),
        migrations.AlterField(
            model_name='newcompany',
            name='registerMoney',
            field=models.CharField(max_length=64, verbose_name='注册资金'),
        ),
    ]