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

from rbac import views as rbac_views
from datacenter import views as data_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',rbac_views.index),
    path('login/',rbac_views.login,name='login'),
    path('logout/',rbac_views.logout,name='logout'),
    path('index/',rbac_views.index,name='index'),
    path('contact/',rbac_views.contact,name='contact'),

    path('summary/',data_views.summary,name='summary'),

]
