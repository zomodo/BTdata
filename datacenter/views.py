from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import datetime
from datacenter import models

from django.db.models import Sum,Count,Avg
# Create your views here.

# 总消费
def allconsume(request):
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

    # context={
    #     'date':latest_date,
    #     'allconsume':bothconsume['allconsume'],
    #     'searchconsume':bothconsume['searchconsume'],
    #     'feedconsume':feedconsume['feedconsume'],
    #     'opconsume':opconsume['opconsume']
    # }
    return render(request, 'datacenter/allconsume.html', context)

# 总消费-图表
def allconsume_chart(request):
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

# 处理有消费账户数
def allaccount(request):
    # 数据最新日期
    latest_date=models.Total.get_latest_date()
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
    latest_date = models.Total.get_latest_date()
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
    return render(request,'datacenter/more_all.html')

# 处理信息流数据
def more_feed(request):
    pass

# 处理品牌数据
def more_op(request):
    pass

# 处理一级行业数据
def industry_1(request):
    pass

# 处理二级行业数据
def industry_2(request):
    pass

# 处理失效数据
def invalid(request):
    pass