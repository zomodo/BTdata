from django.db import models
from django.contrib.auth.models import User as AuthUser

from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

class Menu(models.Model):
    title=models.CharField(max_length=20,verbose_name='菜单标题')
    parent=models.ForeignKey('self',null=True,blank=True,verbose_name='父菜单',on_delete=models.CASCADE)

    def __str__(self):
        # 显示层级菜单
        title_list=[self.title]
        p=self.parent
        while p:
            title_list.insert(0,p.title)
            p=p.parent

        return '-'.join(title_list)

    class Meta:
        verbose_name=verbose_name_plural="菜单信息"


class Action(models.Model):
    title=models.CharField(max_length=20,verbose_name='操作名称')
    code=models.CharField(max_length=10,verbose_name='code')
    def __str__(self):
        return self.title

    class Meta:
        verbose_name=verbose_name_plural="操作动作"


class Permission(models.Model):
    title = models.CharField(max_length=32,verbose_name = '链接标题')
    url = models.CharField(max_length=128,verbose_name='链接URL')
    action = models.ManyToManyField("Action",verbose_name='操作动作')
    menu = models.ForeignKey("Menu", null=True, blank=True,on_delete=models.CASCADE,verbose_name='附属菜单')

    def __str__(self):
        # 显示带菜单前缀的权限
        return '{menu}/{title}{action}'.format(menu=self.menu, title=self.title,action=[i.title for i in self.action.all()])

    class Meta:
        verbose_name=verbose_name_plural="权限信息"


class Role(models.Model):
    title = models.CharField(max_length=32, unique=True,verbose_name='角色名称')
    permissions = models.ManyToManyField("Permission",verbose_name='角色权限')
    # 定义角色和权限的多对多关系

    def __str__(self):
        return self.title

    class Meta:
        verbose_name=verbose_name_plural="角色信息"


class User(models.Model):
    username = models.CharField(max_length=32,verbose_name='账户名称')
    password = models.CharField(max_length=64,verbose_name='账户密码')
    email = models.EmailField(verbose_name='邮箱')
    realname = models.CharField(max_length=32,verbose_name='真实姓名')
    roles = models.ManyToManyField("Role",verbose_name='分配角色')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name=verbose_name_plural="用户信息"


class Message(models.Model):

    DEPART_ITEMS=(
        (0,'数据中心'),
        (1,'策略中心'),
        (2,'百推学院'),
    )

    IS_TOP_ITEMS=(
        (1,'置顶'),
        (0,'不置顶'),
    )

    STATUS_ITEMS=(
        (1,'显示'),
        (0,'不显示'),
    )
    depart=models.PositiveIntegerField(choices=DEPART_ITEMS,verbose_name='部门')
    author=models.ForeignKey(AuthUser,on_delete=models.DO_NOTHING,verbose_name='作者')
    is_top = models.PositiveIntegerField(choices=IS_TOP_ITEMS, default=0, verbose_name='是否置顶', help_text='默认不置顶')
    is_jump=models.BooleanField(default=False,verbose_name='是否跳转',help_text='勾选，输入链接，去掉勾选，输入文本')
    status=models.PositiveIntegerField(choices=STATUS_ITEMS,default=1,verbose_name='是否显示',help_text='默认显示')
    title=models.CharField(max_length=64,verbose_name='标题')
    content=models.TextField(verbose_name='内容')
    created_time=models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    class Meta:
        verbose_name=verbose_name_plural='消息通知'
        ordering=['-is_top','-created_time']

    def __str__(self):
        return self.title