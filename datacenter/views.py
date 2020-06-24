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
    allconsume_list=[]
    ratio_list=[]
    sum_name=''

    if ctype == 'all':
        sum_name = 'allconsume'
    elif ctype == 'fengchao':
        sum_name = 'fengchao_allconsume'
    elif ctype == 'feed':
        sum_name = 'feed_allconsume'
    elif ctype == 'op':
        sum_name = 'op_allconsume'

    if indus1=='all':
        alldata=models.Total.objects.values('date').\
            filter(date__range=(begin_date,end_date)).\
            annotate(consume=Sum(sum_name)).\
            order_by('date')
        for data in alldata:
            date_list.append(data['date'])
            consume_list.append(float(data['consume']))
            ratio_list.append(100)

        context={
            'date_list':date_list,
            'consume_list':consume_list,
            'ratio_list':ratio_list,
        }

        return JsonResponse(context)

    else:
        indus_data=models.Total.objects.values('date').\
            filter(date__range=(begin_date,end_date),account_indus_1=indus1).\
            annotate(consume=Sum(sum_name)).\
            order_by('date')

        for indus in indus_data:
            date_list.append(indus['date'])
            consume_list.append(float(indus['consume']))


        all_data=models.Total.objects.values('date').\
            filter(date__range=(begin_date,end_date)).\
            annotate(allconsume=Sum(sum_name)).\
            order_by('date')

        for all in all_data:
            allconsume_list.append(float(all['allconsume']))


        for i in range(len(consume_list)):
            ratio=consume_list[i] / allconsume_list[i] * 100
            ratio_list.append(round(ratio,2))

        context={
            'date_list':date_list,
            'consume_list':consume_list,
            'ratio_list':ratio_list,
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
    allconsume_list=[]
    ratio_list=[]
    sum_name=''

    if ctype == 'all':
        sum_name = 'allconsume'
    elif ctype == 'fengchao':
        sum_name = 'fengchao_allconsume'
    elif ctype == 'feed':
        sum_name = 'feed_allconsume'
    elif ctype == 'op':
        sum_name = 'op_allconsume'

    allindus2=models.Total.objects.values('date').\
        filter(
        date__range=(begin_date,end_date),
        account_indus_1=indus1,
        account_indus_2=indus2,
    ).annotate(consume=Sum(sum_name)).order_by('date')

    for data2 in allindus2:
        date_list.append(data2['date'])
        consume_list.append(float(data2['consume']))

    allindus1=models.Total.objects.values('date').\
        filter(date__range=(begin_date,end_date),account_indus_1=indus1).\
        annotate(consume=Sum(sum_name)).order_by('date')

    for data1 in allindus1:
        allconsume_list.append(float(data1['consume']))

    for i in range(len(consume_list)):
        ratio = consume_list[i] / allconsume_list[i] * 100
        ratio_list.append(round(ratio, 2))

    context={
        'date_list':date_list,
        'consume_list':consume_list,
        'ratio_list': ratio_list,
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