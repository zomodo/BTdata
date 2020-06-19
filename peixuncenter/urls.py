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

from peixuncenter import views

urlpatterns = [

    path('cate1/', views.cate1, name='cate1'),
    path('cate2/', views.cate2, name='cate2'),
    path('cate3/', views.cate3, name='cate3'),
    path('cate4/', views.cate4, name='cate4'),
    path('cate5/', views.cate5, name='cate5'),
    path('cate6/', views.cate6, name='cate6'),
    path('cate7/', views.cate7, name='cate7'),
    path('cate1/<int:id>/', views.cate_detail, name='cate_detail1'),
    path('cate2/<int:id>/', views.cate_detail, name='cate_detail2'),
    path('cate3/<int:id>/', views.cate_detail, name='cate_detail3'),
    path('cate4/<int:id>/', views.cate_detail, name='cate_detail4'),
    path('cate5/<int:id>/', views.cate_detail, name='cate_detail5'),
    path('cate6/<int:id>/', views.cate_detail, name='cate_detail6'),
    path('cate7/<int:id>/', views.cate_detail, name='cate_detail7'),


]
