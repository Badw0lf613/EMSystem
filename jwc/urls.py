"""jwc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url, include
from EMSystem import views

urlpatterns = [
    path('django_admin/', admin.site.urls),
    # url(r'^EMSystem/', include('EMSystem.urls'))
    path('', views.login),  # 登录
    path('admin/', views.admin),  # 管理员
    path('teacher/', views.teacher),  # 教师
    path('student/', views.student),  # 学生

]