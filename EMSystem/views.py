import MySQLdb
from django.shortcuts import render, redirect


# Create your views here.
# 学生信息列表处理函数
def index(request):
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="jwc", charset='utf8')
    with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
        cursor.execute("SELECT id,student_no,student_name FROM student")
        students = cursor.fetchall()
    return render(request, 'index.html', {'students': students})

# 学生信息新增处理函数
def add(request):
    if request.method == 'GET':
        return render(request, 'add.html')
    else:
        student_no = request.POST.get('student_no', '')
        student_name = request.POST.get('student_name', '')
        conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="jwc", charset='utf8')
        with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("INSERT INTO student (student_no,student_name, id) "
                           "values (%s,%s,%s)", [student_no, student_name, '1'])
            conn.commit()
        return redirect('../')

# 学生信息修改处理函数
def edit(request):
    if request.method == 'GET':
        id = request.GET.get("id")
        print(id)
        conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="jwc", charset='utf8')
        with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("SELECT id,student_no,student_name FROM student where id =%s", [id])
            student = cursor.fetchone()
        return render(request, 'edit.html', {'student': student})
    else:
        id = request.POST.get("id")
        print(id)
        student_no = request.POST.get('student_no', '')
        student_name = request.POST.get('student_name', '')
        conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="jwc", charset='utf8')
        with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("UPDATE student set student_no=%s,student_name=%s where id =%s",
                           [student_no, student_name, id])
            conn.commit()
        return redirect('../')

# 学生信息删除处理函数
def delete(request):
    id = request.GET.get("id")
    print(id)
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="jwc", charset='utf8')
    with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
        cursor.execute("DELETE FROM student WHERE id =%s", [id])
        conn.commit()
    return  redirect('../')