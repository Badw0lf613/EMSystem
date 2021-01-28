import MySQLdb
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import S,D,T,C,O,E
import json

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

def get_admin_info(request):
    ret = {}
    print("request", request.user.username)
    result = User.objects.filter(username=request.user.username)
    print(result)
    if result.exists():
        ret['name'] = result[0].first_name+''+result[0].last_name
        ret['yhm'] = result[0].username
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
    print(">>>admin")
    user_info = get_admin_info(request)
    print(user_info)
    xq = request.POST.get('xq')
    print(xq)
    return render(request, 'admin_index.html', {'name': user_info['name'], 'yhm': user_info['yhm'], 'xq': xq})

@login_required
def student_Management(request):
    print(">>>redirect")
    print(request.POST.get('xq'))
    return render(request, 'student_Management.html')

@login_required
def add_student(request):                 # 学生添加
    print("add")
    keys = {}
    keys['xh'] = request.POST.get('xh')
    keys['xm'] = request.POST.get('xm')
    keys['xb'] = request.POST.get('xb')
    keys['jg'] = request.POST.get('jg')
    keys['csrq'] = request.POST.get('csrq')
    keys['sjhm'] = request.POST.get('sjhm')
    keys['yx'] = request.POST.get('yx')

    if keys['xh'] is not None:                  # 向表中插入新学生
        d_item = D.objects.filter(yxm__contains=keys['yx'])
        yxh = getattr(d_item[0], 'yxh')
        new_s = S.objects.create(xh=keys['xh'], xm=keys['xm'], xb=keys['xb'], csrq=keys['csrq'],
                                 jg=keys['jg'], sjhm=keys['sjhm'], yxh_id=yxh)
        new_s.save()

    result = S.objects.all()                   # 插入后重新渲染表中所有的学生
    students = []
    for item in result:
        res = obj2dict(item)
        d = D.objects.all()
        tmp = d.filter(yxh=res['yxh_id'])
        yxm = obj2dict(tmp[0])['yxm']
        del res['yxh_id']
        res['yxm'] = yxm
        students.append(res)
    return render(request, 'student_Management.html', {'students': students, 'search': 1})

@login_required
def delete_student(request):                    # 学生删除
    print(">>>delete")
    xh = request.GET.get("xh")
    S.objects.filter(xh=xh).delete()

    result = S.objects.all()                    # 删除后重新渲染表中所有的学生
    students = []
    for item in result:
        res = obj2dict(item)
        d = D.objects.all()
        tmp = d.filter(yxh=res['yxh_id'])
        yxm = obj2dict(tmp[0])['yxm']
        del res['yxh_id']
        res['yxm'] = yxm
        students.append(res)
    return render(request, 'student_Management.html', {'students': students, 'search': 1})

@login_required
def edit_student(request):                        # 编辑学生信息
    print(">>>edit")
    xh = request.POST.get('xh')
    xm = request.POST.get('xm')
    xb = request.POST.get('xb')
    jg = request.POST.get('jg')
    csrq = request.POST.get('csrq')
    sjhm = request.POST.get('sjhm')
    yx = request.POST.get('yx')

    d = D.objects.all()                           # 更新数据库记录
    tmp = d.filter(yxm__contains=yx)
    yx = obj2dict(tmp[0])['yxh']
    S.objects.filter(xh=xh).update(xh=xh, xm=xm, xb=xb, csrq=csrq, jg=jg, sjhm=sjhm, yxh_id=yx)

    result = S.objects.all()                      # 更新后重新渲染表中所有的记录
    students = []
    for item in result:
        res = obj2dict(item)
        d = D.objects.all()
        tmp = d.filter(yxh=res['yxh_id'])
        yxm = obj2dict(tmp[0])['yxm']
        del res['yxh_id']
        res['yxm'] = yxm
        students.append(res)
    return render(request, 'student_Management.html', {'students': students, 'search': 1})

@login_required
def search_student(request):                     # 搜索学生
    print(">>>search")
    chosen_xh = request.GET.get('chosen_xh')
    if request.method == 'POST':                 # 如果点击查询，则method是post，查询并且渲染符合条件的所有学生
        print("post")
        keys = {}
        keys['xh'] = request.POST.get('xh')
        keys['xm'] = request.POST.get('xm')
        keys['xb'] = request.POST.get('xb')
        keys['jg'] = request.POST.get('jg')
        keys['csrq'] = request.POST.get('csrq')
        keys['sjhm'] = request.POST.get('sjhm')
        keys['yx'] = request.POST.get('yx')
        # print(keys)
        result = S.objects.all()
        all = True
        if keys['xh']:
            result = result.filter(xh=keys['xh'])
            all = False
        if keys['xm']:
            result = result.filter(xm__contains=keys['xm'])
            all = False
        if keys['xb']:
            result = result.filter(xb=keys['xb'])
            all = False
        if keys['jg']:
            result = result.filter(jg=keys['jg'])
            all = False
        if keys['csrq']:
            result = result.filter(csrq=keys['csrq'])
            all = False
        if keys['sjhm']:
            result = result.filter(sjhm=keys['sjhm'])
            all = False
        if keys['yx']:
            d = D.objects.all()
            yx = d.filter(yxm__contains=keys['yx'])
            yxh = obj2dict(yx[0])['yxh']
            result = result.filter(yxh_id=yxh)
            all = False
    else:                                        # 如果点击编辑，则method是get，只显示当前被编辑的一条记录
        print("get")
        result = S.objects.all()
        result = result.filter(xh=chosen_xh)
        all = False

    students = []
    for item in result:
        res = obj2dict(item)
        d = D.objects.all()
        tmp = d.filter(yxh=res['yxh_id'])
        yxm = obj2dict(tmp[0])['yxm']
        del res['yxh_id']
        res['yxm'] = yxm
        students.append(res)

    if all == True:
        search = 1
    else:
        search = None
    # print(students)
    return render(request, 'student_Management.html',
                  context={'students': students, 'chosen_xh': chosen_xh, 'search': search})

def obj2dict(obj):                                        # 数据库记录object转换成python字典
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

@login_required
def student_AddCourse(request):
    print(">>>student_AddCourse")
    context = get_user_info(request)
    if request.method == 'GET': # 首次进入显示
        print(">>>GET")
        result = E.objects.filter(xq='2020-2021学年春季学期', xh=request.user.username)
        opentable = []  # 开课表，记录工号和上课时间
        teachertable = []  # 教师表，记录工号和姓名
        ghlist = []  # 列表记录使用教师名称在教师表查询到的内容，从其中取出工号
        classtable1 = []  # 列表记录课程名称、学分、学时和院系号
        classtable = []
        for item in result:  # 将对象转换为字典
            content = obj2dict(item)
            result1 = O.objects.filter(id=content['id'])  # 进行提取工号和上课时间
            for item1 in result1:  # 将对象转换为字典
                content1 = obj2dict(item1)
                opentable.append(content1)
                ghlist.append(content1['gh_id'])
                # classtable[]
            print(">>>opentable")
            print(opentable)
            print(">>>ghlist")
            print(ghlist)
            result2 = T.objects.filter(gh__in=ghlist)  # 成功
            for item2 in result2:  # 将对象转换为字典
                content2 = obj2dict(item2)
                teachertable.append(content2)
                # classtable[]
            print(">>>teachertable")
            print(teachertable)
            print(content['id'])
            result3 = C.objects.filter(id=content['id']) # 进行提取课程名称学分学时院系号
            for item3 in result3:  # 将对象转换为字典
                content3 = obj2dict(item3)
                classtable1.append(content3)
                # classtable[]
            print(">>>classtable1")
            print(classtable1)
        idlist = [] # 列表记录O表课程id
        for t1 in opentable:
            idlist.append(t1['id'])
        print(">>>idlist")
        print(idlist)
        for item in result:  # 将对象转换为字典
            content = obj2dict(item)
            ############# 考虑查询结果如何显示 #####################################
            if content['id'] in idlist: # 通过课程id将查询结果中的C表与O表T表对应
                i = idlist.index(content['id']) # 找出下标对应的课程id
                content['gh'] = opentable[i]['gh_id']
                content['sksj'] = opentable[i]['sksj']
                content['km'] = classtable1[i]['km']
                content['xf'] = classtable1[i]['xf']
                content['xs'] = classtable1[i]['xs']
                content['yxh'] = classtable1[i]['yxh_id']
                for item1 in teachertable:
                    if item1['gh'] == opentable[i]['gh_id']:  # 存在一个老师开多门课，此时需找到每门课程对应的工号，再寻找教师名称
                        print(">>>111")
                        print(item1['gh'])
                        content['jsmc'] = item1['xm']
            classtable.append(content)
        print(">>>classtable")
        print(classtable)
        context['classtable'] = classtable
        return render(request, 'student_AddCourse.html', context=context)
    elif request.method == 'POST': # 表单选课
        print(">>>POST")
        msg = [] # 列表存储选课成功/失败信息的整条记录
        for i in range(1, 5):
            m = {}  # 临时字典存储课号，工号和结果
            context['kh' + str(i)] = request.POST['kh' + str(i)]
            context['gh' + str(i)] = request.POST['gh' + str(i)]
            if len(context['kh' + str(i)]) and len(context['gh' + str(i)]): # 两个字段均非空，开始进行查询
                result = O.objects.filter(kh=context['kh' + str(i)], gh=context['gh' + str(i)])
                if not result.exists():
                    m['kh'] = context['kh' + str(i)]
                    m['gh'] = context['gh' + str(i)]
                    m['res'] = '选课失败：不存在此门课程'
                    msg.append(m)
                    continue
                # 可能出现的情况：如gh，E表的外键，T表的主键，需要使用另一张表的原型
                result_id = []
                for item in result:
                    content = obj2dict(item)
                    result_id.append(content)
                item = E.objects.create(
                    id=result_id[0]['id'],
                    xn='2020-2021学年',
                    xq='2020-2021学年春季学期',
                    gh=T.objects.filter(gh=context['gh' + str(i)])[0], # E表的外键，T表的主键，需要使用另一张表的原型
                    # gh=context['gh' + str(i)],
                    # kh=O.objects.filter(xq='2019-2020学年冬季学期', kh=context['kh' + str(i)], gh=T.objects.filter(gh=gh)[0])[0],
                    kh=context['kh' + str(i)],
                    xh=S.objects.filter(xh=request.user.username)[0]
                )
                # item = E(
                #     xn='2020-2021学年',
                #     xq='2020-2021学年春季学期',
                #     gh=context['gh' + str(i)],
                #     kh=context['kh' + str(i)],
                #     xh=request.user.username
                # )
                print(">>>item")
                print(item)
                item.save()
                m['kh'] = context['kh' + str(i)]
                m['gh'] = context['gh' + str(i)]
                m['res'] = '选课成功'
                msg.append(m)
            elif len(context['kh' + str(i)]) or len(context['gh' + str(i)]):
                m['kh'] = context['kh' + str(i)]
                m['gh'] = context['gh' + str(i)]
                m['res'] = '选课失败：信息未填写完整'
                msg.append(m)
        context['msg'] = msg
        result = E.objects.filter(xq='2020-2021学年春季学期', xh=request.user.username)
        opentable = []  # 开课表，记录工号和上课时间
        teachertable = []  # 教师表，记录工号和姓名
        ghlist = []  # 列表记录使用教师名称在教师表查询到的内容，从其中取出工号
        classtable1 = []  # 列表记录课程名称、学分、学时和院系号
        classtable = []
        for item in result:  # 将对象转换为字典
            content = obj2dict(item)
            result1 = O.objects.filter(id=content['id'])  # 进行提取工号和上课时间
            for item1 in result1:  # 将对象转换为字典
                content1 = obj2dict(item1)
                opentable.append(content1)
                ghlist.append(content1['gh_id'])
                # classtable[]
            print(">>>opentable")
            print(opentable)
            print(">>>ghlist")
            print(ghlist)
            result2 = T.objects.filter(gh__in=ghlist)  # 成功
            for item2 in result2:  # 将对象转换为字典
                content2 = obj2dict(item2)
                teachertable.append(content2)
                # classtable[]
            print(">>>teachertable")
            print(teachertable)
            print(content['id'])
            result3 = C.objects.filter(id=content['id'])  # 进行提取课程名称学分学时院系号
            for item3 in result3:  # 将对象转换为字典
                content3 = obj2dict(item3)
                classtable1.append(content3)
                # classtable[]
            print(">>>classtable1")
            print(classtable1)
        idlist = []  # 列表记录O表课程id
        for t1 in opentable:
            idlist.append(t1['id'])
        print(">>>idlist")
        print(idlist)
        for item in result:  # 将对象转换为字典
            content = obj2dict(item)
            ############# 考虑查询结果如何显示 #####################################
            if content['id'] in idlist:  # 通过课程id将查询结果中的C表与O表T表对应
                i = idlist.index(content['id'])  # 找出下标对应的课程id
                content['gh'] = opentable[i]['gh_id']
                content['sksj'] = opentable[i]['sksj']
                content['km'] = classtable1[i]['km']
                content['xf'] = classtable1[i]['xf']
                content['xs'] = classtable1[i]['xs']
                content['yxh'] = classtable1[i]['yxh_id']
                for item1 in teachertable:
                    if item1['gh'] == opentable[i]['gh_id']:  # 存在一个老师开多门课，此时需找到每门课程对应的工号，再寻找教师名称
                        print(">>>111")
                        print(item1['gh'])
                        content['jsmc'] = item1['xm']
            classtable.append(content)
        print(">>>classtable")
        print(classtable)
        context['classtable'] = classtable
        print(">>>context")
        print(context)
        return render(request, 'student_AddCourse.html', context=context)

@login_required
def student_DeleteCourse(request):
    print(">>>student_DeleteCourse")
    context = get_user_info(request)
    if request.method == 'GET': # 首次进入显示
        print(">>>GET")
        result = E.objects.filter(xq='2020-2021学年春季学期', xh=request.user.username)
        opentable = []  # 开课表，记录工号和上课时间
        teachertable = []  # 教师表，记录工号和姓名
        ghlist = []  # 列表记录使用教师名称在教师表查询到的内容，从其中取出工号
        classtable1 = []  # 列表记录课程名称、学分、学时和院系号
        classtable = []
        for item in result:  # 将对象转换为字典
            content = obj2dict(item)
            result1 = O.objects.filter(id=content['id'])  # 进行提取工号和上课时间
            for item1 in result1:  # 将对象转换为字典
                content1 = obj2dict(item1)
                opentable.append(content1)
                ghlist.append(content1['gh_id'])
                # classtable[]
            print(">>>opentable")
            print(opentable)
            print(">>>ghlist")
            print(ghlist)
            result2 = T.objects.filter(gh__in=ghlist)  # 成功
            for item2 in result2:  # 将对象转换为字典
                content2 = obj2dict(item2)
                teachertable.append(content2)
                # classtable[]
            print(">>>teachertable")
            print(teachertable)
            print(content['id'])
            result3 = C.objects.filter(id=content['id']) # 进行提取课程名称学分学时院系号
            for item3 in result3:  # 将对象转换为字典
                content3 = obj2dict(item3)
                classtable1.append(content3)
                # classtable[]
            print(">>>classtable1")
            print(classtable1)
        idlist = [] # 列表记录O表课程id
        for t1 in opentable:
            idlist.append(t1['id'])
        print(">>>idlist")
        print(idlist)
        for item in result:  # 将对象转换为字典
            content = obj2dict(item)
            ############# 考虑查询结果如何显示 #####################################
            if content['id'] in idlist: # 通过课程id将查询结果中的C表与O表T表对应
                i = idlist.index(content['id']) # 找出下标对应的课程id
                content['gh'] = opentable[i]['gh_id']
                content['sksj'] = opentable[i]['sksj']
                content['km'] = classtable1[i]['km']
                content['xf'] = classtable1[i]['xf']
                content['xs'] = classtable1[i]['xs']
                content['yxh'] = classtable1[i]['yxh_id']
                for item1 in teachertable:
                    if item1['gh'] == opentable[i]['gh_id']:  # 存在一个老师开多门课，此时需找到每门课程对应的工号，再寻找教师名称
                        print(">>>111")
                        print(item1['gh'])
                        content['jsmc'] = item1['xm']
            classtable.append(content)
        print(">>>classtable")
        print(classtable)
        context['classtable'] = classtable
        return render(request, 'student_DeleteCourse.html', context=context)
    elif request.method == 'POST': # 表单退课
        print(">>>POST")
        context['kh_array'] = request.POST.get('kh_array')
        context['gh_array'] = request.POST.get('gh_array')
        print(context['kh_array'])
        print(context['gh_array'])
        return HttpResponse(json.dumps({
            "status": status,
            "result": result
        }))
        # return render(request, 'student_DeleteCourse.html', context=context)

@login_required
def student_QueryGrades(request):
    print(">>>student_QueryGrades")
    context = get_user_info(request)
    if request.method == 'GET':
        print(">>>GET")
        return render(request, 'student_QueryGrades.html', context=context)

@login_required
def student_CourseTable(request):
    print(">>>student_CourseTable")
    context = get_user_info(request)
    if request.method == 'GET':
        print(">>>GET")
        return render(request, 'student_CourseTable.html', context=context)

@login_required
def testcheckbox(request):
    print(">>>testcheckbox")
    context = get_user_info(request)
    if request.method == 'GET':
        print(">>>GET")
        return render(request, 'testcheckbox.html', context=context)

@login_required
def testcheckbox2(request):
    print(">>>testcheckbox2")
    context = get_user_info(request)
    if request.method == 'GET':
        print(">>>GET")
        return render(request, 'testcheckbox2.html', context=context)