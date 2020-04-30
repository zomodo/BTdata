# Generated by Django 2.2.11 on 2020-04-26 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_firstdate',
            field=models.DateField(blank=True, null=True, verbose_name='账户首消日'),
        ),
        migrations.AlterField(
            model_name='account',
            name='feed_firstdate',
            field=models.DateField(blank=True, null=True, verbose_name='自主投放首消日'),
        ),
    ]
