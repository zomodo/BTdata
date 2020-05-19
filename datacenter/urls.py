"""BTdata URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings

from datacenter import views

urlpatterns = [
    path('allconsume/', views.allconsume, name='allconsume'),
    path('allconsume_chart/', views.allconsume_chart, name='allconsume_chart'),
    path('allaccount/', views.allaccount, name='allaccount'),
    path('allaccount_chart/', views.allaccount_chart, name='allaccount_chart'),

    path('more_all/', views.more_all, name='more_all'),
    path('more_all_chart/', views.more_all_chart, name='more_all_chart'),

    path('industry_1/', views.industry_1, name='industry_1'),
    path('industry_2/', views.industry_2, name='industry_2'),

]

# 意思是当DEBUG=True时候引入django-debug-toolbar的debug_toolbar，并配置对应的URL地址
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
