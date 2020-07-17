# Generated by Django 2.2.11 on 2020-07-16 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0012_auto_20200630_1511'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_jump',
            field=models.PositiveIntegerField(choices=[(1, '跳转'), (0, '不跳转')], default=0, help_text='意思是输入跳转链接还是描述内容', verbose_name='是否跳转'),
        ),
    ]
