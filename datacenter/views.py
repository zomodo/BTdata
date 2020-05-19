from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import datetime
import calendar
from datacenter import models

from django.db.models import Sum,Count,Avg
# Create your views here.


# 总消费
def allconsume(request):
    # 数据最新日期
    latest_date=models.Account.get_latest_date()
    # 前一天日期，做环比
    yesterday=latest_date+datetime.timedelta(days=-1)
    # 前七天日期，做同比
    lastweek=latest_date+datetime.timedelta(days=-7)


    # 计算最新日期数据
    bothconsume=models.Total.objects.filter(date=latest_date).aggregate(allconsume=Sum('allconsume'),searchconsume=Sum('searchconsume'))
    feedconsume=models.Feed.objects.filter(date=latest_date).aggregate(feedconsume=Sum('feed_allconsume'))
    opconsume=models.OtherPro.objects.filter(date=latest_date).aggregate(opconsume=Sum('op_allconsume'))

    # 计算前一天数据
    bothconsume_l1=models.Total.objects.filter(date=yesterday).aggregate(allconsume=Sum('allconsume'),searchconsume=Sum('searchconsume'))
    feedconsume_l1=models.Feed.objects.filter(date=yesterday).aggregate(feedconsume=Sum('feed_allconsume'))
    opconsume_l1=models.OtherPro.objects.filter(date=yesterday).aggregate(opconsume=Sum('op_allconsume'))

    # 计算前七天数据
    bothconsume_l7=models.Total.objects.filter(date=lastweek).aggregate(allconsume=Sum('allconsume'),searchconsume=Sum('searchconsume'))
    feedconsume_l7=models.Feed.objects.filter(date=lastweek).aggregate(feedconsume=Sum('feed_allconsume'))
    opconsume_l7=models.OtherPro.objects.filter(date=lastweek).aggregate(opconsume=Sum('op_allconsume'))

    # 计算环比
    allconsume_compare_l1='{:.2%}'.format(bothconsume['allconsume'] / bothconsume_l1['allconsume'] -1)
    searchconsume_compare_l1='{:.2%}'.format(bothconsume['searchconsume'] / bothconsume_l1['searchconsume'] -1)
    feedconsume_compare_l1='{:.2%}'.format(feedconsume['feedconsume'] / feedconsume_l1['feedconsume'] -1)
    opconsume_compare_l1='{:.2%}'.format(opconsume['opconsume'] / opconsume_l1['opconsume'] -1)

    # 计算同比
    allconsume_compare_l7='{:.2%}'.format(bothconsume['allconsume'] / bothconsume_l7['allconsume'] -1)
    searchconsume_compare_l7='{:.2%}'.format(bothconsume['searchconsume'] / bothconsume_l7['searchconsume'] -1)
    feedconsume_compare_l7='{:.2%}'.format(feedconsume['feedconsume'] / feedconsume_l7['feedconsume'] -1)
    opconsume_compare_l7='{:.2%}'.format(opconsume['opconsume'] / opconsume_l7['opconsume'] -1)

    today_consume={
        'date':latest_date,
        'allconsume':bothconsume['allconsume'],
        'searchconsume':bothconsume['searchconsume'],
        'feedconsume':feedconsume['feedconsume'],
        'opconsume':opconsume['opconsume']
    }
    compare_l1={
        'allconsume_compare_l1':allconsume_compare_l1,
        'searchconsume_compare_l1':searchconsume_compare_l1,
        'feedconsume_compare_l1':feedconsume_compare_l1,
        'opconsume_compare_l1':opconsume_compare_l1,
    }

    compare_l7={
        'allconsume_compare_l7': allconsume_compare_l7,
        'searchconsume_compare_l7': searchconsume_compare_l7,
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
    # 前30天日期，做曲线图
    last30_date=latest_date+datetime.timedelta(days=-13)

    date_list = []
    allconsume_list = []
    searchconsume_list = []
    feedconsume_list = []
    opconsume_list = []

    # 计算总消费和搜索消费
    sql1="select date,sum(allconsume),sum(searchconsume) from datacenter_total where date between '{begin}' and '{end}' group by date".format(begin=last30_date,end=latest_date)
    bothconsume_last30=models.Total.objects.raw(sql1)
    for data in bothconsume_last30.query:
        date_list.append(data[0])
        allconsume_list.append(round(data[1],2))
        searchconsume_list.append(round(data[2],2))

    # 计算信息流消费
    sql2="select date,sum(feed_allconsume) from datacenter_feed where date between '{begin}' and '{end}' group by date".format(begin=last30_date, end=latest_date)
    feedconsume_last30 = models.Feed.objects.raw(sql2)
    for data in feedconsume_last30.query:
        feedconsume_list.append(round(data[1],2))

    # 计算品牌消费
    sql3="select date,sum(op_allconsume) from datacenter_otherpro where date between '{begin}' and '{end}' group by date".format(begin=last30_date, end=latest_date)
    opconsume_last30 = models.Feed.objects.raw(sql3)
    for data in opconsume_last30.query:
        opconsume_list.append(round(data[1],2))

    # print('1:',date_list,allconsume_list,searchconsume_list,feedconsume_list,opconsume_list)
    context={
        'date':date_list,
        'allconsume':allconsume_list,
        'searchconsume':searchconsume_list,
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
    allcount=models.Total.objects.filter(date=latest_date,allconsume__gt=0).aggregate(allcount=Count('allconsume'))
    searchcount=models.Total.objects.filter(date=latest_date,searchconsume__gt=0).aggregate(searchcount=Count('searchconsume'))
    feedcount=models.Feed.objects.filter(date=latest_date,feed_allconsume__gt=0).aggregate(feedcount=Count('feed_allconsume'))
    opcount=models.OtherPro.objects.filter(date=latest_date,op_allconsume__gt=0).aggregate(opcount=Count('op_allconsume'))

    # 计算前一天数据
    allcount_l1=models.Total.objects.filter(date=yesterday,allconsume__gt=0).aggregate(allcount=Count('allconsume'))
    searchcount_l1=models.Total.objects.filter(date=yesterday,searchconsume__gt=0).aggregate(searchcount=Count('searchconsume'))
    feedcount_l1=models.Feed.objects.filter(date=yesterday,feed_allconsume__gt=0).aggregate(feedcount=Count('feed_allconsume'))
    opcount_l1=models.OtherPro.objects.filter(date=yesterday,op_allconsume__gt=0).aggregate(opcount=Count('op_allconsume'))

    # 计算前七天数据
    allcount_l7=models.Total.objects.filter(date=lastweek,allconsume__gt=0).aggregate(allcount=Count('allconsume'))
    searchcount_l7=models.Total.objects.filter(date=lastweek,searchconsume__gt=0).aggregate(searchcount=Count('searchconsume'))
    feedcount_l7=models.Feed.objects.filter(date=lastweek,feed_allconsume__gt=0).aggregate(feedcount=Count('feed_allconsume'))
    opcount_l7=models.OtherPro.objects.filter(date=lastweek,op_allconsume__gt=0).aggregate(opcount=Count('op_allconsume'))

    # 计算环比
    allcount_compare_l1='{:.2%}'.format(allcount['allcount'] / allcount_l1['allcount'] -1)
    searchcount_compare_l1='{:.2%}'.format(searchcount['searchcount'] / searchcount_l1['searchcount'] -1)
    feedcount_compare_l1='{:.2%}'.format(feedcount['feedcount'] / feedcount_l1['feedcount'] -1)
    opcount_compare_l1='{:.2%}'.format(opcount['opcount'] / opcount_l1['opcount'] -1)

    # 计算同比
    allcount_compare_l7='{:.2%}'.format(allcount['allcount'] / allcount_l7['allcount'] -1)
    searchcount_compare_l7='{:.2%}'.format(searchcount['searchcount'] / searchcount_l7['searchcount'] -1)
    feedcount_compare_l7='{:.2%}'.format(feedcount['feedcount'] / feedcount_l7['feedcount'] -1)
    opcount_compare_l7='{:.2%}'.format(opcount['opcount'] / opcount_l7['opcount'] -1)

    today_count={
        'date':latest_date,
        'allcount':allcount['allcount'],
        'searchcount':searchcount['searchcount'],
        'feedcount':feedcount['feedcount'],
        'opcount':opcount['opcount']
    }
    compare_l1={
        'allcount_compare_l1':allcount_compare_l1,
        'searchcount_compare_l1':searchcount_compare_l1,
        'feedcount_compare_l1':feedcount_compare_l1,
        'opcount_compare_l1':opcount_compare_l1,
    }

    compare_l7={
        'allcount_compare_l7': allcount_compare_l7,
        'searchcount_compare_l7': searchcount_compare_l7,
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
    # 前30天日期，做曲线图
    last30_date=latest_date+datetime.timedelta(days=-13)

    date_list = []
    allcount_list = []
    searchcount_list = []
    feedcount_list = []
    opcount_list = []

    # 计算总有消费账户数
    sql1="select date,count(allconsume) from datacenter_total where allconsume>0 and date between '{begin}' and '{end}' group by date".format(begin=last30_date,end=latest_date)
    allcount_last30=models.Total.objects.raw(sql1)
    for data in allcount_last30.query:
        date_list.append(data[0])
        allcount_list.append(round(data[1],2))

    # 计算搜索有消费账户数
    sql2="select date,count(searchconsume) from datacenter_total where searchconsume>0 and date between '{begin}' and '{end}' group by date".format(begin=last30_date,end=latest_date)
    searchcount_last30=models.Total.objects.raw(sql2)
    for data in searchcount_last30.query:
        searchcount_list.append(round(data[1],2))

    # 计算信息流有消费账户数
    sql3="select date,count(feed_allconsume) from datacenter_feed where feed_allconsume>0 and date between '{begin}' and '{end}' group by date".format(begin=last30_date, end=latest_date)
    feedcount_last30 = models.Feed.objects.raw(sql3)
    for data in feedcount_last30.query:
        feedcount_list.append(round(data[1],2))

    # 计算品牌有消费账户数
    sql4="select date,count(op_allconsume) from datacenter_otherpro where op_allconsume>0 and date between '{begin}' and '{end}' group by date".format(begin=last30_date, end=latest_date)
    opcount_last30 = models.Feed.objects.raw(sql4)
    for data in opcount_last30.query:
        opcount_list.append(round(data[1],2))

    context={
        'date':date_list,
        'allcount':allcount_list,
        'searchcount':searchcount_list,
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

            'allconsume_compare_l1':allconsume_compare_l1,
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
        quarter_allconsume = None
        quarter_feedconsume = None
        quarter_opconsume = None

        # 计算总消费和搜索消费
        sql1 = "select sum(allconsume) from datacenter_total where date between '{begin}' and '{end}'".format(begin=quarter_start_day,end=latest_date)
        allconsume_quarter = models.Total.objects.raw(sql1)
        for data in allconsume_quarter.query:
            quarter_allconsume=data[0]

        # 计算信息流消费
        sql2 = "select sum(feed_allconsume) from datacenter_feed where date between '{begin}' and '{end}'".format(begin=quarter_start_day,end=latest_date)
        feedconsume_quarter = models.Feed.objects.raw(sql2)
        for data in feedconsume_quarter.query:
            quarter_feedconsume=data[0]

        # 计算品牌消费
        sql3 = "select sum(op_allconsume) from datacenter_otherpro where date between '{begin}' and '{end}' group by date".format(begin=quarter_start_day,end=latest_date)
        opconsume_quarter = models.Feed.objects.raw(sql3)
        for data in opconsume_quarter.query:
            quarter_opconsume=data[0]

        # 计算季度任务
        alltask=models.QuarterTask.objects.all()
        allconsume_task=alltask[2].qconsume_task
        feedconsume_task=alltask[1].qconsume_task
        opconsume_task=alltask[0].qconsume_task

        # 计算任务完成率
        all_ratio = '{:.2%}'.format(quarter_allconsume / float(allconsume_task))
        feed_ratio = '{:.2%}'.format(quarter_feedconsume / float(feedconsume_task))
        op_ratio = '{:.2%}'.format(quarter_opconsume / float(opconsume_task))

        # 计算预估完成率
        has_days=quarter_days-cost_days   # 季度剩余天数
        estimate_all = '{:.2%}'.format((float(allconsume_l7['allconsume'] / 7 * has_days) + quarter_allconsume) / float(allconsume_task))
        estimate_feed = '{:.2%}'.format((float(feedconsume_l7['feedconsume'] / 7 * has_days) + quarter_feedconsume) / float(feedconsume_task))
        estimate_op = '{:.2%}'.format((float(opconsume_l7['opconsume'] / 7 * has_days) + quarter_opconsume) / float(opconsume_task))

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

def more_all_chart(request):
    differ=request.POST.get('differ')
    if differ=='range_chart':
        date,consume=[],[]
        begin_date=request.POST.get('begin_date')
        end_date=request.POST.get('end_date')
        range_data=models.Total.objects.filter(date__gte=begin_date,date__lte=end_date).values('date').annotate(allconsume=Sum('allconsume')).order_by('date')
        for p in range_data:
            date.append(p['date'])
            consume.append(float(p['allconsume']))
        context={'date':date,'consume':consume}
        return JsonResponse(context)

    elif differ=='single_tab':
        choice_date=request.POST.get('choice_date')
        choice_date=datetime.datetime.strptime(choice_date,'%Y-%m-%d').date()

        # 前一天日期，做环比
        yesterday = choice_date + datetime.timedelta(days=-1)
        # 前七天日期，做同比
        lastweek = choice_date + datetime.timedelta(days=-7)

        """ 计算当日数据，前日数据，日环比，周同比 """
        # 计算最新日期数据
        allconsume = models.Total.objects.filter(date=choice_date).aggregate(allconsume=Sum('allconsume'))
        feedconsume = models.Feed.objects.filter(date=choice_date).aggregate(feedconsume=Sum('feed_allconsume'))
        opconsume = models.OtherPro.objects.filter(date=choice_date).aggregate(opconsume=Sum('op_allconsume'))

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

        choice_consume={
            'allconsume':round(allconsume['allconsume']/10000,2),
            'feedconsume':round(feedconsume['feedconsume']/10000,2),
            'opconsume': round(opconsume['opconsume']/10000,2),

            'allconsume_l1': round(allconsume_l1['allconsume']/10000,2),
            'feedconsume_l1': round(feedconsume_l1['feedconsume']/10000,2),
            'opconsume_l1': round(opconsume_l1['opconsume']/10000,2),

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
    pass

# 处理品牌数据
def more_op(request):
    pass

# 处理一级行业数据
def industry_1(request):
    return render(request,'datacenter/industry_1.html')

# 处理二级行业数据
def industry_2(request):
    return render(request,'datacenter/industry_2.html')

# 处理失效数据
def invalid(request):
    pass