import MySQLdb
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import S,D,T,C,O,E,TEMP
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json
import random
from math import floor
from django.db.models import Q
import numpy as np
import MySQLdb


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

dt = [['一', '1-2'], ['一', '3-4'], ['一', '5-6'], ['一', '7-8'], ['一', '9-10'], ['一', '11-13'],
      ['二', '1-2'], ['二', '3-4'], ['二', '5-6'], ['二', '7-8'], ['二', '9-10'], ['二', '11-13'],
      ['三', '1-2'], ['三', '3-4'], ['三', '5-6'], ['三', '7-8'], ['三', '9-10'], ['三', '11-13'],
      ['四', '1-2'], ['四', '3-4'], ['四', '5-6'], ['四', '7-8'], ['四', '9-10'], ['四', '11-13'],
      ['五', '1-2'], ['五', '3-4'], ['五', '5-6'], ['五', '7-8'], ['五', '9-10'], ['五', '11-13']]

def get_user_info(request):
    ret={}
    print("request",request.user.username)
    result = S.objects.filter(xh=request.user.username)
    if result.exists():
        jj = round(result[0].jj + 0.00001, 2)  # 四舍五入
        ret = {'xh': result[0].xh, 'xm': result[0].xm, 'jj': jj, 'xfh': result[0].xfh}
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
    return render(request, 'testlogin.html')

@login_required
def admin_index(request):
    global dt
    print(">>>admin")
    user_info = get_admin_info(request)
    print(user_info)
    xq = settings.XQ

    # print(xq)
    # print(settings.XQ)
    return render(request, 'admin_index.html', {'name': user_info['name'], 'yhm': user_info['yhm'], 'xq': xq})

@login_required
def update_xq(request):
    print(">>>update")
    xq = request.POST.get('xq')
    settings.XQ = xq
    if O.objects.all().count() != 0:          # 如果O表不为空，则首先清空O表
        O.objects.all().delete()
    res = C.objects.all()
    res = res.filter(xq=xq)

    for item in res:
        dt_temp = dt[:]
        item_dict = obj2dict(item)
        kh = item_dict['kh']
        xf = item_dict['xf']
        print(kh)
        temp = TEMP.objects.all()

        if temp.filter(km=kh).count() != 0:               # 如果需要有教师认领课程，那么就把课程分配给他
            ghs = []
            res = temp.filter(km=kh)
            for item in res:
                gh = obj2dict(item)['gh']
                ghs.append(gh)
            for gh in ghs:
                sksj = get_sksj(gh, xf, dt_temp)
                t = T.objects.get(gh=gh)
                # gh = T.objects.filter(gh=['gh' + str(i)])[0],  # E表的外键，T表的主键，需要使用另一张表的原型
                print("C.objects.filter(kh=kh)[0]", C.objects.filter(kh=kh)[0])
                cid = C.objects.filter(kh=kh)[0]  # 课程序号
                new_o = O.objects.create(kh=kh, gh=t, sksj=sksj, cid=cid)

        else:                                             # 如果还没有教师认领课程，那么久随机分配一个本院系的老师上这门课
            yxh = obj2dict(item)['yxh_id']
            t = T.objects.filter(yxh_id=yxh)
            num = t.count()
            idx = random.randint(0, num-1)
            gh = getattr(t[idx], 'gh')
            sksj = get_sksj(gh, xf, dt_temp)              # 上课时间也需要重新分配
            # gh = T.objects.filter(gh=['gh' + str(i)])[0],  # E表的外键，T表的主键，需要使用另一张表的原型
            print("C.objects.filter(kh=kh)[0]", C.objects.filter(kh=kh)[0])
            cid = C.objects.filter(kh=kh)[0]  # 课程序号
            new_o = O.objects.create(kh=kh, gh=t[idx], sksj=sksj, cid=cid)
        new_o.save()

    return redirect("admin")

def get_sksj(gh, xf, dt):
    dt_temp = dt[:]
    old_times = []
    o_item = O.objects.filter(gh=gh)
    for o in o_item:
        sj_str = obj2dict(o)['sksj']
        sj_str = sj_str.strip()
        sj = sj_str.split(' ')
        for s in sj:
            old_times.append(s.split(':'))
    print(old_times)
    for tt in old_times:
        dt_temp.remove(tt)
        print(dt_temp)
    l = len(dt_temp)
    print("xf", xf)
    id = random.sample(range(0, l - 1), floor((int(xf) + 1) / 2))
    sksj = ''  # 可能还需要根据他已有的上课时间来分配新课程的时间
    for i in id:
        sksj = sksj + str(dt_temp[i][0]) + ":" + str(dt_temp[i][1])
        if i != len(id) - 1:
            sksj = sksj + " "
    return sksj

@login_required
def Management(request, type):
    print(">>>management")
    xq = settings.XQ
    print(xq)
    print(type)
    return render(request, 'Management.html', {'xq': xq, 'type': type})

@login_required
def add(request, type):                 # 添加
    global dt
    print(">>>add")
    keys = {}
    if type == 1:                          # 添加学生
        keys['xh'] = request.POST.get('xh')
        keys['xm'] = request.POST.get('xm')
        keys['xb'] = request.POST.get('xb')
        keys['jg'] = request.POST.get('jg')
        keys['csrq'] = request.POST.get('csrq')
        keys['sjhm'] = request.POST.get('sjhm')
        keys['yx'] = request.POST.get('yx')

        if User.objects.filter(username=keys['xh']).count() == 0:
            user = User.objects.create_user(username=keys['xh'])      # 向S表插入学生的同时，也向User表中插入学生
            user.is_staff = False
            user.is_superuser = False
            user.set_password(keys['xh'])                             # 设置初始密码为学号
            user.save()

        if keys['xh'] is not None:                  # 向表中插入新学生
            d_item = D.objects.filter(yxm__contains=keys['yx'])
            yxh = getattr(d_item[0], 'yxh')
            new_s = S.objects.create(xh=keys['xh'], xm=keys['xm'], xb=keys['xb'], csrq=keys['csrq'],
                                     jg=keys['jg'], sjhm=keys['sjhm'], yxh_id=yxh)
            new_s.save()

        return redirect("search", type=1, flag=1)

    elif type == 2:                              # 添加老师
        keys['gh'] = request.POST.get('gh')
        keys['xm'] = request.POST.get('xm')
        keys['xb'] = request.POST.get('xb')
        keys['csrq'] = request.POST.get('csrq')
        keys['xl'] = request.POST.get('xl')
        keys['gz'] = request.POST.get('gz')
        keys['yx'] = request.POST.get('yx')
        keys['pf'] = request.POST.get('pf')

        if User.objects.filter(username=keys['gh']).count() == 0:
            user = User.objects.create_user(username=keys['gh'])      # 向T表插入老师的同时，也向User表中插入老师
            user.is_staff = True
            user.is_superuser = False
            user.set_password(keys['gh'])                             # 设置初始密码为工号
            user.save()

        if keys['gh'] is not None:                # 向表中插入新老师
            d_item = D.objects.filter(yxm__contains=keys['yx'])
            yxh = getattr(d_item[0], 'yxh')
            new_t = T.objects.create(gh=keys['gh'], xm=keys['xm'], xb=keys['xb'], csrq=keys['csrq'], xl=keys['xl'],
                                     gz=keys['gz'], yxh_id=yxh, pf=keys['pf'])
            new_t.save()

        return redirect("search", type=2, flag=1)

    elif type == 3:                              # 添加院系
        keys['yxh'] = request.POST.get('yxh')
        keys['yxm'] = request.POST.get('yxm')
        keys['lxdh'] = request.POST.get('lxdh')
        keys['dz'] = request.POST.get('dz')

        if keys['yxh'] is not None:             # 向表中插入新院系
            new_d = D.objects.create(yxh=keys['yxh'], yxm=keys['yxm'], lxdh=keys['lxdh'], dz=keys['dz'])
            new_d.save()
        return redirect("search", type=3, flag=1)

    elif type == 4:
        keys['xq'] = request.POST.get('xq')
        keys['kh'] = request.POST.get('kh')
        keys['km'] = request.POST.get('km')
        keys['xf'] = request.POST.get('xf')
        keys['xs'] = request.POST.get('xs')
        keys['yx'] = request.POST.get('yx')

        if keys['km'] and keys['xf'] and keys['xs'] and keys['yx']:
            d_item = D.objects.filter(yxm__contains=keys['yx'])
            yxh = getattr(d_item[0], 'yxh')
            new_c = C.objects.create(xq=keys['xq'], kh=keys['kh'], km=keys['km'], xf=keys['xf'],
                                     xs=keys['xs'], yxh_id=yxh)
            new_c.save()
            if keys['xq'] == settings.XQ:
                yxh = obj2dict(new_c)['yxh_id']
                t = T.objects.filter(yxh_id=yxh)
                num = t.count()
                idx = random.randint(0, num - 1)
                gh = getattr(t[idx], 'gh')
                sksj = get_sksj(gh, keys['xf'], dt[:])               # 上课时间也需要重新分配
                cid = C.objects.filter(kh=keys['kh'])[0]  # 课程序号
                new_o = O.objects.create(kh=keys['kh'], gh=t[idx], sksj=sksj, cid=cid)

        return redirect("search", type=4, flag=1)


@login_required
@csrf_exempt
def delete(request, type):                    # 删除
    print(">>>delete")

    if type == 1:                            # 学生删除
        data = json.loads(request.body.decode('utf-8'))
        xh = data.get('data_array')
        print(xh)
        for num in xh[:]:
            print(num)
            S.objects.filter(xh=num).delete()
            if User.objects.filter(username=num).count() != 0:
                User.objects.filter(username=num).delete()   # 从用户表里面也删除这个学生

        return redirect("search", type=1, flag=1)

    elif type == 2:                           # 老师删除
        data = json.loads(request.body.decode('utf-8'))
        gh = data.get('data_array')
        print(gh)
        for num in gh[:]:
            T.objects.filter(gh=num).delete()
            if User.objects.filter(username=num).count() != 0:
                User.objects.filter(username__exact=num).delete()  # 从用户表里面也删除这个老师

        return redirect("search", type=2, flag=1)

    elif type == 3:
        data = json.loads(request.body.decode('utf-8'))
        yxh = data.get('data_array')
        print(yxh)
        for num in yxh[:]:
            print(num)
            D.objects.filter(yxh=num).delete()

        return redirect("search", type=3, flag=1)

    elif type == 4:
        data = json.loads(request.body.decode('utf-8'))
        xq = data.get('data_array')
        kh = data.get('kh_array')
        js = data.get('js_array')
        print(xq)
        print(kh)
        print(js)
        for i, j, k in zip(xq[:], kh[:], js[:]):
            if O.objects.filter(kh=j).count() <= 1:
                C.objects.filter(xq=i, kh=j).delete()
            if i == settings.XQ:
                t = T.objects.filter(xm=k)
                gh = getattr(t[0], 'gh')
                O.objects.filter(kh=j, gh=gh).delete()

        return redirect("search", type=4, flag=1)

@login_required
def edit(request, type):                        # 编辑信息
    global dt
    print(">>>edit")
    if type == 1:                             # 编辑学生
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

        return redirect("search", type=1, flag=1)

    elif type == 2:                            # 编辑老师
        gh = request.POST.get('gh')
        xm = request.POST.get('xm')
        xb = request.POST.get('xb')
        csrq = request.POST.get('csrq')
        xl = request.POST.get('xl')
        gz = request.POST.get('gz')
        yx = request.POST.get('yxm')
        pf = request.POST.get('pf')

        d = D.objects.all()                                  # 更新数据库记录
        tmp = d.filter(yxm__contains=yx)
        yx = obj2dict(tmp[0])['yxh']
        T.objects.filter(gh=gh).update(gh=gh, xm=xm, xb=xb, csrq=csrq, xl=xl, gz=gz, yxh_id=yx, pf=pf)

        return redirect("search", type=2, flag=1)

    elif type == 3:
        yxh = request.POST.get('yxh')
        yxm = request.POST.get('yxm')
        lxdh = request.POST.get('lxdh')
        dz = request.POST.get('dz')
        D.objects.filter(yxh=yxh).update(yxh=yxh, yxm=yxm, lxdh=lxdh, dz=dz)
        return redirect("search", type=3, flag=1)

    elif type == 4:
        xq = request.POST.get('xq')
        kh = request.POST.get('kh')
        km = request.POST.get('km')
        js = request.POST.get('js')
        sksj = request.POST.get('sksj')
        xf = request.POST.get('xf')
        xs = request.POST.get('xs')
        yx = request.POST.get('yx')
        if xq == settings.XQ:
            q = Q()
            q.connector = 'AND'
            q.children.append(('kh', kh))
            q.children.append(('sksj', sksj))
            temp_o = O.objects.get(q)
            old_gh = getattr(temp_o, 'gh')
            old_gh = getattr(old_gh, 'gh')
            t_obj = T.objects.get(xm=js)
            gh = getattr(t_obj, 'gh')
            if old_gh != gh:
                sksj = get_sksj(gh, xf, dt[:])
            d = D.objects.all()                                                                    # 更新数据库记录
            tmp = d.filter(yxm__contains=yx)
            yx = obj2dict(tmp[0])['yxh']
            C.objects.filter(xq=xq, kh=kh).update(xq=xq, kh=kh, km=km, xf=xf, xs=int(xf)*10, yxh_id=yx)
            O.objects.filter(kh=kh, gh=old_gh).update(kh=kh, gh=gh, sksj=sksj)

        else:
            d = D.objects.all()  # 更新数据库记录
            tmp = d.filter(yxm__contains=yx)
            yx = obj2dict(tmp[0])['yxh']
            C.objects.filter(xq=xq, kh=kh).update(xq=xq, kh=kh, km=km, xf=xf, xs=int(xf) * 10, yxh_id=yx)

        return redirect("search", type=4, flag=1)

@login_required
def search(request, type, flag=None):                     # 搜索学生,flag是否为None用来判别是否需要显示所有学生
    print(">>>search")
    xq = settings.XQ
    # print(type)
    if type == 1:
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
        else:                                              # 如果method是get则直接显示所有记录
            print("get")
            result = S.objects.all()
            all =  True

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
        print(students)
        return render(request, 'Management.html',
                      context={'students': students, 'chosen_xh': chosen_xh, 'search': search, 'type': type, 'xq':xq})

    elif type == 2:
        chosen_gh = request.GET.get('chosen_gh')
        if request.method == 'POST':  # 如果点击查询，则method是post，查询并且渲染符合条件的所有学生
            print("post")
            keys = {}
            keys['gh'] = request.POST.get('gh')
            keys['xm'] = request.POST.get('xm')
            keys['xb'] = request.POST.get('xb')
            keys['csrq'] = request.POST.get('csrq')
            keys['xl'] = request.POST.get('xl')
            keys['yx'] = request.POST.get('yx')

            # print(keys)
            result = T.objects.all()
            all = True
            if keys['gh']:
                result = result.filter(xh=keys['gh'])
                all = False
            if keys['xm']:
                result = result.filter(xm__contains=keys['xm'])
                all = False
            if keys['xb']:
                result = result.filter(xb=keys['xb'])
                all = False
            if keys['csrq']:
                result = result.filter(csrq=keys['csrq'])
                all = False
            if keys['xl']:
                result = result.filter(sjhm=keys['xl'])
                all = False
            if keys['yx']:
                d = D.objects.all()
                yx = d.filter(yxm__contains=keys['yx'])
                yxh = obj2dict(yx[0])['yxh']
                result = result.filter(yxh_id=yxh)
                all = False
        else:  # 如果method是get则直接显示所有记录
            print("get")
            result = T.objects.all()
            all = True

        teachers = []
        for item in result:
            res = obj2dict(item)
            d = D.objects.all()
            tmp = d.filter(yxh=res['yxh_id'])
            yxm = obj2dict(tmp[0])['yxm']
            del res['yxh_id']
            res['yxm'] = yxm
            teachers.append(res)

        if all == True:
            search = 1
        else:
            search = None
        print(teachers)
        return render(request, 'Management.html',
                      context={'teachers': teachers, 'chosen_gh': chosen_gh, 'search': search, 'type': type, 'xq':xq})

    elif type == 3:
        chosen_yxh = request.GET.get('chosen_yxh')
        if request.method == 'POST':  # 如果点击查询，则method是post，查询并且渲染符合条件的所有学生
            print("post")
            keys = {}
            keys['yxh'] = request.POST.get('yxh')
            keys['yxm'] = request.POST.get('yxm')
            keys['dz'] = request.POST.get('dz')

            # print(keys)
            result = D.objects.all()
            all = True
            if keys['yxh']:
                result = result.filter(yxh=keys['yxh'])
                all = False
            if keys['yxm']:
                result = result.filter(yxm__contains=keys['yxm'])
                all = False
            if keys['dz']:
                result = result.filter(dz=keys['dz'])
                all = False

        else:  # 如果method是get则直接显示所有记录
            print("get")
            result = D.objects.all()
            all = True

        departments = []
        for item in result:
            res = obj2dict(item)
            departments.append(res)

        if all == True:
            search = 1
        else:
            search = None
        print(departments)
        return render(request, 'Management.html',
                      context={'departments': departments, 'chosen_yxh': chosen_yxh, 'search': search, 'type': type, 'xq':xq})

    if type == 4:
        number = TEMP.objects.filter(stats=0).count()
        chosen_kh = request.GET.get('chosen_kh')
        chosen_xq = request.GET.get('chosen_xq')
        chosen_js = request.GET.get('chosen_js')
        print(chosen_kh)
        print(chosen_xq)
        if chosen_js == '':
            print(chosen_js)
        keys = {}
        keys['xq'] = request.POST.get('xq')
        keys['kh'] = request.POST.get('kh')
        keys['km'] = request.POST.get('km')
        keys['js'] = request.POST.get('js')
        keys['sksj'] = request.POST.get('sksj')
        keys['xf'] = request.POST.get('xf')
        keys['xs'] = request.POST.get('xs')
        keys['yx'] = request.POST.get('yx')
        print(keys)

        if request.method == 'POST':                 # 如果点击查询，则method是post，查询并且渲染符合条件的所有学生
            print("post")
            result = C.objects.all()
            all = True

            if keys['xq']:
                result = result.filter(xq=keys['xq'])
                all = False
            if keys['kh']:
                result = result.filter(kh=keys['kh'])
                all = False
            if keys['km']:
                result = result.filter(km__contains=keys['km'])
                all = False
            if keys['js']:
                result_t = T.objects.get(xm=keys['js'])
                gh = getattr(result_t, 'gh')
                result_o = O.objects.all()
                result_o = result_o.filter(gh_id=gh)
                khs = []
                for item in result_o:
                    khs.append(getattr(item, 'kh'))
                q = Q()
                q.connector = 'OR'
                for k in khs:
                    q.children.append(('kh', k))
                if len(q) == 0:
                    res_temp = C.objects.none()
                else:
                    res_temp = C.objects.filter(q)
                result = result & res_temp
                all = False

            if keys['sksj']:
                result_o = O.objects.all()
                result_o = result_o.filter(sksj__contains=keys['sksj'])
                kh = []
                for item in result_o:
                    kh.append(getattr(item, 'kh'))
                q = Q()
                q.connector = 'OR'
                for k in kh:
                    q.children.append(('kh', k))

                if len(q) == 0:
                    res_temp = C.objects.none()
                else:
                    res_temp = C.objects.filter(q)
                result = res_temp & result
                all = False

            if keys['xf']:
                result = result.filter(xf=keys['xf'])
                all = False
            if keys['xs']:
                result = result.filter(xs=keys['xs'])
                all = False

            if keys['yx']:
                d = D.objects.all()
                yx = d.filter(yxm__contains=keys['yx'])
                yxh = obj2dict(yx[0])['yxh']
                result = result.filter(yxh_id=yxh)
                all = False
        else:                                              # 如果method是get则直接显示所有记录
            print("get")
            result = C.objects.all()
            all = True

        courses = []
        for item in result:
            res = obj2dict(item)
            d = D.objects.all()
            tmp_d = d.filter(yxh=res['yxh_id'])
            yxm = obj2dict(tmp_d[0])['yxm']
            del res['yxh_id']
            res['yxm'] = yxm

            o = O.objects.all()
            tmp_o = o.filter(kh=res['kh'])
            if tmp_o.count() > 0 and res['xq'] == xq:
                for i in range(tmp_o.count()):
                    tmp = res.copy()
                    gh_obj = getattr(tmp_o[i], 'gh')
                    tmp['js'] = getattr(gh_obj, 'xm')
                    tmp['sksj'] = getattr(tmp_o[i], 'sksj')
                    if tmp['js'] == keys['js'] and keys['js'] != '' or keys['js'] == '' or keys['js'] is None:
                        courses.append(tmp)
            elif keys['js'] == '' or keys['js'] is None:
                res['js'] = ''
                res['sksj'] = ''
                courses.append(res)

        if all == True:
            search = 1
        else:
            search = None
        print(courses)
        return render(request, 'Management.html',
                      context={'courses': courses, 'chosen_xq': chosen_xq ,'chosen_kh': chosen_kh, 'chosen_js': chosen_js,
                               'search': search, 'type': type, 'xq':xq, 'number':number})

def apply(request, type):                                # 审核课程信息
    xq = settings.XQ
    res = TEMP.objects.filter(stats=0)
    courses = []
    for item in res:
        item_dict = obj2dict(item)
        d = D.objects.all()
        tmp = d.filter(yxh=item_dict['yxh_id'])
        yxm = obj2dict(tmp[0])['yxm']
        del item_dict['yxh_id']
        item_dict['yxm'] = yxm

        t = T.objects.filter(gh=item_dict['gh'])
        js = getattr(t[0], 'xm')
        del item_dict['gh']
        item_dict['js']=js
        courses.append(item_dict)
    return render(request, 'deal_with_apply.html',context={'xq':xq,'courses':courses})


@login_required
@csrf_exempt
def apply_commit(request, type):
    print(">>>commit")
    mysqlCon = MySQLdb.connect(user='root',passwd='1234',db='jwc',port=3306,charset='utf8')  # 连接数据库
    mysqlCur = mysqlCon.cursor()
    data = json.loads(request.body.decode('utf-8'))
    xqs = data.get('xq_array')
    kms = data.get('km_array')
    xfs = data.get('xf_array')
    yxs = data.get('yx_array')
    print(xqs)
    print(kms)
    print(xfs)
    print(yxs)
    for xq, km, xf, yx in zip(xqs, kms, xfs, yxs):
        # TEMP.objects.filter(xq=xq, km=km).update(stats=3)
        # rand = random.sample(['1','2','3','4','5','6','7','8','9','0'], 6)
        # kh = '08'
        # for r in rand:
        #     kh = kh + r
        # d = D.objects.filter(yxm=yx)
        # yxh = getattr(d[0], 'yxh')
        # new_c = C.objects.create(xq=xq,kh=kh,km=km,xf=int(xf),xs=int(xf)*10,yxh_id=yxh)
        print(xq, km, int(xf), yx)
        mysqlCur.callproc('commit', (xq, km, int(xf), yx))              # 调用存储过程
        mysqlCon.commit()
        print(mysqlCur.fetchall())

    mysqlCur.close()
    mysqlCon.close()
    return redirect("apply", 4)

@login_required
@csrf_exempt
def apply_refuse(request, type):
    print(">>>refuse")
    mysqlCon = MySQLdb.connect(user='root',passwd='1234',db='jwc',port=3306,charset='utf8')  # 连接数据库
    mysqlCur = mysqlCon.cursor()
    data = json.loads(request.body.decode('utf-8'))
    xqs = data.get('xq_array')
    kms = data.get('km_array')
    jss = data.get('js_array')
    print(xqs)
    print(kms)
    print(jss)
    for xq, km, js in zip(xqs, kms, jss):
        mysqlCur.callproc('refuse', (xq, km, js))  # 调用存储过程
        mysqlCon.commit()
        print(mysqlCur.fetchall())
    return redirect("apply", 4)

def obj2dict(obj):                                           # 数据库记录object转换成python字典
    res = {}
    for field in obj._meta.fields:
        name = field.attname
        val = getattr(obj, name)
        res[name] = val
    return res


@login_required
def student_index(request):
    print(">>>student")
    # print(request.POST.get("context"))
    context = get_user_info(request)
    context['xq_now'] = settings.XQ
    print(context)
    return render(request, 'student_index.html',context=context)

@login_required
def student_QueryCourse(request):
    print(">>>student_QueryCourse")
    context = get_user_info(request)
    context['xq_now'] = settings.XQ
    print("settings.XQ",settings.XQ)
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
        print(">>>context",context)
        if context['xq']:
            print('>>>xq')
            result = result.filter(xq__contains=context['xq'])
        if context['kh']:
            print('>>>kh')
            result = result.filter(kh__startswith=context['kh'])
        if context['km']:
            print('>>>km')
            result = result.filter(km__contains=context['km'])
        if context['gh']:
            print('>>>gh')
            resultO = O.objects.filter(gh=context['gh'])
            khlist = [] # 列表用于储存课号
            for item in resultO:
                content = obj2dict(item)
                print(">>>item content", content)
                khlist.append(content['kh'])
            q = Q()
            q.connector = 'OR'
            for i in khlist:
                print(">>>i",i)
                q.children.append(('kh', i))
            if len(q) == 0:
                restmp = C.objects.none()
            else:
                restmp = C.objects.filter(q)
            result = result & restmp
        if context['jsmc']:
            print('>>>jsmc')
            resultT = T.objects.filter(xm__contains=context['jsmc'])
            ghlist = []  # 列表用于储存工号
            khlist = []  # 列表用于储存课号
            for item in resultT:
                content = obj2dict(item)
                print(">>>resultT item content", content)
                ghlist.append(content['gh'])
                print(">>>content['gh']", content['gh'])
                resultO = O.objects.filter(gh=content['gh'])
                for itemO in resultO:
                    contentO = obj2dict(itemO)
                    print(">>>resultO item contentO", contentO)
                    khlist.append(contentO['kh'])
            print(">>>ghlist",ghlist)
            print(">>>khlist",khlist)
            q = Q()
            q.connector = 'OR'
            for i in khlist:
                q.children.append(('kh', i))
            if len(q) == 0:
                restmp = C.objects.none()
            else:
                restmp = C.objects.filter(q)
            result = result & restmp
        if context['sksj']:
            print('>>>sksj')
            resultO = O.objects.filter(sksj__contains=context['sksj'])
            khlist = []  # 列表用于储存课号
            for item in resultO:
                content = obj2dict(item)
                print(">>>item content", content)
                khlist.append(content['kh'])
            q = Q()
            q.connector = 'OR'
            for i in khlist:
                print(">>>i", i)
                q.children.append(('kh', i))
            if len(q) == 0:
                restmp = C.objects.none()
            else:
                restmp = C.objects.filter(q)
            result = result & restmp
        classtable = []
        for item in result:  # 将对象转换为字典
            content = obj2dict(item)
            tmp_o = O.objects.filter(kh=content['kh'])
            if tmp_o.count() > 0 and content['xq'] == context['xq_now']:
                print(">>>classtable content",content)
                for i in range(tmp_o.count()):
                    tmp = content.copy()
                    print(">>>tmp", tmp)
                    gh_obj = getattr(tmp_o[i], 'gh')
                    # print(">>>gh_obj",gh_obj, "i", i)
                    tmp['gh'] = getattr(gh_obj, 'gh')
                    tmp['jsmc'] = getattr(T.objects.filter(gh=tmp['gh'])[0], 'xm') # 教师名称字段，因为T表中工号唯一，所以取[0]即可
                    tmp['sksj'] = getattr(tmp_o[i], 'sksj')
                    # print(">>>classtable content",content)
                    print(">>>classtable before",classtable)
                    classtable.append(tmp)
                    print(">>>classtable after",classtable)
                    # 查学院
                    tmpD = D.objects.filter(yxh=content['yxh_id'])
                    yxm = obj2dict(tmpD[0])['yxm']
                    # print(">>>yxm",yxm)
                    tmp['yxm'] = yxm
            else:
                print("else>>>classtable before", classtable)
                classtable.append(content)
                print("else>>>classtable after", classtable)
                # 查学院
                tmpD = D.objects.filter(yxh=content['yxh_id'])
                yxm = obj2dict(tmpD[0])['yxm']
                # print(">>>yxm", yxm)
                content['yxm'] = yxm
        print(">>>classtable",classtable)
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
    context['xq_now'] = settings.XQ
    if request.method == 'GET': # 首次进入显示
        print(">>>GET")
        # context=filterE(context,request)
        print(">>>context before")
        print(context)
        context=filterEnew(context,request)
        print(">>>context after")
        print(context)
        return render(request, 'student_AddCourse.html', context=context)
    elif request.method == 'POST': # 表单选课
        print(">>>POST")
        print(">>>context before")
        print(context)
        context=filterEnew(context,request)
        print(">>>context after")
        print(context)
        # print(">>>context['kb']",context['kb'])
        kbtmp = np.array(context['kb']) # 转numpy数组，方便进行切片
        kbtmp = kbtmp[:,2:] # 用于选课时暂存课程表，以此来判断时间段是否冲突，切掉序号和上课时间
        print(">>>kbtmp",kbtmp)
        lax = ['一', '二', '三', '四', '五']
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
                    print(">>>content",content)
                    result_id.append(content)
                # 切出上课时间，判断时间段是否冲突
                print("result_id[0]['sksj']",result_id[0]['sksj'])
                flag = 0
                for xt in content['sksj'].strip('上机').split('-'):
                    print("xt", xt)
                    if xt[0].isdigit():
                        try:
                            print("try")
                            if (xt[1].isdigit()):
                                second = int(xt[0:2]) - 1
                                rest = xt[2:]
                            else:
                                second = int(xt[0]) - 1
                                rest = xt[1:]
                            while first <= second:
                                print("pos", pos, "first", first, "second", second)
                                print("kbtmp[first][pos]", kbtmp[first][pos])
                                if kbtmp[first][pos] != '': # 不为空，设置不能填
                                    flag = 1 # 不能填
                                    print("!!!kbtmp[first][pos]", kbtmp[first][pos])
                                else: # 可以填，先把当前课程填上
                                    print("!!!kbtmp[first][pos]", kbtmp[first][pos])
                                    kbtmp[first][pos] = 'wrong'  # 填充内容
                                first = first + 1
                            # print("kb", kb)
                            pos = lax.index(rest[0])
                            first = int(rest[1:]) - 1
                        except:
                            second = int(xt) - 1
                            print("except")
                            print("pos", pos, "first", first, "second", second)
                            while first <= second:
                                print("kbtmp[first][pos]", kbtmp[first][pos])
                                if kbtmp[first][pos] != '':
                                    flag = 1 # 不能填
                                    print("!!!kbtmp[first][pos]", kbtmp[first][pos])
                                else: # 可以填，先把当前课程填上
                                    print("!!!kbtmp[first][pos]", kbtmp[first][pos])
                                    kbtmp[first][pos] = 'wrong'  # 填充内容
                                first = first + 1
                    else:
                        pos = lax.index(xt[0])
                        first = int(xt[1:]) - 1
                if E.objects.filter(cid=result_id[0]['cid_id'], xh=request.user.username).exists(): # xx学号的学生选课表内已有id课程
                    m['kh'] = context['kh' + str(i)]
                    m['gh'] = context['gh' + str(i)]
                    m['res'] = '选课失败：已选此课程'
                    msg.append(m)
                    continue
                elif flag == 1: # 时间段有冲突
                    m['kh'] = context['kh' + str(i)]
                    m['gh'] = context['gh' + str(i)]
                    m['res'] = '选课失败：时间段冲突'
                    msg.append(m)
                    continue
                else:
                    item = E.objects.create(
                        # cid=result_id[0]['id'],
                        cid=C.objects.filter(kh=context['kh' + str(i)])[0],  # 课程序号
                        xn='2020-2021学年', # 当前学年
                        xq=context['xq_now'],
                        gh=T.objects.filter(gh=context['gh' + str(i)])[0], # E表的外键，T表的主键，需要使用另一张表的原型
                        # gh=context['gh' + str(i)],
                        # kh=O.objects.filter(xq='2019-2020学年冬季学期', kh=context['kh' + str(i)], gh=T.objects.filter(gh=gh)[0])[0],
                        kh=context['kh' + str(i)],
                        xh=S.objects.filter(xh=request.user.username)[0]
                    )
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
        context = filterEnew(context,request)
        print(">>>context after")
        print(context)
        return render(request, 'student_AddCourse.html', context=context)

# 针对403问题，对此次view请求取消csrf验证
@csrf_exempt
@login_required
def student_DeleteCourse(request):
    print(">>>student_DeleteCourse")
    context = get_user_info(request)
    context['xq_now'] = settings.XQ
    if request.method == 'GET': # 首次进入显示
        print(">>>GET")
        context = filterEnew(context, request)
        print(">>>context after")
        print(context)
        return render(request, 'student_DeleteCourse.html', context=context)
    elif request.method == 'POST': # 表单退课
        print(">>>POST")
        # print(request.body)
        # 需要使用request.body来获取内容
        data = json.loads(request.body.decode('utf-8'))
        context['kh_array'] = data.get('kh_array')
        context['gh_array'] = data.get('gh_array')
        # context['kh_array'] = request.POST.get('kh_array')
        # context['gh_array'] = request.POST.get('gh_array')
        print(context['kh_array'])
        print(context['gh_array'])
        # 接下来做删除课程操作
        msg = [] # 列表存储删除的课程，后发现无法传回给前端
        for i in range(0,len(context['kh_array'])):
            m = {}  # 临时字典存储课号，工号和结果
            if context['kh_array'][i] == '课程号': # 获取到了全选框所在行的内容，此次不做
                print(context['kh_array'][i])
                continue
            m['kh'] = context['kh_array'][i]
            m['gh'] = context['gh_array'][i]
            m['res'] = '退课成功'
            msg.append(m)
            E.objects.filter(xq=context['xq_now'], xh=request.user.username, kh=context['kh_array'][i], gh=context['gh_array'][i]).delete()
        print(">>>msg")
        print(msg)
        context['msg'] = msg
        context = filterEnew(context, request)
        print(">>>context after")
        print(context)
        return render(request, 'student_DeleteCourse.html', context=context)
        # return HttpResponse(json.dumps({
        #     "kh_array": context['kh_array'],
        #     "gh_array": context['gh_array']
        # }))

@login_required
def student_QueryGrades(request):
    print(">>>student_QueryGrades")
    context = get_user_info(request)
    context['xq_now'] = settings.XQ
    context = filterEnew(context, request)
    print(">>>context after")
    print(context)
    calGPA(context)
    return render(request, 'student_QueryGrades.html', context=context)

@login_required
def student_CourseTable(request):
    print(">>>student_CourseTable")
    context = get_user_info(request)
    context['xq_now'] = settings.XQ
    if request.method == 'GET':
        print(">>>GET")
        context = filterEnew(context, request)
        print(">>>context after")
        print(context)
        calGPA(context)
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

# 计算绩点
def calGrade(score):
    # print(">>>calGrade",score, type(score))
    if score is None: # 还未登录
        grade = 0.0
        return grade
    if score >= 90:
        grade = 4.0
    elif score >= 85 and score < 90:
        grade = 3.7
    elif score >= 82 and score < 85:
        grade = 3.3
    elif score >= 78 and score < 82:
        grade = 3.0
    elif score >= 75 and score < 78:
        grade = 2.7
    elif score >= 72 and score < 75:
        grade = 2.3
    elif score >= 68 and score < 72:
        grade = 2.0
    elif score >= 66 and score < 68:
        grade = 1.7
    elif score >= 64 and score < 66:
        grade = 1.5
    elif score >= 60 and score < 64:
        grade = 1.0
    elif score < 60:
        grade = 0.0
    else:
        grade = 666
    return grade

# 筛选已选课程
def filterE(context,request):
    result = E.objects.filter(xq=context['xq_now'], xh=request.user.username)
    opentable = []  # 开课表，记录工号和上课时间
    teachertable = []  # 教师表，记录工号和姓名
    ghlist = []  # 列表记录使用教师名称在教师表查询到的内容，从其中取出工号
    classtable1 = []  # 列表记录课程名称、学分、学时和院系号
    classtable = []
    for item in result:  # 将对象转换为字典
        content = obj2dict(item)
        result1 = O.objects.filter(cid=content['id'])  # 进行提取工号和上课时间
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
    cidlist = []  # 列表记录O表课程id
    for t1 in opentable:
        cidlist.append(t1['cid_id'])
    print(">>>cidlist")
    print(cidlist)
    for item in result:  # 将对象转换为字典
        content = obj2dict(item)
        ############# 考虑查询结果如何显示 #####################################
        if content['id'] in cidlist:  # 通过课程id将查询结果中的C表与O表T表对应
            i = cidlist.index(content['id'])  # 找出下标对应的课程id
            content['gh'] = opentable[i]['gh_id']
            content['sksj'] = opentable[i]['sksj']
            content['km'] = classtable1[i]['km']
            content['xf'] = classtable1[i]['xf']
            content['xs'] = classtable1[i]['xs']
            content['yxh'] = classtable1[i]['yxh_id']
            # 查学院
            tmp = D.objects.filter(yxh=content['yxh'])
            yxm = obj2dict(tmp[0])['yxm']
            content['yxm'] = yxm
            for item1 in teachertable:
                if item1['gh'] == opentable[i]['gh_id']:  # 存在一个老师开多门课，此时需找到每门课程对应的工号，再寻找教师名称
                    print(">>>111")
                    print(item1['gh'])
                    content['jsmc'] = item1['xm']
        classtable.append(content)
    print(">>>classtable")
    print(classtable)
    context['classtable'] = classtable
    return context

# 新筛选已选课程
def filterEnew(context,request):
    result = E.objects.filter(xq=context['xq_now'], xh=request.user.username)
    classtable = []
    letterlist = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N']
    kb = [['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''],
          ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''],
          ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', '']]
    # print("kb", kb)
    lax = ['一', '二', '三', '四', '五']
    idx = 0 # 当前课程下标
    for item in result:  # 将对象转换为字典
        content = obj2dict(item)
        # print(">>>classtable content before", content)
        # 查课程
        resultC = C.objects.filter(id=content['cid_id'])
        contentC = obj2dict(resultC[0])
        # print(">>>contentC", contentC)
        content['km'] = contentC['km']
        content['xf'] = contentC['xf']
        content['xs'] = contentC['xs']
        # 查开课
        resultO = O.objects.filter(cid=content['cid_id'],gh=content['gh_id']) # 同一课程序号加工号只能在开课表查出一门课程，而且选课只能选一门
        contentO = obj2dict(resultO[0])
        # print(">>>contentO", contentO)
        content['sksj'] = contentO['sksj']
        # 查教师名称
        resultT = T.objects.filter(gh=content['gh_id']) # 一个工号对应一个教师
        contentT = obj2dict(resultT[0])
        content['jsmc'] = contentT['xm']
        # 查学院
        resultD = D.objects.filter(yxh=contentC['yxh_id'])
        yxm = obj2dict(resultD[0])['yxm']
        content['yxm'] = yxm
        # 计算绩点
        content['grade'] = calGrade(content['zpcj'])
        # 添加字母序号
        content['letter'] = letterlist[idx]
        # print(">>>classtable content after", content)
        classtable.append(content)
        # 提取上课时间
        for xt in content['sksj'].strip('上机').split('-'):
            # print("xt", xt)
            if xt[0].isdigit():
                try:
                    if (xt[1].isdigit()):
                        second = int(xt[0:2]) - 1
                        rest = xt[2:]
                    else:
                        second = int(xt[0]) - 1
                        rest = xt[1:]
                    while first <= second:
                        # print("pos", pos, "first", first, "second", second)
                        kb[first][pos] = content['letter'] # 填充内容
                        first = first + 1
                    # print("kb", kb)
                    pos = lax.index(rest[0])
                    first = int(rest[1:]) - 1
                except:
                    second = int(xt) - 1
                    # print("pos", pos, "first", first, "second", second)
                    while first <= second:
                        kb[first][pos] = content['letter']
                        first = first + 1
            else:
                pos = lax.index(xt[0])
                first = int(xt[1:]) - 1
        idx = idx + 1
    # print(">>>kb",kb)
    time = ['8:00 ~ 8:45', '8:55 ~ 9:40', '10:00 ~ 10:45', '10:55 ~ 11:40', '12:10 ~ 12:55', '13:05 ~ 13:50', '14:10 ~ 14:55',
            '15:05 ~ 15:50', '16:00 ~ 16:45', '16:55 ~ 17:40', '18:00 ~ 18:45', '18:55 ~ 19:40', '19:50 ~ 20:35']
    cnt = 1 # 课程表序号
    for i, j in zip(kb, time):
        i.insert(0, cnt)
        i.insert(1, j)
        # print(">>>i insert",i)
        cnt = cnt + 1
    context['kb'] = kb
    print(">>>classtable")
    print(classtable)
    context['classtable'] = classtable
    return context

# 计算总学分和均绩
def calGPA(context):
    # print(">>>calGPA")
    # print(">>>classtable",context['classtable'])
    xftotal = 0 # 总计学分
    gradetotal = 0 # 所有课程绩点总和
    for i in context['classtable']:
        xftotal = xftotal + i['xf']
        gradetotal = gradetotal + i['xf'] * i['grade']
    # print(">>>xftotal",xftotal)
    # print(">>>gradetotal",gradetotal)
    if xftotal != 0:
        GPA = round(gradetotal / xftotal + 0.00001, 2) # 四舍五入
        print(">>>gradetotal / xftotal",gradetotal / xftotal)
    else: # 防止除0
        GPA = 0
    print(">>>GPA",GPA)
    context['xftotal'] = xftotal
    context['GPA'] = GPA