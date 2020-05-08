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
    return redirect(reverse('login'))

def index(request):
    context = {'mark':'index'}
    return render(request,'rbac/index.html',context)

def contact(request):
    context = {'mark': 'contact'}
    return render(request,'rbac/contact.html',context)

