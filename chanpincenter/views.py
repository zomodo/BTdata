from django.shortcuts import render
from chanpincenter import models
from django.http import FileResponse
from django.utils.encoding import escape_uri_path
from django.db.models import Sum,Count,Avg,Q

from urllib import parse
# Create your views here.

def resources(request,id=None):
    if not id:
        allcategory=models.ResourceCategory.objects.filter(status=1).only('name')
        allcontent=models.Resource.objects.\
            filter(status=1,category__status=1).\
            only('title','upload_file','is_top','created_time')

        context={
            'allcategory':allcategory,
            'allcontent':allcontent,
        }
        return render(request, 'chanpincenter/resources.html',context)

    else:

        allcategory = models.ResourceCategory.objects.filter(status=1).only('name')
        allcontent = models.Resource.objects. \
            filter(status=1, category__status=1, category_id=id). \
            only('title', 'upload_file', 'is_top','created_time')
        context = {
            'allcategory': allcategory,
            'allcontent': allcontent,
            'category_id': id,
        }
        return render(request, 'chanpincenter/resources.html', context)


def resources_show(request,id):
    data=models.Resource.objects.get(id=id)
    alltitle=models.Resource.objects.filter(category_id=data.category_id)[:10]
    context={
        'data':data,
        'alltitle':alltitle,
    }
    return render(request, 'chanpincenter/resources_show_pdf.html', context)

def resources_download(request,id):
    data=models.Resource.objects.get(id=id)

    pth=parse.unquote(str(data.upload_file.url).strip('/'))
    file_name=pth.split('/')[-1]

    file = open(pth, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename={}'.format(escape_uri_path(file_name))
    return response


def share_example(request,cid=None):
    if not cid:
        allcategory = models.ShareExampleCategory.objects.filter(status=1).only('name')
        allcontent = models.ShareExample.objects.\
            filter(status=1, category__status=1).\
            only('title', 'upload_file','is_top','created_time')

        context = {
            'allcategory': allcategory,
            'allcontent': allcontent,
        }
        return render(request, 'chanpincenter/share_example.html', context)

    else:

        allcategory = models.ShareExampleCategory.objects.filter(status=1).only('name')
        allcontent = models.ShareExample.objects. \
            filter(status=1, category__status=1, category_id=cid). \
            only('title', 'upload_file', 'is_top', 'created_time')
        context = {
            'allcategory': allcategory,
            'allcontent': allcontent,
            'category_id': cid,
        }
        return render(request, 'chanpincenter/share_example.html', context)

def share_example_show(request,id):
    data = models.ShareExample.objects.get(id=id)
    alltitle = models.ShareExample.objects.filter(category_id=data.category_id)[:10]
    context = {
        'data': data,
        'alltitle': alltitle,
    }
    return render(request, 'chanpincenter/share_example_show_pdf.html', context)


def share_example_download(request,id):
    data = models.ShareExample.objects.get(id=id)

    pth=parse.unquote(str(data.upload_file.url).strip('/'))
    file_name=pth.split('/')[-1]

    file = open(pth, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename={}'.format(escape_uri_path(file_name))
    return response


def insight(request,id=None):
    if not id:
        data_list=models.Insight.objects.filter(status=1).only('title','upload_file','is_top','created_time')
        context={
            'data_list':data_list,
        }
        return render(request, 'chanpincenter/insight.html',context)

    else:

        data = models.Insight.objects.get(id=id)
        context = {
            'data': data,
        }
        return render(request, 'chanpincenter/show_detail.html', context)


def insight_download(request,id):
    data = models.Insight.objects.get(id=id)

    pth=parse.unquote(str(data.upload_file.url).strip('/'))
    file_name=pth.split('/')[-1]

    file = open(pth, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename={}'.format(escape_uri_path(file_name))
    return response


def item(request,id=None):
    if not id:
        data_list=models.Item.objects.filter(status=1).only('title','upload_file','is_top','created_time')
        context={
            'data_list':data_list,
        }
        return render(request, 'chanpincenter/item.html',context)

    else:
        data = models.Item.objects.get(id=id)
        context = {
            'data': data,
        }
        return render(request, 'chanpincenter/show_detail.html', context)


def item_download(request,id):
    data = models.Item.objects.get(id=id)

    pth=parse.unquote(str(data.upload_file.url).strip('/'))
    file_name=pth.split('/')[-1]

    file = open(pth, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename={}'.format(escape_uri_path(file_name))
    return response