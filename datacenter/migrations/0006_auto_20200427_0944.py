# Generated by Django 2.2.11 on 2020-04-27 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0005_auto_20200427_0943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='userid',
            field=models.IntegerField(blank=True, null=True, verbose_name='账户ID'),
        ),
    ]
