from django.db import models

# Create your models here.

class Total(models.Model):
    date=models.DateField(verbose_name='日期')
    userid=models.CharField(max_length=16,verbose_name='账户ID')
    username=models.CharField(max_length=128,verbose_name='账户名称')
    customer_indus_1=models.CharField(max_length=16,null=True,blank=True,verbose_name='客户一级行业')
    customer_indus_2=models.CharField(max_length=16,null=True,blank=True,verbose_name='客户二级行业')
    account_indus_1=models.CharField(max_length=16,null=True,blank=True,verbose_name='账户一级行业')
    account_indus_2=models.CharField(max_length=16,null=True,blank=True,verbose_name='账户二级行业')
    account_type=models.CharField(max_length=16,null=True,blank=True,verbose_name='运营单位账户属性')
    register_province=models.CharField(max_length=16,null=True,blank=True,verbose_name='发证机关所在省')
    register_city=models.CharField(max_length=16, null=True, blank=True, verbose_name='发证机关所在市')
    linked_id=models.IntegerField(verbose_name='关联客户ID',null=True, blank=True)
    sf_username=models.CharField(max_length=32,verbose_name='SF二级账号')
    order_line=models.CharField(max_length=16,null=True,blank=True,verbose_name='订单行')
    health_type=models.CharField(max_length=16,verbose_name='客户行业健康度')

    allconsume=models.DecimalField(max_digits=10,decimal_places=2,verbose_name='总消费')
    searchconsume=models.DecimalField(max_digits=10,decimal_places=2,verbose_name='搜索点击消费')

    class Meta:
        verbose_name=verbose_name_plural='总消费数据'
        ordering=['-date']
        get_latest_by='date'
        unique_together=(('date','userid'),)

    def __str__(self):
        return self.username


class Feed(models.Model):
    date=models.DateField(verbose_name='日期')
    userid=models.CharField(max_length=16,verbose_name='账户ID')
    username=models.CharField(max_length=128, verbose_name='账户名称')
    order_line=models.CharField(max_length=16, null=True,blank=True,verbose_name='订单行')
    feed_ald_consume=models.DecimalField(max_digits=10,decimal_places=2,verbose_name='原生阿拉丁')
    feed_cpc_consume=models.DecimalField(max_digits=10,decimal_places=2,verbose_name='原生CPC消费')
    feed_cpm_consume = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='原生CPM消费')

    class Meta:
        verbose_name=verbose_name_plural='信息流数据'
        ordering=['-date']
        get_latest_by = 'date'
        unique_together = (('date','userid'),)

    def __str__(self):
        return self.username


class Account(models.Model):
    date=models.DateField(verbose_name='日期')
    userid=models.CharField(max_length=16,verbose_name='账户ID')
    username=models.CharField(max_length=128, verbose_name='账户名称')
    company_name=models.CharField(max_length=128,null=True,blank=True,verbose_name='公司名称')
    account_status=models.CharField(max_length=16,null=True,blank=True,verbose_name='账户状态')
    signup_date=models.DateField(verbose_name='开户日期',null=True,blank=True)
    feed_firstdate=models.DateField(verbose_name='自主投放首消日',null=True,blank=True)
    account_firstdate=models.DateField(verbose_name='账户首消日',null=True,blank=True)
    allbalance=models.DecimalField(null=True,blank=True,max_digits=10,decimal_places=2,verbose_name='推广总余额')
    website_url=models.URLField(max_length=128,verbose_name='网站URL')
    administrator=models.CharField(max_length=64,verbose_name='管理员')
    order_line=models.CharField(max_length=16,null=True,blank=True,verbose_name='订单行')
    is_rebate=models.CharField(max_length=8,verbose_name='是否高返')
    allconsume=models.DecimalField(max_digits=10,decimal_places=2,verbose_name='总消费')

    class Meta:
        verbose_name=verbose_name_plural='账户数据'
        ordering = ['-date']
        get_latest_by = 'date'
        unique_together = (('date','userid'),)

    def __str__(self):
        return self.username


class OtherPro(models.Model):
    date=models.DateField(verbose_name='日期')
    userid=models.CharField(max_length=16,verbose_name='账户ID')
    username=models.CharField(max_length=128, verbose_name='账户名称')
    order_line=models.CharField(max_length=16,null=True,blank=True,verbose_name='订单行')
    feed_gd_consume=models.DecimalField(max_digits=10,decimal_places=2,verbose_name='原生GD消费')
    qipaoxian_consume=models.DecimalField(max_digits=10,decimal_places=2,verbose_name='品牌起跑线消费')
    jvping_search=models.DecimalField(max_digits=10,decimal_places=2,verbose_name='凤巢聚屏消费')
    jvping_contract=models.DecimalField(max_digits=10,decimal_places=2,verbose_name='聚屏平台合约消费')
    jvping_compete=models.DecimalField(max_digits=10, decimal_places=2, verbose_name='聚屏平台竞价消费')
    huabiao_consume=models.DecimalField(max_digits=10, decimal_places=2, verbose_name='品牌华表消费')
    pic_consume=models.DecimalField(max_digits=10, decimal_places=2, verbose_name='图片推广消费')
    zhuanqu_consume=models.DecimalField(max_digits=10, decimal_places=2, verbose_name='品牌专区消费')
    silu_consume=models.DecimalField(max_digits=10, decimal_places=2, verbose_name='品牌丝路消费')
    zhishi_consume=models.DecimalField(max_digits=10, decimal_places=2, verbose_name='知识营销消费')
    kaiping_consume=models.DecimalField(max_digits=10, decimal_places=2, verbose_name='手百开屏消费')
    feibiao_consume=models.DecimalField(max_digits=10, decimal_places=2, verbose_name='非标消费')
    quanjing_consume=models.DecimalField(max_digits=10, decimal_places=2, verbose_name='品牌全景消费')
    xuzhang_consume=models.DecimalField(max_digits=10, decimal_places=2, verbose_name='品牌序章消费')

    class Meta:
        verbose_name=verbose_name_plural='品牌类数据'
        ordering=['-date']
        get_latest_by='date'
        unique_together = (('date', 'userid'),)

    def __str__(self):
        return self.username