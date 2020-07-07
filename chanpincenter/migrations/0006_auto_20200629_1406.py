# Generated by Django 2.2.11 on 2020-06-29 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chanpincenter', '0005_auto_20200617_1621'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='insight',
            options={'ordering': ['-is_top', '-created_time'], 'verbose_name': '营销洞察', 'verbose_name_plural': '营销洞察'},
        ),
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['-is_top', '-created_time'], 'verbose_name': '活动专题', 'verbose_name_plural': '活动专题'},
        ),
        migrations.AlterModelOptions(
            name='resource',
            options={'ordering': ['-is_top', '-created_time'], 'verbose_name': '产品资源', 'verbose_name_plural': '产品资源'},
        ),
        migrations.AlterModelOptions(
            name='shareexample',
            options={'ordering': ['-is_top', '-created_time'], 'verbose_name': '案例分享', 'verbose_name_plural': '案例分享'},
        ),
        migrations.AddField(
            model_name='insight',
            name='is_top',
            field=models.PositiveIntegerField(choices=[(1, '置顶'), (0, '不置顶')], default=0, help_text='默认不置顶', verbose_name='是否置顶'),
        ),
        migrations.AddField(
            model_name='item',
            name='is_top',
            field=models.PositiveIntegerField(choices=[(1, '置顶'), (0, '不置顶')], default=0, help_text='默认不置顶', verbose_name='是否置顶'),
        ),
        migrations.AddField(
            model_name='resource',
            name='is_top',
            field=models.PositiveIntegerField(choices=[(1, '置顶'), (0, '不置顶')], default=0, help_text='默认不置顶', verbose_name='是否置顶'),
        ),
        migrations.AddField(
            model_name='shareexample',
            name='is_top',
            field=models.PositiveIntegerField(choices=[(1, '置顶'), (0, '不置顶')], default=0, help_text='默认不置顶', verbose_name='是否置顶'),
        ),
    ]
