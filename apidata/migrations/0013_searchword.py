# Generated by Django 2.2.11 on 2021-03-09 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apidata', '0012_auto_20200611_1458'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='日期')),
                ('userid', models.CharField(max_length=16, verbose_name='账户ID')),
                ('username', models.CharField(max_length=64, verbose_name='账户名称')),
                ('indus_1', models.CharField(max_length=32, verbose_name='一级行业')),
                ('indus_2', models.CharField(max_length=32, verbose_name='二级行业')),
                ('sf_name', models.CharField(blank=True, max_length=32, null=True, verbose_name='SF二级账号')),
                ('depart_1', models.CharField(max_length=32, verbose_name='一级部门')),
                ('depart_2', models.CharField(max_length=32, verbose_name='二级部门')),
                ('depart_3', models.CharField(max_length=32, verbose_name='三级部门')),
                ('searchword', models.CharField(max_length=128, verbose_name='搜索词')),
                ('consume', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='消费')),
                ('click', models.IntegerField(verbose_name='点击')),
                ('pv', models.IntegerField(verbose_name='展现')),
            ],
            options={
                'verbose_name': '搜索词数据',
                'verbose_name_plural': '搜索词数据',
                'get_latest_by': 'date',
            },
        ),
    ]
