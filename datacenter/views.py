from django.shortcuts import render
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
