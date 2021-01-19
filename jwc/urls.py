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
from django.urls import path, re_path
from django.conf.urls import url, include
from EMSystem import views

urlpatterns = [
    path('django_admin/', admin.site.urls),
    # url(r'^EMSystem/', include('EMSystem.urls'))
    path('', views.login_view),  # 登录
    path('admin/', views.admin_view),  # 管理员
    path('teacher/', views.teacher_view),  # 教师
    path('student/', views.student_view),  # 学生
    path('admin/delete/', views.delete_student), # 删除学生
    path('admin/edit/', views.edit_student) # 编辑学生
    # path('student/<username>/',views.student_view,name='username')
]
