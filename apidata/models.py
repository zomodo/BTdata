from django.db import models

# Create your models here.

class KeyWord(models.Model):
    date=models.DateField(verbose_name='日期')
    userid=models.CharField(max_length=16,verbose_name='账户ID')
    username=models.CharField(max_length=64,verbose_name='账户名称')
    indus_1=models.CharField(max_length=32,verbose_name='一级行业')
    indus_2=models.CharField(max_length=32,verbose_name='二级行业')
    sf_name=models.CharField(max_length=32,null=True,blank=True,verbose_name='SF二级账号')
    depart_1=models.CharField(max_length=32,verbose_name='一级部门')
    depart_2=models.CharField(max_length=32,verbose_name='二级部门')
    depart_3=models.CharField(max_length=32,verbose_name='三级部门')
    keyword=models.CharField(max_length=128,verbose_name='关键词')
    consume=models.DecimalField(max_digits=10,decimal_places=2,verbose_name='消费')
    click=models.IntegerField(verbose_name='点击')
    pv=models.IntegerField(verbose_name='展现')

    class Meta:
        verbose_name=verbose_name_plural='关键词数据'
        get_latest_by = 'date'

    @classmethod
    def get_latest_date(cls):
        return cls.objects.only('date').latest().date

    def __str__(self):
        return self.keyword

class HourData(models.Model):
    date=models.DateField(verbose_name='日期')
    hour=models.IntegerField(verbose_name='时段')
    userid=models.CharField(max_length=16,verbose_name='账户ID')
    username=models.CharField(max_length=64,verbose_name='账户名称')
    indus_1=models.CharField(max_length=32,verbose_name='一级行业')
    indus_2=models.CharField(max_length=32,verbose_name='二级行业')
    sf_name=models.CharField(max_length=32,null=True,blank=True,verbose_name='SF二级账号')
    depart_1=models.CharField(max_length=32,verbose_name='一级部门')
    depart_2=models.CharField(max_length=32,verbose_name='二级部门')
    depart_3=models.CharField(max_length=32,verbose_name='三级部门')
    consume=models.DecimalField(max_digits=10,decimal_places=2,verbose_name='消费')
    click=models.IntegerField(verbose_name='点击')
    pv=models.IntegerField(verbose_name='展现')

    class Meta:
        verbose_name = verbose_name_plural = '推广时段分布'
        get_latest_by = 'date'

    def __str__(self):
        return self.userid

    @classmethod
    def get_latest_date(cls):
        return cls.objects.only('date').latest().date

class AreaData(models.Model):
    date=models.DateField(verbose_name='日期')
    userid=models.CharField(max_length=16,verbose_name='账户ID')
    username=models.CharField(max_length=64,verbose_name='账户名称')
    indus_1=models.CharField(max_length=32,verbose_name='一级行业')
    indus_2=models.CharField(max_length=32,verbose_name='二级行业')
    sf_name=models.CharField(max_length=32,null=True,blank=True,verbose_name='SF二级账号')
    depart_1=models.CharField(max_length=32,verbose_name='一级部门')
    depart_2=models.CharField(max_length=32,verbose_name='二级部门')
    depart_3=models.CharField(max_length=32,verbose_name='三级部门')
    area1=models.CharField(max_length=32,verbose_name='一级地域')
    area2=models.CharField(max_length=32, verbose_name='二级地域')
    consume=models.DecimalField(max_digits=10,decimal_places=2,verbose_name='消费')
    click=models.IntegerField(verbose_name='点击')
    pv=models.IntegerField(verbose_name='展现')

    class Meta:
        verbose_name = verbose_name_plural = '推广地域分布'
        get_latest_by = 'date'

    def __str__(self):
        return self.userid

    @classmethod
    def get_latest_date(cls):
        return cls.objects.only('date').latest().date

class NewCompany(models.Model):
    companyName=models.CharField(max_length=128,verbose_name='公司名称')
    identifier=models.CharField(max_length=64,verbose_name='统一社会信用代码',primary_key=True)
    date=models.DateField(verbose_name='注册日期')
    location=models.CharField(max_length=64,verbose_name='注册地点')
    founder=models.CharField(max_length=64,verbose_name='法人代表')
    registerMoney=models.CharField(max_length=64,verbose_name='注册资金')
    address=models.CharField(max_length=512,verbose_name='注册地址')
    companyType=models.CharField(max_length=64,verbose_name='企业类型')
    companyStatus=models.CharField(max_length=32,verbose_name='经营状态')
    makesOffer=models.CharField(max_length=1024,verbose_name='经营范围')

    class Meta:
        verbose_name = verbose_name_plural = '新注册公司数据'
        ordering = ['-date']
        get_latest_by = 'date'

    def __str__(self):
        return self.companyName

    @classmethod
    def get_latest(cls):
        latest_date=cls.objects.only('date').latest().date
        allcount=cls.objects.count()

        return latest_date,allcount


class SearchWord(models.Model):
    date=models.DateField(verbose_name='日期')
    userid=models.CharField(max_length=16,verbose_name='账户ID')
    username=models.CharField(max_length=64,verbose_name='账户名称')
    indus_1=models.CharField(max_length=32,verbose_name='一级行业')
    indus_2=models.CharField(max_length=32,verbose_name='二级行业')
    sf_name=models.CharField(max_length=32,null=True,blank=True,verbose_name='SF二级账号')
    depart_1=models.CharField(max_length=32,verbose_name='一级部门')
    depart_2=models.CharField(max_length=32,verbose_name='二级部门')
    depart_3=models.CharField(max_length=32,verbose_name='三级部门')
    searchword=models.CharField(max_length=128,verbose_name='搜索词')
    consume=models.DecimalField(max_digits=10,decimal_places=2,verbose_name='消费')
    click=models.IntegerField(verbose_name='点击')
    pv=models.IntegerField(verbose_name='展现')

    class Meta:
        verbose_name=verbose_name_plural='搜索词数据'
        get_latest_by = 'date'

    @classmethod
    def get_latest_date(cls):
        return cls.objects.only('date').latest().date

    def __str__(self):
        return self.searchword