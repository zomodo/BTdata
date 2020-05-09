from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import datetime
from datacenter import models

from django.db.models import Sum,Count,Avg
# Create your views here.


def summary(request):
    # 数据最新日期
    latest_date=models.Total.get_latest_date()
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

    consume={
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
        'consume':consume,
        'compare_l1':compare_l1,
        'compare_l7':compare_l7,
    }

    # context={
    #     'date':latest_date,
    #     'allconsume':bothconsume['allconsume'],
    #     'searchconsume':bothconsume['searchconsume'],
    #     'feedconsume':feedconsume['feedconsume'],
    #     'opconsume':opconsume['opconsume']
    # }
    return render(request,'datacenter/summary.html',context)


def summary_chart(request):
    # 数据最新日期
    latest_date = models.Total.get_latest_date()
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