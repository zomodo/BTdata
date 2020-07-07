from django.shortcuts import render
from peixuncenter import models
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

from django.http import FileResponse
from django.utils.encoding import escape_uri_path
from urllib import parse
# Create your views here.

# Django内置分页扩展
class CustomPaginator(Paginator):
    def __init__(self,current_page,per_page_num,*args,**kwargs):
        self.current_page=int(current_page)     # 当前页
        self.per_page_num=int(per_page_num)     # 显示的页数
        super(CustomPaginator, self).__init__(*args,**kwargs)

    def page_num_range(self):
        # self.num_pages  总页数
        # 页数特别少
        if self.num_pages <= self.per_page_num:
            return range(1,self.num_pages+1)
        # 页数特别多
        part=int(self.per_page_num/2)

        if self.current_page <= part:
            # 判断头部
            return range(1,self.per_page_num+1)
        elif self.current_page > (self.num_pages-part):
            # 判断尾部
            return range(self.num_pages-self.per_page_num+1,self.num_pages+1)
        else:
            # 剩余中间
            return range(self.current_page-part,self.current_page+part+1)


def getpage(request,resources_list):
    current_page = request.GET.get('page', '1')
    per_page_num=5
    paginator = CustomPaginator(current_page, per_page_num, resources_list, 12)

    try:
        allresources = paginator.page(current_page)
    except PageNotAnInteger:
        # 如果请求的页数不是整数，返回第一页
        allresources = paginator.page(1)
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页
        allresources = paginator.page(paginator.num_pages)

    return allresources


def cate1(request):
    category=models.CategoryInfo.objects.get(id=1)
    resources_list = models.ResourceInfo.objects.\
        filter(status=1, category_id=1).\
        only('title','is_top','image','desc')

    allresources = getpage(request, resources_list)

    context={
        'allresources':allresources,
        'category':category,
    }
    return render(request,'peixuncenter/resources.html',context)


def cate2(request):
    category=models.CategoryInfo.objects.get(id=2)
    resources_list = models.ResourceInfo.objects.\
        filter(status=1, category__status=1, category_id=2).\
        only('title','is_top','image','desc')

    allresources = getpage(request, resources_list)

    context={
        'allresources':allresources,
        'category': category,
    }
    return render(request,'peixuncenter/resources.html',context)

def cate3(request):
    category=models.CategoryInfo.objects.get(id=3)
    resources_list = models.ResourceInfo.objects.\
        filter(status=1, category__status=1, category_id=3).\
        only('title','is_top','image','desc')

    allresources = getpage(request, resources_list)

    context={
        'allresources':allresources,
        'category': category,
    }
    return render(request,'peixuncenter/resources.html',context)


def cate4(request):
    category=models.CategoryInfo.objects.get(id=4)
    resources_list = models.ResourceInfo.objects.\
        filter(status=1, category__status=1, category_id=4).\
        only('title','is_top','image','desc')

    allresources = getpage(request, resources_list)

    context={
        'allresources':allresources,
        'category': category,
    }
    return render(request,'peixuncenter/resources.html',context)


def cate5(request):
    category=models.CategoryInfo.objects.get(id=5)
    resources_list = models.ResourceInfo.objects.\
        filter(status=1, category__status=1, category_id=5).\
        only('title','is_top','image','desc')

    allresources = getpage(request, resources_list)

    context={
        'allresources':allresources,
        'category': category,
    }
    return render(request,'peixuncenter/resources.html',context)


def cate7(request):
    category=models.CategoryInfo.objects.get(id=7)
    resources_list = models.ResourceInfo.objects.\
        filter(status=1, category__status=1, category_id=7).\
        only('title','is_top','image','desc')

    allresources = getpage(request, resources_list)

    context={
        'allresources':allresources,
        'category': category,
    }
    return render(request,'peixuncenter/resources.html',context)


def cate_detail(request,id):
    data=models.ResourceInfo.objects.filter(status=1).get(id=id)
    category=models.CategoryInfo.objects.filter(id=data.category_id).get()

    context={
        'data':data,
        'category':category,
    }
    return render(request,'peixuncenter/cate_detail.html',context)


def sharefile(request,id=None):
    if not id:
        allcategory=models.ShareCategory.objects.filter(status=1).only('name')
        alldata=models.ShareFile.objects.\
            filter(status=1,category__status=1).\
            only('title','upload_file','is_top','created_time')

        context={
            'allcategory':allcategory,
            'alldata':alldata,
        }
        return render(request, 'peixuncenter/sharefile.html',context)

    else:
        allcategory = models.ShareCategory.objects.filter(status=1).only('name')
        alldata = models.ShareFile.objects.\
            filter(status=1,category_id=id,category__status=1).\
            only('title','upload_file','is_top','created_time')

        context = {
            'allcategory': allcategory,
            'alldata': alldata,
            'category_id': id,
        }
        return render(request, 'peixuncenter/sharefile.html', context)

def sharefile_show(request,id):

    data = models.ShareFile.objects.filter(status=1, id=id).get()
    alltitle=models.ShareFile.objects.filter(status=1,category_id=data.category_id).only('title')[:10]

    context = {
        'data': data,
        'alltitle':alltitle,
    }
    return render(request, 'peixuncenter/sharefile_detail.html', context)

def sharefile_download(request,id=None):
    data = models.ShareFile.objects.get(status=1,id=id)

    pth=parse.unquote(str(data.upload_file.url).strip('/'))
    file_name=pth.split('/')[-1]

    file = open(pth, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename={}'.format(escape_uri_path(file_name))
    return response