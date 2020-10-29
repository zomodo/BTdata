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

    path('more_feed/', views.more_feed, name='more_feed'),
    path('more_op/', views.more_op, name='more_op'),

    path('industry_1/', views.industry_1, name='industry_1'),
    path('indus1_chart/',views.indus1_chart,name='indus1_chart'),

    path('industry_2/', views.industry_2, name='industry_2'),
    path('indus2_chart/', views.indus2_chart, name='indus2_chart'),

    path('get_indus1/',views.get_indus1,name='get_indus1'),
    path('get_indus2/',views.get_indus2,name='get_indus2'),

    path('invalid/',views.invalid,name='invalid'),
    path('get_invalid/',views.get_invalid,name='get_invalid'),
    path('personal/',views.personal,name='personal'),
    path('personal_detail/',views.personal_detail,name='personal_detail'),
    path('personal_chart/',views.personal_chart,name='personal_chart'),


]