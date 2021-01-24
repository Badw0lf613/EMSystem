import MySQLdb
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import S,D,T,C,O,E

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

def get_user_info(request):
    ret={}
    print("request",request.user.username)
    result = S.objects.filter(xh=request.user.username)
    print(result)
    if result.exists():
        ret = {'xh': result[0].xh, 'xm': result[0].xm}
    return ret

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username)
        print(password)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser==1 and user.is_staff==1:           # 管理员
                return HttpResponseRedirect("/admin")
            elif user.is_superuser==0 and user.is_staff==1:          # 老师
                return HttpResponseRedirect("/teacher")
            elif user.is_superuser==0 and user.is_staff==0:          # 学生
                return HttpResponseRedirect("/student")
                # return redirect(reverse('username',kwargs={'username':username}))
        else:
            alert = "用户名或密码错误"
            print(alert)
    # else:
    #     user = User.objects.create_user(username='student', email='123456@qq.com', password='1234')
    #     user.save()
    return render(request, 'login.html')

@login_required
def admin_index(request):
    chosen_xh = request.GET.get('chosen_xh')
    xh = request.POST.get('xh')
    xm = request.POST.get('xm')
    xb = request.POST.get('xb')
    jg = request.POST.get('jg')
    csrq = request.POST.get('csrq')
    sjhm = request.POST.get('sjhm')
    yxh = request.POST.get('yxh')
    students = []                       # 获取当前学生列表
    all_s = S.objects.all()
    for item in all_s:                  # 将对象转换为字典
        attdict = {}
        for field in item._meta.fields:
            name = field.attname
            value = getattr(item, name)
            attdict[name] = value
        students.append(attdict)
    if xh is not None:                  # 如果输入不是空，就创建一个新的学生（还没有做输入正确信息的检查）
        d_item = D.objects.filter(yxh=yxh)
        yxh = getattr(d_item[0], 'yxh')
        new_s = S.objects.create(xh=xh, xm=xm, xb=xb, csrq=csrq, jg=jg, sjhm=sjhm, yxh_id=yxh)
        new_s.save()
        attdict={}
        for field in new_s._meta.fields:      # 向students中添加新的学生
            name = field.attname
            value = getattr(new_s, name)
            attdict[name] = value
        students.append(attdict)
    print(students)
    return render(request, 'admin_index.html', {'students':students, 'chosen_xh':chosen_xh})

@login_required
def delete_student(request):                    # 学生删除
    xh = request.GET.get("xh")
    S.objects.filter(xh=xh).delete()
    return redirect('../')

@login_required
def edit_student(request):
    xh = request.POST.get('xh')
    xm = request.POST.get('xm')
    xb = request.POST.get('xb')
    jg = request.POST.get('jg')
    csrq = request.POST.get('csrq')
    sjhm = request.POST.get('sjhm')
    yxh = request.POST.get('yxh')
    S.objects.filter(xh=xh).update(xh=xh, xm=xm, xb=xb, csrq=csrq, jg=jg, sjhm=sjhm, yxh_id=yxh)
    return redirect('../')

@login_required
def search_student(request):
    keys = {}
    keys['xh'] = request.POST.get('xh')
    keys['xm'] = request.POST.get('xm')
    keys['xb'] = request.POST.get('xb')
    keys['jg'] = request.POST.get('jg')
    keys['csrq'] = request.POST.get('csrq')
    keys['sjhm'] = request.POST.get('sjhm')
    keys['yxh'] = request.POST.get('yxh')
    print(keys)
    result = S.objects.all()
    if keys['xh']:
        result = result.filter(xh=keys['xh'])
    if keys['xm']:
        result = result.filter(xm__contains=keys['xm'])
    if keys['xb']:
        result = result.filter(xb=keys['xb'])
    if keys['jg']:
        result = result.filter(jg=keys['jg'])
    if keys['csrq']:
        result = result.filter(csrq=keys['csrq'])
    if keys['sjhm']:
        result = result.filter(sjhm=keys['sjhm'])
    if keys['yxh']:
        result = result.filter(yxh_id=keys['yxh'])
    students = []
    for item in result:
        students.append(obj2dict(item))
    print(students)
    return render(request, 'admin_index.html', context={'students':students})

def obj2dict(obj):
    res = {}
    for field in obj._meta.fields:
        name = field.attname
        val = getattr(obj, name)
        res[name] = val
    return res

@login_required
def teacher_index(request):
    return render(request, 'teacher_index.html')

@login_required
def student_index(request):
    print(">>>student")
    # print(request.POST.get("context"))
    context = get_user_info(request)
    print(context)
    return render(request, 'student_index.html',context=context)


@login_required
def student_QueryCourse(request):
    print(">>>student_QueryCourse")
    context = get_user_info(request)
    if request.method == 'GET':
        print(">>>GET")
        return render(request, 'student_QueryCourse.html', context=context)
    elif request.method == 'POST':
        print(">>>POST")
        result = C.objects.all()
        # result1 = O.objects.all()
        context['xq'] = request.POST['xq']
        context['kh'] = request.POST['kh']
        context['km'] = request.POST['km']
        context['gh'] = request.POST['gh']
        context['jsmc'] = request.POST['jsmc']
        context['sksj'] = request.POST['sksj']
        flag = 0
        print(context)
        opentable=[] # 开课表，记录工号和上课时间
        teachertable=[] # 教师表，记录工号和姓名
        if context['xq']:
            result = result.filter(xq__contains=context['xq'])
        if context['kh']:
            result = result.filter(kh__startswith=context['kh'])
        if context['km']:
            result = result.filter(km__contains=context['km'])
        if context['gh']:
            print('>>>gh')
            flag = 1
            result = result.filter(id__in=O.objects.filter(gh=context['gh']))
            result1 = O.objects.filter(gh=context['gh']) # 进行提取工号和上课时间
            for item in result1:  # 将对象转换为字典
                content = obj2dict(item)
                opentable.append(content)
                # classtable[]
            print(">>>opentable")
            print(opentable)
            result2 = T.objects.filter(gh=context['gh']) # 进行提取姓名
            for item in result2:  # 将对象转换为字典
                content = obj2dict(item)
                teachertable.append(content)
                # classtable[]
            print(">>>teachertable")
            print(teachertable)
        if context['jsmc']:
            print('>>>jsmc')
            flag = 1
            opentable=[] # 开课表，记录工号和上课时间
            teachertable=[] # 教师表，记录工号和姓名
            result = result.filter(id__in=O.objects.filter(gh__in=T.objects.filter(xm__contains=context['jsmc'])))
            result1 = T.objects.filter(xm__contains=context['jsmc']) # 进行提取工号和教师名称
            for item in result1:  # 将对象转换为字典
                content = obj2dict(item)
                teachertable.append(content)
                # classtable[]
            print(">>>teachertable")
            print(teachertable)
            result2 = O.objects.filter(gh__in=T.objects.filter(xm__contains=context['jsmc'])) # 进行提取工号和上课时间
            for item in result2:  # 将对象转换为字典
                content = obj2dict(item)
                opentable.append(content)
                # classtable[]
            print(">>>opentable")
            print(opentable)
        if context['sksj']:
            print('>>>sksj')
            flag = 1
            opentable=[] # 开课表，记录工号和上课时间
            teachertable=[] # 教师表，记录工号和姓名
            ghlist = []  # 列表记录使用教师名称在教师表查询到的内容，从其中取出工号
            result = result.filter(id__in=O.objects.filter(sksj__contains=context['sksj']))
            result1 = O.objects.filter(sksj__contains=context['sksj']) # 进行提取工号和上课时间
            for item in result1:  # 将对象转换为字典
                content = obj2dict(item)
                opentable.append(content)
                ghlist.append(content['gh_id'])
                # classtable[]
            print(">>>opentable")
            print(opentable)
            print(">>>ghlist")
            print(ghlist)
            result2 = T.objects.filter(gh__in=ghlist)  # 成功
            for item in result2:  # 将对象转换为字典
                content = obj2dict(item)
                teachertable.append(content)
                # classtable[]
            print(">>>teachertable")
            print(teachertable)
        if flag == 0: # 此情况为gh，jsmc，sksj三个字段均为空的情况
            # and len(opentable) == 0 and len(teachertable) == 0
            print(">>>flag == 0")
            opentable=[] # 开课表，记录工号和上课时间
            teachertable=[] # 教师表，记录工号和姓名
            ghlist = []  # 列表记录使用教师名称在教师表查询到的内容，从其中取出工号
            for item in result:  # 将对象转换为字典
                content = obj2dict(item)
                result1 = O.objects.filter(id=content['id'])  # 进行提取工号和上课时间
                for item1 in result1:  # 将对象转换为字典
                    content = obj2dict(item1)
                    opentable.append(content)
                    ghlist.append(content['gh_id'])
                    # classtable[]
                print(">>>opentable")
                print(opentable)
                print(">>>ghlist")
                print(ghlist)
                result2 = T.objects.filter(gh__in=ghlist)  # 成功
                for item2 in result2:  # 将对象转换为字典
                    content = obj2dict(item2)
                    teachertable.append(content)
                    # classtable[]
                print(">>>teachertable")
                print(teachertable)
        idlist = []
        for t1 in opentable:
            idlist.append(t1['id'])
        print(">>>idlist")
        print(idlist)
        classtable = []
        # for kc in result[0]._meta.fields:
        #     # print(kc)
        #     # classtable.append(
        #     #     # {'kh': kc.kh, 'km': kc.km, 'gh': kc.kh.gh, 'jsmc': kc.kh.gh.xm, 'sksj': kc.sksj, 'xq': kc.xq}
        #     #     {'kh': kc.kh, 'km': kc.km, 'xq': kc.xq}
        #     # )
        #     name = kc.attname
        #     value = getattr(result[0], name)
        #     dict1[name] = value
        # i = 0
        for item in result:  # 将对象转换为字典
            content = obj2dict(item)
            # 需要在字典中加入gh，jsmc，sksj
            # print(">>>i")
            # print(i)
            if content['xq'] == '2020-2021学年春季学期':
                ############# 考虑查询结果如何显示 #####################################
                if content['id'] in idlist: # 通过课程id将查询结果中的C表与O表T表对应
                    i = idlist.index(content['id']) # 找出下标对应的课程id
                    content['gh'] = opentable[i]['gh_id']
                    content['sksj'] = opentable[i]['sksj']
                    for item1 in teachertable:
                        if item1['gh'] == opentable[i]['gh_id']:  # 存在一个老师开多门课，此时需找到每门课程对应的工号，再寻找教师名称
                            print(">>>111")
                            print(item1['gh'])
                            content['jsmc'] = item1['xm']
                # i = i + 1
            classtable.append(content)
        print(">>>classtable")
        print(classtable)
        context['classtable'] = classtable
        # classtable1 = []
        # for item in result1:  # 将对象转换为字典
        #     classtable1.append(obj2dict(item))
        # print(">>>")
        # print(classtable1)
        # context['classtable'] = classtable
        return render(request, 'student_QueryCourse.html', context=context)
    return HttpResponseRedirect("/")