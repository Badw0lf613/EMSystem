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
    path('admin/', views.admin_index),  # 管理员
    path('teacher/', views.teacher_index),  # 教师
    path('student/', views.student_index),  # 学生
    path('student/QueryCourse', views.student_QueryCourse,name="student_QueryCourse"),  # 学生课程查询
    path('student/AddCourse', views.student_AddCourse, name="student_AddCourse"),  # 学生选课
    path('student/DeleteCourse', views.student_DeleteCourse, name="student_DeleteCourse"),  # 学生退课
    path('student/QueryGrades', views.student_QueryGrades, name="student_QueryGrades"),  # 学生成绩查询
    path('student/CourseTable', views.student_CourseTable, name="student_CourseTable"),  # 学生课表查询
    path('admin/StudentManagement', views.student_Management, name="student_Management"),  # 学生管理
    path('admin/StudentManagement/search/delete', views.delete_student), # 删除学生
    path('admin/StudentManagement/search/edit', views.edit_student),  # 编辑学生
    path('admin/StudentManagement/search/add', views.add_student),  # 添加学生
    path('admin/StudentManagement/search/', views.search_student)
    # path('student/<username>/',views.student_view,name='username')
]
