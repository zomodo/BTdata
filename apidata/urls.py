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

from apidata import views

urlpatterns = [
    path('keyword/', views.keyword, name='apikeyword'),
    path('keyword_tab1/', views.keyword_tab1, name='keyword_tab1'),
    path('keyword_tab2/', views.keyword_tab2, name='keyword_tab2'),

    path('hour/', views.hour, name='apihour'),
    path('hour_chart/', views.hour_chart, name='hour_chart'),

    path('area/', views.area, name='apiarea'),
    path('area_chart/', views.area_chart, name='area_chart'),

    path('company/', views.company, name='company'),
    path('company/<str:code>', views.company_detail, name='company_detail'),

]