# Generated by Django 2.2.11 on 2020-04-26 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0002_auto_20200426_1710'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='account',
            unique_together=set(),
        ),
    ]
