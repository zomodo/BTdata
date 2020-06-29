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

from django.urls import path,re_path
from django.urls import include
from django.conf import settings

from chanpincenter import views

urlpatterns = [
    path('resources/', views.resources, name='resources'),
    path('resources/<int:id>/', views.resources, name='resources_category'),

    path('resources/show_pdf/<int:id>/', views.resources_show, name='resources_show'),
    path('resources/download_pdf/<int:id>/', views.resources_download, name='resources_download'),

    path('share_example/', views.share_example, name='share_example'),
    path('share_example/<int:cid>/', views.share_example, name='share_example_category'),

    path('share_example/show_pdf/<int:id>/', views.share_example_show, name='share_example_show'),
    path('share_example/download_pdf/<int:id>/', views.share_example_download, name='share_example_download'),


    path('insight/', views.insight, name='insight'),
    path('insight/<int:id>/', views.insight, name='insight_detail'),
    path('insight/download/<int:id>/', views.insight_download, name='insight_download'),

    path('item/', views.item, name='item'),
    path('item/<int:id>/', views.item, name='item_detail'),
    path('item/download/<int:id>/', views.item_download, name='item_download'),

]