from import_export import resources,fields
from datetime import datetime

from datacenter import models

class AccountResource(resources.ModelResource):
    date=fields.Field(column_name='日期',attribute='date')
    userid=fields.Field(column_name='账户ID',attribute='userid')
    username = fields.Field(column_name='账户名称', attribute='username')
    company_name= fields.Field(column_name='公司名称', attribute='company_name')
    account_status= fields.Field(column_name='账户状态', attribute='account_status')
    signup_date=fields.Field(column_name='开户日期',attribute='signup_date')
    feed_firstdate = fields.Field(column_name='自主投放首次消费日', attribute='feed_firstdate')
    account_firstdate= fields.Field(column_name='账户首次消费日', attribute='account_firstdate')
    allbalance= fields.Field(column_name='推广总余额', attribute='allbalance')
    website_url = fields.Field(column_name='网站URL', attribute='website_url')
    administrator = fields.Field(column_name='管理员', attribute='administrator')
    order_line = fields.Field(column_name='订单行', attribute='order_line')
    is_rebate = fields.Field(column_name='高返标识', attribute='is_rebate')
    allconsume = fields.Field(column_name='总消费', attribute='allconsume')

    def before_import_row(self, row, **kwargs):
        row['日期'] = datetime.strptime(row['data_flag'],"%Y%m%d").date()

        if row['开户日期']:
            row['开户日期'] = datetime.strptime(row['开户日期'], "%Y/%m/%d %H:%M").date()
        else:
            row['开户日期']=None

        if row['自主投放首次消费日']:
            row['自主投放首次消费日'] = datetime.strptime(row['自主投放首次消费日'], "%Y/%m/%d").date()
        else:
            row['自主投放首次消费日']=None

        if row['账户首次消费日']:
            row['账户首次消费日'] = datetime.strptime(row['账户首次消费日'], "%Y/%m/%d").date()
        else:
            row['账户首次消费日']=None

        return super(AccountResource, self).before_import_row(row,**kwargs)

    class Meta:
        model=models.Account
        skip_diff =True


class TotalResource(resources.ModelResource):
    date = fields.Field(column_name='日期', attribute='date')
    userid=fields.Field(column_name='账户ID', attribute='userid')
    username=fields.Field(column_name='账户ID', attribute='username')
    customer_indus_1=fields.Field(column_name='客户一级行业', attribute='customer_indus_1')
    customer_indus_2=fields.Field(column_name='客户二级行业', attribute='customer_indus_2')
    account_indus_1=fields.Field(column_name='账户一级行业', attribute='account_indus_1')
    account_indus_2=fields.Field(column_name='账户二级行业', attribute='account_indus_2')
    account_type=fields.Field(column_name='运营单位账户属性', attribute='account_type')
    register_province=fields.Field(column_name='发证机关所在省', attribute='register_province')
    register_city=fields.Field(column_name='发证机关所在市', attribute='register_city')
    linked_id=fields.Field(column_name='资质客户ID', attribute='linked_id')
    sf_username=fields.Field(column_name='SF对应二级账号', attribute='sf_username')
    order_line=fields.Field(column_name='订单行', attribute='order_line')
    health_type=fields.Field(column_name='客户行业健康度', attribute='health_type')
    allconsume = fields.Field(column_name='总消费', attribute='allconsume')
    searchconsume = fields.Field(column_name='搜索点击消费', attribute='searchconsume')

    def before_import_row(self, row, **kwargs):
        row['日期'] = datetime.strptime(row['data_flag'], "%Y%m%d").date()
        
        return super(TotalResource, self).before_import_row(row,**kwargs)
        
    class Meta:
        model=models.Total
        skip_diff=True