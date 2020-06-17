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
from django.conf.urls.static import static

from rbac import views as rbac_views
from datacenter import views as data_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', rbac_views.index),
    path('login/',rbac_views.login,name='login'),
    path('logout/',rbac_views.logout,name='logout'),
    path('index/',rbac_views.index,name='index'),
    path('message/<str:id>',rbac_views.message,name='message'),
    path('contact/',rbac_views.contact,name='contact'),

    # 路由转发，转到数据部分
    path('data/',include(('datacenter.urls','data'),namespace='data')),

    # 路由转发，转到数据部分
    path('api/',include(('apidata.urls','api'),namespace='api')),

    # 路由转发，转到产品部分
    path('chanpin/',include(('chanpincenter.urls','chanpin'),namespace='chanpin')),

    # 路由转发，转到培训部分
    path('peixun/',include(('peixuncenter.urls','peixun'),namespace='peixun')),

    path('ckeditor/',include('ckeditor_uploader.urls')),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

# 意思是当DEBUG=True时候引入django-debug-toolbar的debug_toolbar，并配置对应的URL地址
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/',include(debug_toolbar.urls)),
    ]

# 自定义错误页面
handler403 = rbac_views.permission_denied
handler404 = rbac_views.page_not_found
handler500 = rbac_views.error