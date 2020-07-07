# Generated by Django 2.2.11 on 2020-06-30 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chanpincenter', '0006_auto_20200629_1406'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='resourcecategory',
            options={'ordering': ['-created_time'], 'verbose_name': '产品资源分类', 'verbose_name_plural': '产品资源分类'},
        ),
        migrations.AlterModelOptions(
            name='shareexamplecategory',
            options={'ordering': ['-created_time'], 'verbose_name': '案例分享分类', 'verbose_name_plural': '案例分享分类'},
        ),
        migrations.AlterField(
            model_name='insight',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='item',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='resourcecategory',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='shareexample',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='shareexamplecategory',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
    ]
