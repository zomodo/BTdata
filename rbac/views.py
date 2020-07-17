from django.shortcuts import render,HttpResponse
from django.shortcuts import redirect,reverse
import json

from rbac import models
from rbac import forms
from rbac.init_permission import init_permission
# Create your views here.

def login(request):
    if request.method=='POST':
        form=forms.LoginForm(request.POST)
        message='请检查填写的内容！'
        if form.is_valid():
            try:
                user = models.User.objects.get(username=form.cleaned_data['username'])
            except:
                message = '用户名错误！'
                context = {'form':form,'message': json.dumps(message)}
                return render(request, 'rbac/login.html', context)
            if user.password == form.cleaned_data['password']:
                init_permission(request, user)
                return redirect(reverse('index'))
            else:
                message = '密码错误！'
                context = {'form':form,'message': json.dumps(message)}
                return render(request, 'rbac/login.html', context)
        else:
            context = {'form':form,'message': json.dumps(message)}
            return render(request, 'rbac/login.html', context)

    else:
        form = forms.LoginForm()
        context = {'form':form,'message': json.dumps('success')}
        return render(request, 'rbac/login.html', context)


def logout(request):
    request.session.flush()
    return redirect(reverse('index'))


def index(request):

    alldata=models.Message.objects.filter(status=1).only('id','title','created_time','is_top','is_jump')
    sheet0=alldata.filter(depart=0)[:20]
    sheet1=alldata.filter(depart=1)[:20]
    sheet2=alldata.filter(depart=2)[:20]

    context={
        'mark':'index',
        'sheet0':sheet0,
        'sheet1':sheet1,
        'sheet2':sheet2,
    }

    return render(request,'rbac/index.html',context)


def message(request,id):

    message=models.Message.objects.get(id=id)
    menu_list=models.Message.objects.filter(depart=message.depart,status=1).only('title','is_jump')[:20]

    context={
        'menu_list':menu_list,
        'message':message,
    }
    return render(request,'rbac/message.html',context)


def contact(request):
    context = {'mark': 'contact'}
    return render(request,'rbac/contact.html',context)


def permission_denied(request,exception):
    context={'exception':exception}
    return render(request,'rbac/403.html',context)

def page_not_found(request,exception):
    context = {'exception': exception}
    return render(request, 'rbac/404.html',context)

def error(request):
    return render(request, 'rbac/500.html')