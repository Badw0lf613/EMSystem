import MySQLdb
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

# Create your views here.
# 学生信息列表处理函数
# def index(request):
#     conn = MySQLdb.connect(host="localhost", user="root", passwd="1234", db="jwc", charset='utf8')
#     with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
#         cursor.execute("SELECT id,student_no,student_name FROM emsystem_student")
#         students = cursor.fetchall()
#     return render(request, 'index.html', {'students': students})
#
# # 学生信息新增处理函数
# def add(request):
#     if request.method == 'GET':
#         return render(request, 'add.html')
#     else:
#         student_no = request.POST.get('student_no', '')
#         student_name = request.POST.get('student_name', '')
#         conn = MySQLdb.connect(host="localhost", user="root", passwd="1234", db="jwc", charset='utf8')
#         with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
#             cursor.execute("INSERT INTO emsystem_student (student_no,student_name, id) "
#                            "values (%s,%s,%s)", [student_no, student_name, '1'])
#             conn.commit()
#         return redirect('../')
#
# # 学生信息修改处理函数
# def edit(request):
#     if request.method == 'GET':
#         id = request.GET.get("id")
#         print(id)
#         conn = MySQLdb.connect(host="localhost", user="root", passwd="1234", db="jwc", charset='utf8')
#         with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
#             cursor.execute("SELECT id,student_no,student_name FROM emsystem_student where id =%s", [id])
#             student = cursor.fetchone()
#         return render(request, 'edit.html', {'student': student})
#     else:
#         id = request.POST.get("id")
#         print(id)
#         student_no = request.POST.get('student_no', '')
#         student_name = request.POST.get('student_name', '')
#         conn = MySQLdb.connect(host="localhost", user="root", passwd="1234", db="jwc", charset='utf8')
#         with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
#             cursor.execute("UPDATE emsystem_student set student_no=%s,student_name=%s where id =%s",
#                            [student_no, student_name, id])
#             conn.commit()
#         return redirect('../')
#
# # 学生信息删除处理函数
# def delete(request):
#     id = request.GET.get("id")
#     print(id)
#     conn = MySQLdb.connect(host="localhost", user="root", passwd="1234", db="jwc", charset='utf8')
#     with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
#         cursor.execute("DELETE FROM emsystem_student WHERE id =%s", [id])
#         conn.commit()
#     return  redirect('../')


def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        pass_word = request.POST.get("password")
        print(username)
        print(pass_word)
        user = authenticate(username=username, password=pass_word)
        if user is not None:
            if user.is_superuser==1 and user.is_staff==1:            # 管理员
                return HttpResponseRedirect("/EMSystem/admin")
            elif user.is_superuser==0 and user.is_staff==1:          # 老师
                return HttpResponseRedirect("/EMSystem/teacher")
            elif user.is_superuser==0 and user.is_staff==0:          # 学生
                return HttpResponseRedirect("/EMSystem/student")
        else:
            alert = "用户名或密码错误"
            print(alert)
    # else:
    #     user = User.objects.create_user(username='student', email='123456@qq.com', password='1234')
    #     user.save()
    return render(request, 'login.html')


def admin(request):
    return render(request, 'admin_index.html')

def teacher(request):
    return render(request, 'teacher_index.html')

def student(request):
    return render(request, 'student_index.html')
