from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum,Q,F
import datetime
import calendar
import jieba
import jieba.analyse
from collections import Counter

from django.views.decorators.cache import cache_page

from apidata import forms
from apidata import models
# Create your views here.

# 处理关键词数据
def keyword(request):
    latest_date=models.KeyWord.get_latest_date()
    context={'latest_date':latest_date}
    return render(request,'apidata/keyword.html',context)


def keyword_tab1(request):
    latest_date=models.KeyWord.get_latest_date()
    begin_date=latest_date.replace(day=1)
    end_day=calendar.monthrange(latest_date.year,latest_date.month)[1]
    end_date=latest_date.replace(day=end_day)

    ctype=request.POST.get('c1type')
    ptype=request.POST.get('p1type')
    kword=request.POST.get('kword').strip()
    kw_list=[]

    if ctype==ptype==kword:
        kw_data = models.KeyWord.objects.filter(date__range=(begin_date,end_date)).values('indus_1', 'indus_2','keyword', 'consume','click', 'pv')[:10]
        for data in kw_data:
            kw_list.append(data)
        context={
            'kw_list':kw_list,
        }
        return JsonResponse(context)

    if ctype=='all':

        kw_data = models.KeyWord.objects.\
            filter(date__range=(begin_date,end_date),keyword__icontains=kword).\
            values('indus_1', 'indus_2', 'keyword', 'consume', 'click', 'pv').order_by(ptype)[:200]
        for data in kw_data:
            kw_list.append(data)

        context={
            'kw_list':kw_list,
        }
        return JsonResponse(context)

    else:

        kw_data = models.KeyWord.objects.\
            filter(date__range=(begin_date,end_date),depart_1=ctype,keyword__icontains=kword).\
            values('indus_1', 'indus_2', 'keyword', 'consume', 'click', 'pv').order_by(ptype)[:200]
        for data in kw_data:
            kw_list.append(data)
        context={
            'kw_list':kw_list
        }
        return JsonResponse(context)


def keyword_tab2(request):

    latest_date=models.KeyWord.get_latest_date()
    begin_date=latest_date.replace(day=1)
    end_day=calendar.monthrange(latest_date.year,latest_date.month)[1]
    end_date=latest_date.replace(day=end_day)

    ctype=request.POST.get('c2type')
    ptype=request.POST.get('p2type')
    indus1=request.POST.get('indus1')
    indus2=request.POST.get('indus2')
    kw_list=[]

    if ctype=='all':
        kw_data = models.KeyWord.objects.\
            filter(date__range=(begin_date,end_date),indus_1=indus1,indus_2=indus2).\
            values('indus_1', 'indus_2', 'keyword', 'consume', 'click', 'pv').order_by(ptype)[:200]
        for data in kw_data:
            kw_list.append(data)
        context={
            'kw_list':kw_list
        }
        return JsonResponse(context)

    else:

        kw_data = models.KeyWord.objects.\
            filter(date__range=(begin_date,end_date),depart_1=ctype,indus_1=indus1,indus_2=indus2).\
            values('indus_1', 'indus_2', 'keyword', 'consume', 'click', 'pv').order_by(ptype)[:200]
        for data in kw_data:
            kw_list.append(data)
        context={
            'kw_list':kw_list
        }
        return JsonResponse(context)


# 处理分小时数据
def hour(request):
    latest_date=models.HourData.get_latest_date()
    context={'latest_date':latest_date}
    return render(request,'apidata/hour.html',context)


def hour_chart(request):
    latest_date=models.HourData.get_latest_date()
    begin_date=latest_date.replace(day=1)
    end_day=calendar.monthrange(latest_date.year,latest_date.month)[1]
    end_date=latest_date.replace(day=end_day)

    ctype=request.POST.get('ctype')
    indus1=request.POST.get('indus1')
    indus2=request.POST.get('indus2')

    date_list=[]
    consume_list=[]
    click_list=[]
    pv_list=[]

    if ctype=='all':

        alldata=models.HourData.objects.filter(date__range=(begin_date,end_date),indus_1=indus1,indus_2=indus2).\
            values('hour').annotate(consume=Sum('consume'),click=Sum('click'),pv=Sum('pv')).order_by('hour')
        # print(alldata)
        for data in alldata:
            date_list.append(data['hour'])
            consume_list.append(float(data['consume']))
            click_list.append(data['click'])
            pv_list.append(data['pv'])

        for t in range(24):
            if t not in date_list:
                date_list.insert(t, t)
                consume_list.insert(t, 0)
                click_list.insert(t, 0)
                pv_list.insert(t, 0)

        context={
            'xData':date_list,
            'datasets':[
                {'name': '消费', 'data': consume_list, 'unit': '消费', 'type': 'areaspline', 'valueDecimals': 2},
                {'name': '点击', 'data': click_list, 'unit': '点击', 'type': 'areaspline', 'valueDecimals': 0},
                {'name': '展现', 'data': pv_list, 'unit': '展现', 'type': 'areaspline', 'valueDecimals': 0},
            ]
        }

        return JsonResponse(context)

    else:

        alldata=models.HourData.objects.filter(date__range=(begin_date,end_date),depart_1=ctype,indus_1=indus1,indus_2=indus2).\
            values('hour').annotate(consume=Sum('consume'),click=Sum('click'),pv=Sum('pv')).order_by('hour')
        # print(alldata)
        for data in alldata:
            date_list.append(data['hour'])
            consume_list.append(float(data['consume']))
            click_list.append(data['click'])
            pv_list.append(data['pv'])

        for t in range(24):
            if t not in date_list:
                date_list.insert(t, t)
                consume_list.insert(t, 0)
                click_list.insert(t, 0)
                pv_list.insert(t, 0)

        context={
            'xData':date_list,
            'datasets':[
                {'name': '消费', 'data': consume_list, 'unit': '消费', 'type': 'areaspline', 'valueDecimals': 2},
                {'name': '点击', 'data': click_list, 'unit': '点击', 'type': 'areaspline', 'valueDecimals': 0},
                {'name': '展现', 'data': pv_list, 'unit': '展现', 'type': 'areaspline', 'valueDecimals': 0},
            ]
        }

        return JsonResponse(context)


# 处理分地域数据
def area(request):
    latest_date=models.AreaData.get_latest_date()
    context={'latest_date':latest_date}
    return render(request,'apidata/area.html',context)


def area_chart(request):
    latest_date=models.AreaData.get_latest_date()
    begin_date=latest_date.replace(day=1)
    end_day=calendar.monthrange(latest_date.year,latest_date.month)[1]
    end_date=latest_date.replace(day=end_day)

    ctype=request.POST.get('ctype')
    indus1=request.POST.get('indus1')
    indus2=request.POST.get('indus2')
    ptype=request.POST.get('ptype')

    data_cn=[]
    data_hb=[]

    if ctype=='all':

        cn_all=models.AreaData.objects.filter(date__range=(begin_date,end_date),indus_1=indus1,indus_2=indus2).aggregate(all=Sum(ptype))
        cn_area=models.AreaData.objects.filter(date__range=(begin_date,end_date),indus_1=indus1,indus_2=indus2).\
            values('area1').annotate(ptype=Sum(ptype)).order_by('-ptype')

        for data in cn_area:
            data_cn.append({'name': data['area1'], 'value': float(data['ptype'])/float(cn_all['all'])})

        hb_all=models.AreaData.objects.filter(date__range=(begin_date,end_date),area1='湖北',indus_1=indus1,indus_2=indus2).aggregate(all=Sum(ptype))
        hb_area = models.AreaData.objects.filter(date__range=(begin_date,end_date),area1='湖北', indus_1=indus1, indus_2=indus2). \
            values('area2').annotate(ptype=Sum(ptype)).order_by('-ptype')
        for data in hb_area:
            data_hb.append({'name': data['area2'], 'value': float(data['ptype'])/float(hb_all['all'])})

        context={
            'data_cn':data_cn,
            'data_hb':data_hb,
        }

        return JsonResponse(context)

    else:

        cn_all = models.AreaData.objects.filter(date__range=(begin_date,end_date),depart_1=ctype,indus_1=indus1, indus_2=indus2).aggregate(all=Sum(ptype))
        cn_area = models.AreaData.objects.filter(date__range=(begin_date,end_date), depart_1=ctype,indus_1=indus1, indus_2=indus2). \
            values('area1').annotate(ptype=Sum(ptype)).order_by('-ptype')
        for data in cn_area:
            data_cn.append({'name': data['area1'], 'value': float(data['ptype'])/float(cn_all['all'])})

        hb_all = models.AreaData.objects.filter(date__range=(begin_date,end_date),depart_1=ctype,area1='湖北',indus_1=indus1,indus_2=indus2).aggregate(all=Sum(ptype))
        hb_area = models.AreaData.objects.filter(date__range=(begin_date,end_date), depart_1=ctype,area1='湖北', indus_1=indus1, indus_2=indus2). \
            values('area2').annotate(ptype=Sum(ptype)).order_by('-ptype')
        for data in hb_area:
            data_hb.append({'name': data['area2'], 'value': float(data['ptype'])/float(hb_all['all'])})

        context = {
            'data_cn': data_cn,
            'data_hb': data_hb,
        }

        return JsonResponse(context)


# 处理新注册公司数据
def company(request):

    alldata = models.NewCompany.get_latest()
    latest_date = alldata[0]
    allcount = round(alldata[1] / 10000, 2)

    if request.method=="GET":
        form=forms.CompanyForm()
        allcompany = models.NewCompany.objects.filter(location='武汉',companyName__contains='公司').only('companyName','identifier','founder','registerMoney','date','address')[:50]

        context={
            'form':form,
            'allcompany':allcompany,
            'latest_date':latest_date,
            'allcount':allcount,
        }
        return render(request,'apidata/company.html',context)


    form=forms.CompanyForm(request.POST)
    if form.is_valid():
        date=form.cleaned_data.get('date')
        city=form.cleaned_data.get('area','all')
        word=form.cleaned_data.get('searchword').strip()
        search_dict={}

        q_all=Q()

        if '-' in date:
            begin_date = date.split('-')[0]
            end_date = date.split('-')[1]
            begin_date = datetime.datetime.strptime(begin_date, '%Y.%m.%d').date()
            end_date = datetime.datetime.strptime(end_date, '%Y.%m.%d').date()

            search_dict['date__range']=(begin_date,end_date)

        if word:
            # search_dict['companyName__icontains']=word
            q1=Q(companyName__icontains=word)
            q2=Q(makesOffer__icontains=word)
            q_all=q1 | q2

        if city:
            search_dict['location']=city

        if search_dict['location']=='all':
            search_dict.pop('location')
            allcompany=models.NewCompany.objects.filter(q_all,**search_dict).\
                only('companyName','identifier','founder','registerMoney','date','address')[:100]

            context={
                'form':form,
                'allcompany':allcompany,
                'latest_date':latest_date,
                'allcount':allcount,
            }
            return render(request,'apidata/company.html',context)

        else:

            allcompany=models.NewCompany.objects.filter(q_all,**search_dict).\
                only('companyName','identifier','founder','registerMoney','date','address')[:100]

            context={
                'form':form,
                'allcompany':allcompany,
                'latest_date':latest_date,
                'allcount':allcount,
            }

            return render(request,'apidata/company.html',context)


def company_detail(request,code):
    form=forms.CompanyForm()
    company=models.NewCompany.objects.get(identifier=str(code))

    context={
        'form':form,
        'company':company,
    }
    return render(request,'apidata/company_detail.html',context)


def searchword(request):

    if request.method == 'GET':
        latest_date = models.SearchWord.get_latest_date()
        end_date = datetime.timedelta(days=6)+latest_date

        context={
            "latest_date":latest_date,
            "end_date":end_date,

        }
        return render(request,'apidata/searchword.html',context)

    if request.method == 'POST':
        area=request.POST.get('area')
        indus1=request.POST.get('indus1')
        indus2=request.POST.get('indus2')
        s={}
        if area != 'all':
            s['depart_1']=area
        if indus1:
            s['indus_1']=indus1
        if indus2 != 'all':
            s['indus_2']=indus2

        c1=Counter()
        c2=Counter()
        # jieba.enable_parallel(4)      # 并行分词 ，不支持windows
        data1=models.SearchWord.objects.filter(**s).only('searchword')
        data2=models.SearchWord.objects.filter(**s).only('searchword').order_by('-consume')[:100]
        if data1:
            for i in data1:
                word=jieba.analyse.extract_tags(i.searchword)
                for w in word:
                    c1[w]+=1

            for i in data2:
                word=jieba.analyse.extract_tags(i.searchword)
                for w in word:
                    c2[w]+=1

            data1_list=[]
            for wd in c1.most_common(50):
                data_dict = {}
                data_dict['name']=wd[0]
                data_dict['weight']=wd[1]
                data1_list.append(data_dict)

            data2_list=[]
            for wd in c2.most_common(50):
                data_dict = {}
                data_dict['name']=wd[0]
                data_dict['weight']=wd[1]
                data2_list.append(data_dict)

            # print(data_list)
            return JsonResponse({'c1': data1_list,'c2': data2_list})

        return JsonResponse({'c1':[{'name':'没有数据'}],'c2':[{'name':'没有数据'}]})
