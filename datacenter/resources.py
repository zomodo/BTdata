from import_export import resources,fields
from import_export.fields import widgets
from datetime import datetime

from datacenter import models

class AccountResource(resources.ModelResource):
    date=fields.Field(column_name='日期',attribute='date')
    userid=fields.Field(column_name='账户ID',attribute='userid')
    username = fields.Field(column_name='账户名称', attribute='username')
    company_name= fields.Field(column_name='公司名称', attribute='company_name')
    account_indus_1=fields.Field(column_name='账户一级行业', attribute='account_indus_1')
    account_indus_2=fields.Field(column_name='账户二级行业', attribute='account_indus_2')
    account_status= fields.Field(column_name='账户状态', attribute='account_status')
    signup_date=fields.Field(column_name='开户日期',attribute='signup_date')
    feed_firstdate = fields.Field(column_name='自主投放首次消费日', attribute='feed_firstdate')
    account_firstdate= fields.Field(column_name='账户首次消费日', attribute='account_firstdate')
    allbalance= fields.Field(column_name='推广总余额', attribute='allbalance')
    website_url = fields.Field(column_name='网站URL', attribute='website_url')
    sf_username=fields.Field(column_name='SF对应二级账号', attribute='sf_username')
    administrator = fields.Field(column_name='管理员', attribute='administrator')
    order_line = fields.Field(column_name='订单行', attribute='order_line')
    is_rebate = fields.Field(column_name='累计高返', attribute='is_rebate')
    allconsume = fields.Field(column_name='总消费', attribute='allconsume')

    def before_import_row(self, row, **kwargs):
        row['日期'] = datetime.strptime(str(row['data_flag']),"%Y%m%d").date()    # 编码问题 \ufeff

        # if row['开户日期']:
        #     row['开户日期'] = datetime.strptime(str(row['开户日期']), "%Y/%m/%d %H:%M:%S").date()
        # else:
        #     row['开户日期']=None
        #
        # if row['自主投放首次消费日']:
        #     row['自主投放首次消费日'] = datetime.strptime(str(row['自主投放首次消费日']), "%Y/%m/%d").date()
        # else:
        #     row['自主投放首次消费日']=None
        #
        # if row['账户首次消费日']:
        #     row['账户首次消费日'] = datetime.strptime(str(row['账户首次消费日']), "%Y/%m/%d").date()
        # else:
        #     row['账户首次消费日']=None
        if not row['开户日期']:
            row['开户日期'] = None

        if not row['自主投放首次消费日']:
            row['自主投放首次消费日'] = None

        if not row['账户首次消费日']:
            row['账户首次消费日'] = None

        if row['推广总余额']=='':
            row['推广总余额']=0

        # 修改那些账户ID为0的数据，重命名为'op'+订单行
        if str(row['账户ID'])=='0':
            row['账户ID']='op'+str(row['订单行'])

        return super(AccountResource, self).before_import_row(row,**kwargs)

    class Meta:
        model=models.Account
        # skip_diff = True
        skip_unchanged = True
        report_skipped = False
        use_bulk = True
        force_init_instance = True


class TotalResource(resources.ModelResource):
    date = fields.Field(column_name='日期', attribute='date')
    userid=fields.Field(column_name='账户ID', attribute='userid')
    username=fields.Field(column_name='账户名称', attribute='username')
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
    fengchao_allconsume = fields.Field(column_name='凤巢总消费', attribute='fengchao_allconsume')
    feed_allconsume= fields.Field(column_name='原生总消费', attribute='feed_allconsume')
    op_allconsume=fields.Field(column_name='品牌展示总消费', attribute='op_allconsume')
    feedow_allconsume=fields.Field(column_name='原生自主投放总消费', attribute='feedow_allconsume')


    def before_import_row(self, row, **kwargs):
        row['日期'] = datetime.strptime(str(row['data_flag']), "%Y%m%d").date()

        # 修改那些账户ID为0的数据，重命名为'op'+订单行
        if str(row['账户ID'])=='0':
            row['账户ID']='op'+str(row['订单行'])

        # print(row['账户名称'])
        return super(TotalResource, self).before_import_row(row,**kwargs)
        
    class Meta:
        model=models.Total
        # skip_diff = True
        skip_unchanged = True
        report_skipped = False
        use_bulk = True
        force_init_instance = True

class FeedResource(resources.ModelResource):
    date = fields.Field(column_name='日期', attribute='date')
    userid=fields.Field(column_name='账户ID', attribute='userid')
    username=fields.Field(column_name='账户名称', attribute='username')
    account_indus_1=fields.Field(column_name='账户一级行业', attribute='account_indus_1')
    account_indus_2=fields.Field(column_name='账户二级行业', attribute='account_indus_2')
    sf_username = fields.Field(column_name='SF对应二级账号', attribute='sf_username')
    order_line=fields.Field(column_name='订单行', attribute='order_line')
    feed_allconsume = fields.Field(column_name='原生总消费', attribute='feed_allconsume')
    feed_ald_consume=fields.Field(column_name='原生阿拉丁消费', attribute='feed_ald_consume')
    feed_cpc_consume=fields.Field(column_name='原生CPC消费', attribute='feed_cpc_consume')
    feed_cpm_consume=fields.Field(column_name='原生CPM消费', attribute='feed_cpm_consume')
    baiyi_feed=fields.Field(column_name='百意Feed消费', attribute='baiyi_feed')
    baiyi_wi_cpc=fields.Field(column_name='百意无线开屏CPC消费', attribute='baiyi_wi_cpc')
    baiyi_feedGD=fields.Field(column_name='百意FeedGD消费', attribute='baiyi_feedGD')


    def before_import_row(self, row, **kwargs):
        row['日期']=datetime.strptime(str(row['data_flag']), "%Y%m%d").date()

        # 修改那些账户ID为0的数据，重命名为'op'+订单行
        if str(row['账户ID'])=='0':
            row['账户ID']='op'+str(row['订单行'])

        return super(FeedResource, self).before_import_row(row,**kwargs)

    class Meta:
        model=models.Feed
        # skip_diff=True
        skip_unchanged = True
        report_skipped = False
        use_bulk=True
        force_init_instance = True


class OtherProResource(resources.ModelResource):
    date = fields.Field(column_name='日期', attribute='date')
    userid=fields.Field(column_name='账户ID', attribute='userid')
    username=fields.Field(column_name='账户名称', attribute='username')
    account_indus_1=fields.Field(column_name='账户一级行业', attribute='account_indus_1')
    account_indus_2=fields.Field(column_name='账户二级行业', attribute='account_indus_2')
    sf_username = fields.Field(column_name='SF对应二级账号', attribute='sf_username')
    order_line=fields.Field(column_name='订单行', attribute='order_line')
    op_allconsume=fields.Field(column_name='品牌展示总消费', attribute='op_allconsume')
    feed_gd_consume=fields.Field(column_name='原生GD消费', attribute='feed_gd_consume')
    qipaoxian_consume=fields.Field(column_name='品牌起跑线消费', attribute='qipaoxian_consume')
    jvping_search=fields.Field(column_name='凤巢聚屏消费', attribute='jvping_search')
    jvping_contract=fields.Field(column_name='聚屏平台合约消费', attribute='jvping_contract')
    jvping_compete=fields.Field(column_name='聚屏平台竞价消费', attribute='jvping_compete')
    huabiao_consume=fields.Field(column_name='品牌华表消费', attribute='huabiao_consume')
    pic_consume=fields.Field(column_name='图片推广消费', attribute='pic_consume')
    zhuanqu_consume=fields.Field(column_name='品牌专区消费', attribute='zhuanqu_consume')
    silu_consume=fields.Field(column_name='品牌丝路消费', attribute='silu_consume')
    zhishi_consume=fields.Field(column_name='知识营销消费', attribute='zhishi_consume')
    kaiping_consume=fields.Field(column_name='手百开屏消费', attribute='kaiping_consume')
    feibiao_consume=fields.Field(column_name='非标消费', attribute='feibiao_consume')
    quanjing_consume=fields.Field(column_name='品牌全景消费', attribute='quanjing_consume')
    xuzhang_consume=fields.Field(column_name='品牌序章消费', attribute='xuzhang_consume')
    jvping_allconsume=fields.Field(column_name='聚屏总消费', attribute='jvping_allconsume')


    def before_import_row(self, row, **kwargs):
        row['日期']=datetime.strptime(str(row['data_flag']), "%Y%m%d").date()
        row['聚屏总消费']=float(row['凤巢聚屏消费'])+float(row['聚屏平台合约消费'])+float(row['聚屏平台竞价消费'])

        # 修改那些账户ID为0的数据，重命名为'op'+订单行
        if str(row['账户ID'])=='0':
            row['账户ID']='op'+str(row['订单行'])

        return super(OtherProResource, self).before_import_row(row,**kwargs)

    class Meta:
        model=models.OtherPro
        # skip_diff = True
        skip_unchanged = True
        report_skipped = False
        use_bulk = True
        force_init_instance = True


class Industry1Resource(resources.ModelResource):
    indus1_name=fields.Field(column_name='一级行业',attribute='indus1_name')

    class Meta:
        model=models.Industry1

class Industry2Resource(resources.ModelResource):
    indus1_name=fields.Field(
        column_name='一级行业',
        attribute='indus1_name',
        widget=widgets.ForeignKeyWidget(models.Industry1,'indus1_name')
    )
    indus2_name=fields.Field(column_name='二级行业',attribute='indus2_name')

    class Meta:
        model=models.Industry2

class InvalidResource(resources.ModelResource):
    date = fields.Field(column_name='日期', attribute='date')
    userid = fields.Field(column_name='账户ID', attribute='userid')
    username = fields.Field(column_name='账户名称', attribute='username')
    company_name = fields.Field(column_name='公司名称', attribute='company_name')
    account_indus_1 = fields.Field(column_name='账户一级行业', attribute='account_indus_1')
    account_indus_2 = fields.Field(column_name='账户二级行业', attribute='account_indus_2')
    linked_id = fields.Field(column_name='资质客户ID', attribute='linked_id')
    account_firstdate = fields.Field(column_name='账户首次消费日', attribute='account_firstdate')
    sf_username = fields.Field(column_name='SF对应二级账号', attribute='sf_username')
    depart = fields.Field(column_name='部门', attribute='depart')

    # def before_import_row(self, row, **kwargs):
    #     row['日期']=datetime.strftime(row['日期'],"%Y-%m-%d")
    #
    #     if row['账户首次消费日']:
    #         row['账户首次消费日'] = datetime.strftime(row['账户首次消费日'], "%Y-%m-%d")
    #     else:
    #         row['账户首次消费日']=None

    class Meta:
        model=models.Invalid
        # skip_diff = True
        skip_unchanged = True
        report_skipped = False
        use_bulk = True
        force_init_instance = True