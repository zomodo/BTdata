from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import datetime
import calendar
from datacenter import models

from django.db.models import Sum,Count,Avg,Q
# Create your views here.


# 总消费
def allconsume(request):
    # 数据最新日期
    latest_date=models.Account.get_latest_date()
    # print(latest_date)
    # 前一天日期，做环比
    yesterday=latest_date+datetime.timedelta(days=-1)
    # 前七天日期，做同比
    lastweek=latest_date+datetime.timedelta(days=-7)


    # 计算最新日期数据
    bothconsume=models.Total.objects.filter(date=latest_date).aggregate(
        allconsume=Sum('allconsume'),
        fengchao_allconsume=Sum('fengchao_allconsume'),
        feed_allconsume=Sum('feed_allconsume'),
        op_allconsume=Sum('op_allconsume'),
    )

    # 计算前一天数据
    bothconsume_l1=models.Total.objects.filter(date=yesterday).aggregate(
        allconsume=Sum('allconsume'),
        fengchao_allconsume=Sum('fengchao_allconsume'),
        feed_allconsume=Sum('feed_allconsume'),
        op_allconsume=Sum('op_allconsume'),
    )

    # 计算七天前数据
    bothconsume_l7=models.Total.objects.filter(date=lastweek).aggregate(
        allconsume=Sum('allconsume'),
        fengchao_allconsume=Sum('fengchao_allconsume'),
        feed_allconsume=Sum('feed_allconsume'),
        op_allconsume=Sum('op_allconsume'),
    )

    # 计算环比
    allconsume_compare_l1='{:.2%}'.format(bothconsume['allconsume'] / bothconsume_l1['allconsume'] -1)
    fengchaoconsume_compare_l1='{:.2%}'.format(bothconsume['fengchao_allconsume'] / bothconsume_l1['fengchao_allconsume'] -1)
    feedconsume_compare_l1='{:.2%}'.format(bothconsume['feed_allconsume'] / bothconsume_l1['feed_allconsume'] -1)
    opconsume_compare_l1='{:.2%}'.format(bothconsume['op_allconsume'] / bothconsume_l1['op_allconsume'] -1)

    # 计算同比
    allconsume_compare_l7='{:.2%}'.format(bothconsume['allconsume'] / bothconsume_l7['allconsume'] -1)
    fengchaoconsume_compare_l7='{:.2%}'.format(bothconsume['fengchao_allconsume'] / bothconsume_l7['fengchao_allconsume'] -1)
    feedconsume_compare_l7='{:.2%}'.format(bothconsume['feed_allconsume'] / bothconsume_l7['feed_allconsume'] -1)
    opconsume_compare_l7='{:.2%}'.format(bothconsume['op_allconsume'] / bothconsume_l7['op_allconsume'] -1)

    today_consume={
        'date':latest_date,
        'allconsume':bothconsume['allconsume'],
        'fengchaoconsume':bothconsume['fengchao_allconsume'],
        'feedconsume':bothconsume['feed_allconsume'],
        'opconsume':bothconsume['op_allconsume']
    }
    compare_l1={
        'allconsume_compare_l1':allconsume_compare_l1,
        'fengchaoconsume_compare_l1':fengchaoconsume_compare_l1,
        'feedconsume_compare_l1':feedconsume_compare_l1,
        'opconsume_compare_l1':opconsume_compare_l1,
    }
    compare_l7={
        'allconsume_compare_l7': allconsume_compare_l7,
        'fengchaoconsume_compare_l7': fengchaoconsume_compare_l7,
        'feedconsume_compare_l7': feedconsume_compare_l7,
        'opconsume_compare_l7': opconsume_compare_l7,
    }

    context={
        'today_consume':today_consume,
        'compare_l1':compare_l1,
        'compare_l7':compare_l7,
    }

    return render(request, 'datacenter/allconsume.html', context)


# 总消费-图表
def allconsume_chart(request):
    # 数据最新日期
    latest_date = models.Account.get_latest_date()
    # 前14天日期，做曲线图
    last14_date=latest_date+datetime.timedelta(days=-14)

    date_list = []
    allconsume_list = []
    fengchaoconsume_list = []
    feedconsume_list = []
    opconsume_list = []

    # 计算消费的趋势图
    bothconsume_last14=models.Total.objects.values('date').\
        filter(date__range=(last14_date,latest_date)).\
        annotate(
        all=Sum('allconsume'),
        fengchao=Sum('fengchao_allconsume'),
        feed=Sum('feed_allconsume'),
        op=Sum('op_allconsume'),
    ).order_by('date')
    #print(bothconsume_last14)
    for data in bothconsume_last14:
        date_list.append(data['date'])
        allconsume_list.append(float(data['all']))
        fengchaoconsume_list.append(float(data['fengchao']))
        feedconsume_list.append(float(data['feed']))
        opconsume_list.append(float(data['op']))

    context={
        'date':date_list,
        'allconsume':allconsume_list,
        'fengchaoconsume':fengchaoconsume_list,
        'feedconsume':feedconsume_list,
        'opconsume':opconsume_list,
    }

    return JsonResponse(context)


# 处理有消费账户数
def allaccount(request):
    # 数据最新日期
    latest_date=models.Account.get_latest_date()
    # 前一天日期，做环比
    yesterday=latest_date+datetime.timedelta(days=-1)
    # 前七天日期，做同比
    lastweek=latest_date+datetime.timedelta(days=-7)

    # 计算最新日期数据
    allcount=models.Total.objects.filter(date=latest_date,allconsume__gt=0).aggregate(allcount=Count('userid'))
    fengchaocount=models.Total.objects.filter(date=latest_date,fengchao_allconsume__gt=0).aggregate(fengchaocount=Count('userid'))
    feedcount=models.Total.objects.filter(date=latest_date,feed_allconsume__gt=0).aggregate(feedcount=Count('userid'))
    opcount=models.Total.objects.filter(date=latest_date,op_allconsume__gt=0).aggregate(opcount=Count('userid'))

    # 计算前一天数据
    allcount_l1=models.Total.objects.filter(date=yesterday,allconsume__gt=0).aggregate(allcount=Count('userid'))
    fengchaocount_l1=models.Total.objects.filter(date=yesterday,fengchao_allconsume__gt=0).aggregate(fengchaocount=Count('userid'))
    feedcount_l1=models.Total.objects.filter(date=yesterday,feed_allconsume__gt=0).aggregate(feedcount=Count('userid'))
    opcount_l1=models.Total.objects.filter(date=yesterday,op_allconsume__gt=0).aggregate(opcount=Count('userid'))

    # 计算前七天数据
    allcount_l7=models.Total.objects.filter(date=lastweek,allconsume__gt=0).aggregate(allcount=Count('userid'))
    fengchaocount_l7=models.Total.objects.filter(date=lastweek,fengchao_allconsume__gt=0).aggregate(fengchaocount=Count('userid'))
    feedcount_l7=models.Total.objects.filter(date=lastweek,feed_allconsume__gt=0).aggregate(feedcount=Count('userid'))
    opcount_l7=models.Total.objects.filter(date=lastweek,op_allconsume__gt=0).aggregate(opcount=Count('userid'))

    # 计算环比
    allcount_compare_l1='{:.2%}'.format(allcount['allcount'] / allcount_l1['allcount'] -1)
    fengchaocount_compare_l1='{:.2%}'.format(fengchaocount['fengchaocount'] / fengchaocount_l1['fengchaocount'] -1)
    feedcount_compare_l1='{:.2%}'.format(feedcount['feedcount'] / feedcount_l1['feedcount'] -1)
    opcount_compare_l1='{:.2%}'.format(opcount['opcount'] / opcount_l1['opcount'] -1)

    # 计算同比
    allcount_compare_l7='{:.2%}'.format(allcount['allcount'] / allcount_l7['allcount'] -1)
    fengchaocount_compare_l7='{:.2%}'.format(fengchaocount['fengchaocount'] / fengchaocount_l7['fengchaocount'] -1)
    feedcount_compare_l7='{:.2%}'.format(feedcount['feedcount'] / feedcount_l7['feedcount'] -1)
    opcount_compare_l7='{:.2%}'.format(opcount['opcount'] / opcount_l7['opcount'] -1)

    today_count={
        'date':latest_date,
        'allcount':allcount['allcount'],
        'fengchaocount':fengchaocount['fengchaocount'],
        'feedcount':feedcount['feedcount'],
        'opcount':opcount['opcount']
    }
    compare_l1={
        'allcount_compare_l1':allcount_compare_l1,
        'fengchaocount_compare_l1':fengchaocount_compare_l1,
        'feedcount_compare_l1':feedcount_compare_l1,
        'opcount_compare_l1':opcount_compare_l1,
    }

    compare_l7={
        'allcount_compare_l7': allcount_compare_l7,
        'fengchaocount_compare_l7': fengchaocount_compare_l7,
        'feedcount_compare_l7': feedcount_compare_l7,
        'opcount_compare_l7': opcount_compare_l7,
    }

    context={
        'today_count':today_count,
        'compare_l1':compare_l1,
        'compare_l7':compare_l7,
    }

    return render(request,'datacenter/allaccount.html',context)


# 有消费账户数-图表
def allaccount_chart(request):
    # 数据最新日期
    latest_date = models.Account.get_latest_date()
    # 前14天日期，做曲线图
    last14_date=latest_date+datetime.timedelta(days=-14)

    date_list = []
    allcount_list = []
    fengchaocount_list = []
    feedcount_list = []
    opcount_list = []

    # 计算有消费账户数趋势
    allcount=models.Total.objects.filter(date__gte=last14_date,date__lte=latest_date,allconsume__gt=0).values('date').annotate(all=Count('userid')).order_by('date')
    fengchaocount=models.Total.objects.filter(date__gte=last14_date,date__lte=latest_date,fengchao_allconsume__gt=0).values('date').annotate(fengchao=Count('userid')).order_by('date')
    feedcount=models.Total.objects.filter(date__gte=last14_date,date__lte=latest_date,feed_allconsume__gt=0).values('date').annotate(feed=Count('userid')).order_by('date')
    opcount=models.Total.objects.filter(date__gte=last14_date,date__lte=latest_date,op_allconsume__gt=0).values('date').annotate(op=Count('userid')).order_by('date')

    for adata in allcount:
        date_list.append(adata['date'])
        allcount_list.append(adata['all'])

    for fcdata in fengchaocount:
        fengchaocount_list.append(fcdata['fengchao'])

    for fddata in feedcount:
        feedcount_list.append(fddata['feed'])

    for opdata in opcount:
        opcount_list.append(opdata['op'])

    context={
        'date':date_list,
        'allcount':allcount_list,
        'fengchaocount':fengchaocount_list,
        'feedcount':feedcount_list,
        'opcount':opcount_list,
    }

    return JsonResponse(context)


# 处理整体数据
def more_all(request):
    # 数据最新日期
    latest_date = models.Account.get_latest_date()
    # 前一天日期，做环比
    yesterday = latest_date + datetime.timedelta(days=-1)
    # 前七天日期，做同比
    lastweek = latest_date + datetime.timedelta(days=-7)


    if request.method=='GET':

        """ 计算当日数据，前日数据，日环比，周同比 """
        # 计算最新日期数据
        allconsume = models.Total.objects.filter(date=latest_date).aggregate(allconsume=Sum('allconsume'))
        feedconsume = models.Feed.objects.filter(date=latest_date).aggregate(feedconsume=Sum('feed_allconsume'))
        opconsume = models.OtherPro.objects.filter(date=latest_date).aggregate(opconsume=Sum('op_allconsume'))

        # 计算前一天数据
        allconsume_l1 = models.Total.objects.filter(date=yesterday).aggregate(allconsume=Sum('allconsume'))
        feedconsume_l1 = models.Feed.objects.filter(date=yesterday).aggregate(feedconsume=Sum('feed_allconsume'))
        opconsume_l1 = models.OtherPro.objects.filter(date=yesterday).aggregate(opconsume=Sum('op_allconsume'))

        # 计算前七天数据
        allconsume_l7 = models.Total.objects.filter(date=lastweek).aggregate(allconsume=Sum('allconsume'))
        feedconsume_l7 = models.Feed.objects.filter(date=lastweek).aggregate(feedconsume=Sum('feed_allconsume'))
        opconsume_l7 = models.OtherPro.objects.filter(date=lastweek).aggregate(opconsume=Sum('op_allconsume'))

        # 计算环比
        allconsume_compare_l1 = '{:.2%}'.format(allconsume['allconsume'] / allconsume_l1['allconsume'] - 1)
        feedconsume_compare_l1 = '{:.2%}'.format(feedconsume['feedconsume'] / feedconsume_l1['feedconsume'] - 1)
        opconsume_compare_l1 = '{:.2%}'.format(opconsume['opconsume'] / opconsume_l1['opconsume'] - 1)

        # 计算同比
        allconsume_compare_l7 = '{:.2%}'.format(allconsume['allconsume'] / allconsume_l7['allconsume'] - 1)
        feedconsume_compare_l7 = '{:.2%}'.format(feedconsume['feedconsume'] / feedconsume_l7['feedconsume'] - 1)
        opconsume_compare_l7 = '{:.2%}'.format(opconsume['opconsume'] / opconsume_l7['opconsume'] - 1)

        normal_consume={
            'allconsume':allconsume['allconsume'],
            'feedconsume':feedconsume['feedconsume'],
            'opconsume': opconsume['opconsume'],

            'allconsume_l1': allconsume_l1['allconsume'],
            'feedconsume_l1': feedconsume_l1['feedconsume'],
            'opconsume_l1': opconsume_l1['opconsume'],

            'allconsume_compare_l1': allconsume_compare_l1,
            'feedconsume_compare_l1':feedconsume_compare_l1,
            'opconsume_compare_l1':opconsume_compare_l1,

            'allconsume_compare_l7': allconsume_compare_l7,
            'feedconsume_compare_l7': feedconsume_compare_l7,
            'opconsume_compare_l7': opconsume_compare_l7,
        }

        """ 计算时间进度 """
        # 计算季度第一天
        quarter_start_day = datetime.date(latest_date.year, latest_date.month - (latest_date.month - 1) % 3, 1)
        # 计算季度已过的时间长度
        cost_days = (latest_date - quarter_start_day).days + 1
        # 计算当前季度
        quarter_num = (int(latest_date.strftime('%m')) - 1) // 3 + 1
        # 计算当前季度的长度
        quarter_days = 0
        if quarter_num == 1:
            for i in range(1, 4):
                quarter_days += calendar.monthrange(int(latest_date.strftime('%Y')), i)[1]
        elif quarter_num == 2:
            for i in range(4, 7):
                quarter_days += calendar.monthrange(int(latest_date.strftime('%Y')), i)[1]
        elif quarter_num == 3:
            for i in range(7, 10):
                quarter_days += calendar.monthrange(int(latest_date.strftime('%Y')), i)[1]
        elif quarter_num == 4:
            for i in range(10, 13):
                quarter_days += calendar.monthrange(int(latest_date.strftime('%Y')), i)[1]

        cost_time_ratio='{:.2%}'.format(cost_days/quarter_days)

        cost_time={
            'date':latest_date,
            'cost_time_ratio':cost_time_ratio,
        }

        """ 计算消费进度 """

        # 计算季度消费值
        bothconsume=models.Total.objects.values('date').\
            filter(date__range=(quarter_start_day,latest_date)).\
            aggregate(
            all=Sum('allconsume'),
            feed=Sum('feed_allconsume'),
            op=Sum('op_allconsume'),
        )

        # 计算季度任务
        alltask=models.QuarterTask.objects.all()
        allconsume_task=alltask[2].qconsume_task
        feedconsume_task=alltask[1].qconsume_task
        opconsume_task=alltask[0].qconsume_task

        # 计算任务完成率
        all_ratio = '{:.2%}'.format(bothconsume['all'] / allconsume_task)
        feed_ratio = '{:.2%}'.format(bothconsume['feed'] / feedconsume_task)
        op_ratio = '{:.2%}'.format(bothconsume['op'] / opconsume_task)

        # 计算预估完成率
        has_days=quarter_days-cost_days   # 季度剩余天数
        estimate_all = '{:.2%}'.format((allconsume_l7['allconsume'] / 7 * has_days + bothconsume['all']) / allconsume_task)
        estimate_feed = '{:.2%}'.format((feedconsume_l7['feedconsume'] / 7 * has_days + bothconsume['feed']) / feedconsume_task)
        estimate_op = '{:.2%}'.format((opconsume_l7['opconsume'] / 7 * has_days + bothconsume['op']) / opconsume_task)

        estimate_data={
            'allconsume_task':allconsume_task,
            'feedconsume_task': feedconsume_task,
            'opconsume_task': opconsume_task,

            'all_ratio':all_ratio,
            'feed_ratio':feed_ratio,
            'op_ratio':op_ratio,

            'estimate_all': estimate_all,
            'estimate_feed': estimate_feed,
            'estimate_op': estimate_op,
        }

        context={
            'normal_consume':normal_consume,
            'cost_time':cost_time,
            'estimate_data':estimate_data,
        }

        return render(request,'datacenter/more_all.html',context)


# 处理整体数据页
def more_all_chart(request):
    differ=request.POST.get('differ')

    if differ=='range_chart':
        date,consume=[],[]
        begin_date=request.POST.get('begin_date')
        end_date=request.POST.get('end_date')
        range_data=models.Total.objects.filter(date__range=(begin_date,end_date)).values('date').annotate(allconsume=Sum('allconsume')).order_by('date')
        for p in range_data:
            date.append(p['date'])
            consume.append(float(p['allconsume']))
        context={'date':date,'consume':consume}
        return JsonResponse(context)

    elif differ=='single_tab':
        choice_date=request.POST.get('choice_date')
        choice_date=datetime.datetime.strptime(choice_date,'%Y-%m-%d').date()

        if choice_date>models.Account.get_latest_date():
            context={'message':'{d}日数据尚未更新！'.format(d=choice_date)}
            return JsonResponse(context)

        # 前一天日期，做环比
        yesterday = choice_date + datetime.timedelta(days=-1)
        # 前七天日期，做同比
        lastweek = choice_date + datetime.timedelta(days=-7)

        """ 计算当日数据，前日数据，日环比，周同比 """
        # 计算最新日期数据
        bothconsume = models.Total.objects.values('date').\
            filter(date=choice_date).\
            aggregate(
            all=Sum('allconsume'),
            feed=Sum('feed_allconsume'),
            op=Sum('op_allconsume'),
        )

        # 计算前一天数据
        bothconsume_l1 = models.Total.objects.values('date').\
            filter(date=yesterday).\
            aggregate(
            all=Sum('allconsume'),
            feed=Sum('feed_allconsume'),
            op=Sum('op_allconsume'),
        )

        # 计算七天前数据
        bothconsume_l7 = models.Total.objects.values('date').\
            filter(date=lastweek).\
            aggregate(
            all=Sum('allconsume'),
            feed=Sum('feed_allconsume'),
            op=Sum('op_allconsume'),
        )

        # 计算环比
        allconsume_compare_l1 = '{:.2%}'.format(bothconsume['all'] / bothconsume_l1['all'] - 1)
        feedconsume_compare_l1 = '{:.2%}'.format(bothconsume['feed'] / bothconsume_l1['feed'] - 1)
        opconsume_compare_l1 = '{:.2%}'.format(bothconsume['op'] / bothconsume_l1['op'] - 1)

        # 计算同比
        allconsume_compare_l7 = '{:.2%}'.format(bothconsume['all'] / bothconsume_l7['all'] - 1)
        feedconsume_compare_l7 = '{:.2%}'.format(bothconsume['feed'] / bothconsume_l7['feed'] - 1)
        opconsume_compare_l7 = '{:.2%}'.format(bothconsume['op'] / bothconsume_l7['op'] - 1)

        choice_consume={
            'allconsume':round(bothconsume['all']/10000,2),
            'feedconsume':round(bothconsume['feed']/10000,2),
            'opconsume': round(bothconsume['op']/10000,2),

            'allconsume_l1': round(bothconsume_l1['all']/10000,2),
            'feedconsume_l1': round(bothconsume_l1['feed']/10000,2),
            'opconsume_l1': round(bothconsume_l1['op']/10000,2),

            'allconsume_compare_l1':allconsume_compare_l1,
            'feedconsume_compare_l1':feedconsume_compare_l1,
            'opconsume_compare_l1':opconsume_compare_l1,

            'allconsume_compare_l7': allconsume_compare_l7,
            'feedconsume_compare_l7': feedconsume_compare_l7,
            'opconsume_compare_l7': opconsume_compare_l7,
        }

        return JsonResponse(choice_consume)


# 处理信息流数据
def more_feed(request):
    return render(request,'datacenter/more_feed.html')

# 处理品牌数据
def more_op(request):
    return render(request,'datacenter/more_op.html')


# 获取一级行业列表
def get_indus1(request):
    indus1_list=[]
    all_indus1=models.Industry1.objects.values()
    for name in all_indus1:
        indus1_list.append(name['indus1_name'])

    return JsonResponse(indus1_list,safe=False)


# 获取二级行业列表
def get_indus2(request):
    indus1=request.GET.get('indus1')
    indus2_list=[]

    indus1_id=models.Industry1.objects.get(indus1_name=indus1).id
    all_indus2=models.Industry2.objects.filter(indus1_name=indus1_id).values()
    for name in all_indus2:
        indus2_list.append(name['indus2_name'])

    return JsonResponse(indus2_list,safe=False)


# 处理一级行业数据
def industry_1(request):
    return render(request,'datacenter/industry_1.html')

# 一级行业的图表
def indus1_chart(request):
    indus1 = request.POST.get('indus1')
    ctype = request.POST.get('ctype')
    begin_date = request.POST.get('begin_date')
    end_date = request.POST.get('end_date')

    begin_date = datetime.datetime.strptime(begin_date, '%Y.%m.%d').date()
    end_date = datetime.datetime.strptime(end_date, '%Y.%m.%d').date()
    # print(indus1,ctype,begin_date,end_date)

    date_list=[]
    consume_list=[]

    count_list=[]

    sum_name=''
    search_dict={}


    if ctype == 'all':
        search_dict['allconsume__gt']=0
        sum_name= 'allconsume'
    elif ctype == 'fengchao':
        search_dict['fengchao_allconsume__gt']=0
        sum_name = 'fengchao_allconsume'
    elif ctype == 'feed':
        search_dict['feed_allconsume__gt']=0
        sum_name = 'feed_allconsume'
    elif ctype == 'op':
        search_dict['op_allconsume__gt']=0
        sum_name = 'op_allconsume'

    if indus1:

        indus_data=models.Total.objects.values('date').\
            filter(date__range=(begin_date,end_date),account_indus_1=indus1,**search_dict).\
            order_by('date')

        allconsume=indus_data.annotate(consume=Sum(sum_name))
        for data in allconsume:
            date_list.append(data['date'])
            consume_list.append(float(data['consume']))

        allcount=indus_data.annotate(count=Count('id'))
        for data in allcount:
            count_list.append(data['count'])

        context={
            'date_list':date_list,
            'consume_list':consume_list,
            'count_list':count_list,
        }

        return JsonResponse(context)


# 处理二级行业数据
def industry_2(request):
    return render(request,'datacenter/industry_2.html')

def indus2_chart(request):
    indus1 = request.POST.get('indus1')
    indus2 = request.POST.get('indus2')
    ctype = request.POST.get('ctype')
    begin_date = request.POST.get('begin_date')
    end_date = request.POST.get('end_date')

    begin_date = datetime.datetime.strptime(begin_date, '%Y.%m.%d').date()
    end_date = datetime.datetime.strptime(end_date, '%Y.%m.%d').date()
    # print(indus1,indus2,ctype,begin_date,end_date)

    date_list=[]
    consume_list=[]
    count_list=[]

    sum_name=''
    search_dict = {}

    if ctype == 'all':
        sum_name = 'allconsume'
        search_dict['allconsume__gt']=0
    elif ctype == 'fengchao':
        sum_name = 'fengchao_allconsume'
        search_dict['fengchao_allconsume__gt'] = 0
    elif ctype == 'feed':
        sum_name = 'feed_allconsume'
        search_dict['feed_allconsume__gt'] = 0
    elif ctype == 'op':
        sum_name = 'op_allconsume'
        search_dict['op_allconsume__gt'] = 0


    indus_data=models.Total.objects.values('date').\
        filter(
        date__range=(begin_date,end_date),
        account_indus_1=indus1,
        account_indus_2=indus2,
        **search_dict
    ).order_by('date')

    allconsume=indus_data.annotate(consume=Sum(sum_name))
    for data in allconsume:
        date_list.append(data['date'])
        consume_list.append(float(data['consume']))

    allcount=indus_data.annotate(count=Count('id'))
    for data in allcount:
        count_list.append(data['count'])

    context={
        'date_list':date_list,
        'consume_list':consume_list,
        'count_list': count_list,
    }
    return JsonResponse(context)

# 处理失效数据
def invalid(request):
    return render(request,'datacenter/invalid.html')

def get_invalid(request):
    latest_date=models.Invalid.get_latest_date()
    word=request.POST.get('word').strip()
    data_list=[]
    alldata=models.Invalid.objects.filter(Q(username=word) | Q(company_name=word),date=latest_date).\
        values('username','company_name','account_indus_1','account_indus_2','sf_username','depart')

    for data in alldata:
        data_list.append(data)
    context={
        'invalid_data':data_list,
    }
    return JsonResponse(context)


def personal(request):
    # 数据最新日期
    latest_date = models.Account.get_latest_date()
    # 新开最新日期
    new_date = models.Personal.get_latest_date()
    # 七天前的日期
    last_seven_day = latest_date + datetime.timedelta(days=-7)
    # 一天前的日期
    last_one_day = latest_date + datetime.timedelta(days=-1)
    # 计算季度第一天
    quarter_start_day = datetime.date(latest_date.year, latest_date.month - (latest_date.month - 1) % 3, 1)

    username = request.session.get('user_info')['username']
    realname = request.session.get('user_info')['realname']
    # print(username,realname,quarter_start_day,latest_date,new_date)

    alldata=None
    date_filter=(datetime.datetime.strftime(latest_date,"%Y-%m-%d"),datetime.datetime.strftime(last_one_day,"%Y-%m-%d"),datetime.datetime.strftime(last_seven_day,"%Y-%m-%d"))

    if realname == '员工':

        userid = models.Personal.objects.values('userid').filter(date=new_date,frame1=username)
        alluserid=[i['userid'] for i in userid]

        if alluserid:
            sql = ''
            sql_more = ''
            moreinfo = {}

            if len(alluserid) > 1:
                sql = "select p.id,t.username,p.company_name,p.sign_date,p.sf_name,sum(t.allconsume) as consume from datacenter_personal p left join datacenter_total t on p.userid=t.userid " \
                      "where t.date between '{}' and '{}' and t.userid in {} and p.date='{}' group by t.username".format(quarter_start_day,latest_date,tuple(alluserid),new_date)

                sql_more = "select p.id,t.username,t.date,sum(t.allconsume) as s from datacenter_personal p left join datacenter_total t on p.userid=t.userid " \
                           "where t.date in {} and t.userid in {} and p.date='{}' group by t.username,t.date".format(date_filter, tuple(alluserid), new_date)

            elif len(alluserid) == 1:
                sql = "select p.id,t.username,p.company_name,p.sign_date,p.sf_name,sum(t.allconsume) as consume from datacenter_personal p left join datacenter_total t on p.userid=t.userid " \
                      "where t.date between '{}' and '{}' and t.userid ='{}' and p.date='{}' group by t.username".format(quarter_start_day,latest_date,alluserid[0],new_date)

                sql_more = "select p.id,t.username,t.date,sum(t.allconsume) as s from datacenter_personal p left join datacenter_total t on p.userid=t.userid " \
                           "where t.date in {} and t.userid = '{}' and p.date='{}' group by t.username,t.date".format(date_filter, alluserid[0], new_date)

            alldata = models.Personal.objects.raw(sql)
            more_data = models.Personal.objects.raw(sql_more)

            for i in more_data:

                if not i.username in moreinfo.keys():
                    moreinfo[i.username] = [0, 0, 0]

                if i.date == latest_date:
                    moreinfo[i.username][0] = i.s

                if i.date == last_one_day:
                    moreinfo[i.username][1] = i.s

                if i.date == last_seven_day:
                    moreinfo[i.username][2] = i.s

            for a in alldata:
                if a.username in moreinfo.keys():
                    a.p1 = moreinfo[a.username][0]
                    a.p2 = moreinfo[a.username][0] - moreinfo[a.username][1]
                    a.p3 = moreinfo[a.username][0] - moreinfo[a.username][2]
                else:
                    a.p1 = 0
                    a.p2 = 0
                    a.p3 = 0


    if realname == '主管':
        userid = models.Personal.objects.values('userid').filter(date=new_date, frame2=username)
        alluserid=[i['userid'] for i in userid]

        if alluserid:
            sql = ''
            sql_more = ''
            moreinfo = {}

            if len(alluserid) > 1:
                sql = "select p.id,p.frame1,sum(t.allconsume) as consume from datacenter_personal p left join datacenter_total t on p.userid=t.userid " \
                      "where t.date between '{}' and '{}' and t.userid in {} and p.date='{}' group by p.frame1".format(quarter_start_day,latest_date,tuple(alluserid),new_date)

                sql_more = "select p.id,p.frame1,t.date,sum(t.allconsume) as s from datacenter_personal p left join datacenter_total t on p.userid=t.userid " \
                           "where t.date in {} and t.userid in {} and p.date='{}' group by p.frame1,t.date".format(date_filter, tuple(alluserid), new_date)

            elif len(alluserid) == 1:
                sql = "select p.id,p.frame1,sum(t.allconsume) as consume from datacenter_personal p left join datacenter_total t on p.userid=t.userid " \
                      "where t.date between '{}' and '{}' and t.userid ='{}' and p.date='{}' group by p.frame1".format(quarter_start_day,latest_date,alluserid[0],new_date)

                sql_more = "select p.id,p.frame1,t.date,sum(t.allconsume) as s from datacenter_personal p left join datacenter_total t on p.userid=t.userid " \
                           "where t.date in {} and t.userid = '{}' and p.date='{}' group by p.frame1,t.date".format(date_filter, alluserid[0], new_date)

            alldata = models.Personal.objects.raw(sql)
            more_data = models.Personal.objects.raw(sql_more)

            for i in more_data:

                if not i.frame1 in moreinfo.keys():
                    moreinfo[i.frame1] = [0, 0, 0]

                if i.date == latest_date:
                    moreinfo[i.frame1][0] = i.s

                if i.date == last_one_day:
                    moreinfo[i.frame1][1] = i.s

                if i.date == last_seven_day:
                    moreinfo[i.frame1][2] = i.s

            for a in alldata:
                if a.frame1 in moreinfo.keys():
                    a.p1 = moreinfo[a.frame1][0]
                    a.p2 = moreinfo[a.frame1][0] - moreinfo[a.frame1][1]
                    a.p3 = moreinfo[a.frame1][0] - moreinfo[a.frame1][2]
                else:
                    a.p1 = 0
                    a.p2 = 0
                    a.p3 = 0


    if realname == '经理':
        userid = models.Personal.objects.values('userid').filter(date=new_date, frame3=username)
        alluserid=[i['userid'] for i in userid]

        if alluserid:
            sql = ''
            sql_more = ''
            moreinfo = {}

            if len(alluserid) >1:
                sql = "select p.id,p.frame1,sum(t.allconsume) as consume from datacenter_personal p left join datacenter_total t on p.userid=t.userid " \
                      "where t.date between '{}' and '{}' and t.userid in {} and p.date='{}' group by p.frame1".format(quarter_start_day,latest_date,tuple(alluserid),new_date)

                sql_more = "select p.id,p.frame1,t.date,sum(t.allconsume) as s from datacenter_personal p left join datacenter_total t on p.userid=t.userid " \
                           "where t.date in {} and t.userid in {} and p.date='{}' group by p.frame1,t.date".format(date_filter, tuple(alluserid), new_date)

            elif len(alluserid) == 1:
                sql = "select p.id,p.frame1,sum(t.allconsume) as consume from datacenter_personal p left join datacenter_total t on p.userid=t.userid " \
                      "where t.date between '{}' and '{}' and t.userid ='{}' and p.date='{}' group by p.frame1".format(quarter_start_day,latest_date,alluserid[0],new_date)

                sql_more = "select p.id,p.frame1,t.date,sum(t.allconsume) as s from datacenter_personal p left join datacenter_total t on p.userid=t.userid " \
                           "where t.date in {} and t.userid = '{}' and p.date='{}' group by p.frame1,t.date".format(date_filter, alluserid[0], new_date)

            alldata = models.Personal.objects.raw(sql)
            more_data = models.Personal.objects.raw(sql_more)

            for i in more_data:

                if not i.frame1 in moreinfo.keys():
                    moreinfo[i.frame1] = [0, 0, 0]

                if i.date == latest_date:
                    moreinfo[i.frame1][0] = i.s

                if i.date == last_one_day:
                    moreinfo[i.frame1][1] = i.s

                if i.date == last_seven_day:
                    moreinfo[i.frame1][2] = i.s

            for a in alldata:
                if a.frame1 in moreinfo.keys():
                    a.p1 = moreinfo[a.frame1][0]
                    a.p2 = moreinfo[a.frame1][0] - moreinfo[a.frame1][1]
                    a.p3 = moreinfo[a.frame1][0] - moreinfo[a.frame1][2]
                else:
                    a.p1 = 0
                    a.p2 = 0
                    a.p3 = 0


    if realname == '总监':
        userid = models.Personal.objects.values('userid').filter(date=new_date, frame4=username)
        alluserid=[i['userid'] for i in userid]

        if alluserid:
            sql = ''
            sql_more = ''
            moreinfo = {}

            if len(alluserid) > 1:
                sql = "select p.id,p.frame1,p.depart,sum(t.allconsume) as consume from datacenter_personal p left join datacenter_total t on p.userid=t.userid " \
                      "where t.date between '{}' and '{}' and t.userid in {} and p.date='{}' group by p.frame1".format(quarter_start_day,latest_date,tuple(alluserid),new_date)

                sql_more = "select p.id,p.frame1,t.date,sum(t.allconsume) as s from datacenter_personal p left join datacenter_total t on p.userid=t.userid " \
                           "where t.date in {} and t.userid in {} and p.date='{}' group by p.frame1,t.date".format(date_filter, tuple(alluserid), new_date)

            elif len(alluserid) == 1:
                sql = "select p.id,p.frame1,p.depart,sum(t.allconsume) as consume from datacenter_personal p left join datacenter_total t on p.userid=t.userid " \
                      "where t.date between '{}' and '{}' and t.userid ='{}' and p.date='{}' group by p.frame1".format(quarter_start_day,latest_date,alluserid[0],new_date)

                sql_more = "select p.id,p.frame1,t.date,sum(t.allconsume) as s from datacenter_personal p left join datacenter_total t on p.userid=t.userid " \
                           "where t.date in {} and t.userid = '{}' and p.date='{}' group by p.frame1,t.date".format(date_filter, alluserid[0], new_date)

            alldata = models.Personal.objects.raw(sql)
            more_data = models.Personal.objects.raw(sql_more)

            for i in more_data:

                if not i.frame1 in moreinfo.keys():
                    moreinfo[i.frame1] = [0, 0, 0]

                if i.date == latest_date:
                    moreinfo[i.frame1][0] = i.s

                if i.date == last_one_day:
                    moreinfo[i.frame1][1] = i.s

                if i.date == last_seven_day:
                    moreinfo[i.frame1][2] = i.s

            for a in alldata:
                if a.frame1 in moreinfo.keys():
                    a.p1 = moreinfo[a.frame1][0]
                    a.p2 = moreinfo[a.frame1][0] - moreinfo[a.frame1][1]
                    a.p3 = moreinfo[a.frame1][0] - moreinfo[a.frame1][2]
                else:
                    a.p1 = 0
                    a.p2 = 0
                    a.p3 = 0


    if realname == 'LKA':

        edu = "教育行业拓展部"
        userid = models.Personal.objects.values('userid').filter(date=new_date).exclude(depart=edu)
        alluserid=[i['userid'] for i in userid]

        if alluserid:
            sql = ''
            sql_more = ''
            moreinfo={}

            if len(alluserid) > 1:
                sql = "select p.id,p.frame1,p.depart,sum(t.allconsume) as consume from datacenter_personal p left join datacenter_total t on p.userid=t.userid " \
                      "where t.date between '{}' and '{}' and t.userid in {} and p.date='{}' and p.depart !='{}' group by p.frame1".format(quarter_start_day,latest_date,tuple(alluserid),new_date,edu)

                sql_more = "select p.id,p.frame1,t.date,sum(t.allconsume) as s from datacenter_personal p left join datacenter_total t on p.userid=t.userid " \
                           "where t.date in {} and t.userid in {} and p.date='{}' and p.depart !='{}' group by p.frame1,t.date".format(date_filter, tuple(alluserid), new_date, edu)

            elif len(alluserid) == 1:
                sql = "select p.id,p.frame1,p.depart,sum(t.allconsume) as consume from datacenter_personal p left join datacenter_total t on p.userid=t.userid " \
                      "where t.date between '{}' and '{}' and t.userid ='{}' and p.date='{}' and p.depart !='{}' group by p.frame1".format(quarter_start_day,latest_date,alluserid[0],new_date,edu)

                sql_more = "select p.id,p.frame1,t.date,sum(t.allconsume) as s from datacenter_personal p left join datacenter_total t on p.userid=t.userid " \
                           "where t.date in {} and t.userid = '{}' and p.date='{}' and p.depart !='{}' group by p.frame1,t.date".format(date_filter, alluserid[0], new_date,edu)

            alldata = models.Personal.objects.raw(sql)
            more_data = models.Personal.objects.raw(sql_more)

            for i in more_data:

                if not i.frame1 in moreinfo.keys():
                    moreinfo[i.frame1] = [0, 0, 0]

                if i.date == latest_date:
                    moreinfo[i.frame1][0] = i.s

                if i.date == last_one_day:
                    moreinfo[i.frame1][1] = i.s

                if i.date == last_seven_day:
                    moreinfo[i.frame1][2] = i.s

            for a in alldata:
                if a.frame1 in moreinfo.keys():
                    a.p1 = moreinfo[a.frame1][0]
                    a.p2 = moreinfo[a.frame1][0] - moreinfo[a.frame1][1]
                    a.p3 = moreinfo[a.frame1][0] - moreinfo[a.frame1][2]
                else:
                    a.p1 = 0
                    a.p2 = 0
                    a.p3 = 0


    if realname == 'all':
        # --- type1 ---
        # userid = models.Personal.objects.values('userid').filter(date=new_date)
        # alluserid=[i['userid'] for i in userid]
        #
        # if alluserid:
        #     sql = ''
        #     if len(alluserid) > 1:
        #         sql = "select p.id,p.frame1,case when sum(t.sa) is null then 0 else sum(t.sa) end consume from (select id,userid,frame1 from datacenter_personal where date='{}') p " \
        #               "left join (select userid,sum(allconsume) sa from datacenter_total where date between '{}' and '{}' and userid in {} group by userid) t " \
        #               "on p.userid = t.userid group by p.frame1".format(new_date,quarter_start_day,latest_date,tuple(alluserid))
        #     elif len(alluserid) == 1:
        #         sql = "select p.id,p.frame1,case when sum(t.sa) is null then 0 else sum(t.sa) end consume from (select id,userid,frame1 from datacenter_personal where date='{}') p " \
        #               "left join (select userid,sum(allconsume) sa from datacenter_total where date between '{}' and '{}' and userid ='{}' group by userid) t " \
        #               "on p.userid = t.userid group by p.frame1".format(new_date,quarter_start_day,latest_date,alluserid[0])
        #     alldata = models.Personal.objects.raw(sql)
        # --- end type1 ---

        userid = models.Personal.objects.values('userid').filter(date=new_date)
        alluserid=[i['userid'] for i in userid]

        if alluserid:
            sql = ''
            sql_more = ''
            moreinfo={}

            if len(alluserid) > 1:
                sql = "select p.id,p.frame1,p.depart,sum(t.allconsume) as consume from datacenter_personal p left join datacenter_total t on p.userid=t.userid " \
                      "where t.date between '{}' and '{}' and t.userid in {} and p.date='{}' group by p.frame1".format(quarter_start_day,latest_date,tuple(alluserid),new_date)

                sql_more = "select p.id,p.frame1,t.date,sum(t.allconsume) as s from datacenter_personal p left join datacenter_total t on p.userid=t.userid " \
                           "where t.date in {} and t.userid in {} and p.date='{}' group by p.frame1,t.date".format(date_filter, tuple(alluserid), new_date)

            elif len(alluserid) == 1:
                sql = "select p.id,p.frame1,p.depart,sum(t.allconsume) as consume from datacenter_personal p left join datacenter_total t on p.userid=t.userid " \
                      "where t.date between '{}' and '{}' and t.userid ='{}' and p.date='{}' group by p.frame1".format(quarter_start_day,latest_date,alluserid[0],new_date)

                sql_more = "select p.id,p.frame1,t.date,sum(t.allconsume) as s from datacenter_personal p left join datacenter_total t on p.userid=t.userid " \
                           "where t.date in {} and t.userid = '{}' and p.date='{}' group by p.frame1,t.date".format(date_filter, alluserid[0], new_date)

            alldata = models.Personal.objects.raw(sql)
            more_data = models.Personal.objects.raw(sql_more)

            for i in more_data:

                if not i.frame1 in moreinfo.keys():
                    moreinfo[i.frame1] = [0, 0, 0]

                if i.date == latest_date:
                    moreinfo[i.frame1][0] = i.s

                if i.date == last_one_day:
                    moreinfo[i.frame1][1] = i.s

                if i.date == last_seven_day:
                    moreinfo[i.frame1][2] = i.s

            for a in alldata:
                if a.frame1 in moreinfo.keys():
                    a.p1 = moreinfo[a.frame1][0]
                    a.p2 = moreinfo[a.frame1][0] - moreinfo[a.frame1][1]
                    a.p3 = moreinfo[a.frame1][0] - moreinfo[a.frame1][2]
                else:
                    a.p1 = 0
                    a.p2 = 0
                    a.p3 = 0


        """  sss """

        # moreinfo = {}
        #
        # sql_more = "select p.id,p.frame1,t.date,sum(t.allconsume) as s from datacenter_personal p left join datacenter_total t on p.userid=t.userid " \
        #       "where t.date in {} and t.userid in {} and p.date='{}' group by p.frame1,t.date".format(date_filter,tuple(alluserid), new_date)
        # data = models.Personal.objects.raw(sql_more)
        # for i in data:
        #
        #     if not i.frame1 in moreinfo.keys():
        #         moreinfo[i.frame1] = [0, 0, 0]
        #
        #     if i.date == latest_date:
        #         moreinfo[i.frame1][0] = i.s
        #
        #     if i.date == last_one_day:
        #         moreinfo[i.frame1][1] = i.s
        #
        #     if i.date == last_seven_day:
        #         moreinfo[i.frame1][2] = i.s
        #
        # for a in alldata:
        #     if a.frame1 in moreinfo.keys():
        #         a.p1 = moreinfo[a.frame1][0]
        #         a.p2 = moreinfo[a.frame1][0] - moreinfo[a.frame1][1]
        #         a.p3 = moreinfo[a.frame1][0] - moreinfo[a.frame1][2]
        #     else:
        #         a.p1 = 0
        #         a.p2 = 0
        #         a.p3 = 0

        """  end """


    context={
        'latest_date':latest_date,
        'alldata':alldata
    }
    return render(request, 'datacenter/personal.html',context)

# django 合并查询集

def personal_detail(request):
    # 数据最新日期
    latest_date = models.Account.get_latest_date()
    # 新开最新日期
    new_date = models.Personal.get_latest_date()
    # 七天前的日期
    last_seven_day = latest_date + datetime.timedelta(days=-7)
    # 一天前的日期
    last_one_day = latest_date + datetime.timedelta(days=-1)
    # 计算季度第一天
    quarter_start_day = datetime.date(latest_date.year, latest_date.month - (latest_date.month - 1) % 3, 1)
    name = request.POST.get('n')


    userid = models.Personal.objects.values('userid').filter(date=new_date, frame1=name)
    alluserid = [i['userid'] for i in userid]
    sql = ''
    if len(alluserid) > 1:
        sql = "select p.id,p.userid,t.username,p.company_name,p.sign_date,p.sf_name,sum(t.allconsume) as consume from datacenter_personal p left join datacenter_total t on p.userid=t.userid " \
              "where t.date between '{}' and '{}' and t.userid in {} and p.date='{}' group by t.username order by consume desc".format(quarter_start_day,latest_date,tuple(alluserid),new_date)

    elif len(alluserid) == 1:
        sql = "select p.id,p.userid,t.username,p.company_name,p.sign_date,p.sf_name,sum(t.allconsume) as consume from datacenter_personal p left join datacenter_total t on p.userid=t.userid " \
              "where t.date between '{}' and '{}' and t.userid= '{}' and p.date='{}' group by t.username".format(quarter_start_day,latest_date,alluserid[0],new_date)


    # --- type1 ---
    # if len(alluserid) > 1:
    #
    #     sql = "select p.id,t.userid,t.username,p.company_name,p.sign_date,p.sf_name,case when sum(t.sa) is null then 0 else sum(t.sa) end consume from" \
    #           " (select id,userid,company_name,sign_date,sf_name from datacenter_personal where date='{}' and frame1='{}') p " \
    #           "left join (select userid,username,sum(allconsume) sa from datacenter_total where date between '{}' and '{}' and userid in {} group by userid,username) t " \
    #           "on p.userid = t.userid group by t.username order by consume desc".format(new_date,name,quarter_start_day,latest_date,tuple(alluserid))
    #
    # elif len(alluserid) == 1:
    #     sql = "select p.id,t.userid,t.username,p.company_name,p.sign_date,p.sf_name,case when sum(t.sa) is null then 0 else sum(t.sa) end consume from" \
    #           " (select id,userid,company_name,sign_date,sf_name from datacenter_personal where date='{}' and frame1='{}') p " \
    #           "left join (select userid,username,sum(allconsume) sa from datacenter_total where date between '{}' and '{}' and userid ='{}' group by userid,username) t " \
    #           "on p.userid = t.userid group by t.username order by consume desc".format(new_date, name,quarter_start_day, latest_date,alluserid[0])
    # --- end type1 ---

    alldata = models.Personal.objects.raw(sql)

    """ select 2 """

    # moreinfo={}
    # for u in alluserid:
    #     data = models.Total.objects.filter(userid=u, date__in=(latest_date, last_one_day, last_seven_day)).values('date').annotate(s=Sum('allconsume'))
    #
    #     data_dict = {}
    #     for i in data:
    #         data_dict[i['date']] = i['s']
    #
    #     p = []
    #     if latest_date in data_dict.keys():
    #         p.insert(0, data_dict[latest_date])
    #     else:
    #         p.insert(0, 0)
    #
    #     if last_one_day in data_dict.keys():
    #         p.insert(1, p[0] - data_dict[last_one_day])
    #     else:
    #         p.insert(1, p[0])
    #
    #     if last_seven_day in data_dict.keys():
    #         p.insert(2, p[0] - data_dict[last_seven_day])
    #     else:
    #         p.insert(2, p[0])
    #
    #     moreinfo[u]=p

    """  select 3  """
    moreinfo = {}

    data = models.Total.objects.filter(userid__in=userid, date__in=(latest_date, last_one_day, last_seven_day)).values('userid','date','allconsume')
    for i in data:

        if not i['userid'] in moreinfo.keys():
            moreinfo[i['userid']]=[0,0,0]

        if i['date'] == latest_date:
            moreinfo[i['userid']][0]=i['allconsume']

        if i['date'] == last_one_day:
            moreinfo[i['userid']][1]=i['allconsume']

        if i['date'] == last_seven_day:
            moreinfo[i['userid']][2]=i['allconsume']

    context=[]
    for data in alldata:
        d={}
        d['username']=data.username
        d['company_name']=data.company_name
        d['sign_date']=data.sign_date
        d['sf_name']=data.sf_name
        d['consume']=data.consume
        if data.userid in moreinfo.keys():
            d['p1'] = moreinfo[data.userid][0]
            d['p2'] = moreinfo[data.userid][0] - moreinfo[data.userid][1]
            d['p3'] = moreinfo[data.userid][0] - moreinfo[data.userid][2]
        else:
            d['p1'] = 0
            d['p2'] = 0
            d['p3'] = 0


        context.append(d)

    return JsonResponse(context,safe=False)


def personal_chart(request):
    # 数据最新日期
    latest_date = models.Account.get_latest_date()
    # 七天前的日期
    last_seven_day=latest_date+datetime.timedelta(days=-6)

    name = request.POST.get('name')

    # print(latest_date, last_seven_day , name)

    sql = "select id,date,allconsume from datacenter_total where date between '{}' and '{}' and username='{}'".format(last_seven_day,latest_date,name)
    alldata = models.Total.objects.raw(sql)


    data_dict={}
    alldata_dict={}

    for i in alldata:
        data_dict[i.date]=i.allconsume
        # print(i.date,i.allconsume)

    for d in range(7):
        c_date=last_seven_day+datetime.timedelta(days=d)
        if c_date in data_dict.keys():
            alldata_dict[datetime.datetime.strftime(c_date,"%Y-%m-%d")] = float(data_dict[c_date])
        else:
            alldata_dict[datetime.datetime.strftime(c_date,"%Y-%m-%d")] = 0

    context={
        'keys':list(alldata_dict.keys()),
        'values':list(alldata_dict.values()),
    }

    return JsonResponse(context)