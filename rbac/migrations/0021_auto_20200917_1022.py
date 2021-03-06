# Generated by Django 2.2.11 on 2020-09-17 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0020_banner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='banner',
            options={'ordering': ['-created_time'], 'verbose_name': '主页滚动图片', 'verbose_name_plural': '主页滚动图片'},
        ),
        migrations.AlterField(
            model_name='banner',
            name='img',
            field=models.ImageField(help_text='高度最大500像素，超出自动等比压缩', upload_to='banners/', verbose_name='上传图片'),
        ),
    ]
