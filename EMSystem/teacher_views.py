import MySQLdb
from django.db import connection
from django.forms import forms
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from pymysql import NULL

from jwc.settings import XQ
from .models import S,D,T,C,O,E

def toast(request,a,x = ''):
    if(a == 1):
        messages.success(request,"本学期没有课程")
    elif(a == 2):
        messages.success(request, "提交成功")
    elif(a == 3):
        messages.success(request,"没有需要打分的学生")
    elif(a == 4):
        messages.success(request,"已经有本课程")
    elif(a == 5):
        messages.success(request,"课程号错误："+x)

def get_from_table(sql,param):
    cursor = connection.cursor()
    cursor.execute(sql,param)
    row = cursor.fetchall()
    desc = cursor.description
    title = []
    out = []
    for i in desc:
        title.append(i[0])
    for i in row:
        out.append(dict(zip(title,i)))
    return out

def update_from_table(sql,param):
    cursor = connection.cursor()
    cursor.execute(sql, param)
    return

def find(request):
    a = request.user
    #sql = 'select * from emsystem_t t join emsystem_d d on t.yxh_id=d.yxh where gh = %s'%a
    sql = 'select * from emsystem_t where gh = %s'%a
    result = T.objects.raw(sql)
    for i in result:
        x = i.yxh_id
        sql = 'select * from emsystem_d where yxh = %s'%x
        ot = D.objects.raw(sql)
        for k in ot:
            content={"xm" : i.xm,'gh':i.gh,'yx':k.yxm,'zc':i.xl,'yxh_id':i.yxh_id}
    return content

def index(request):
    b = find(request)
    ct =b
    return render(request,"teacher_index.html",context=ct)

def check(request):
    if request.method == 'GET':
        b = find(request)
        return render(request, "teacher_check.html", context=b)
    elif request.method == 'POST':
        try:
            gt = request.POST['rdy']
            b = find(request)
            sql = 'select * from emsystem_e e join emsystem_s s on e.xh_id = s.xh where e.kh=%s and e.xq=%s and e.gh_id=%s'
            param = [gt,XQ,b['gh']]
            result0 = get_from_table(sql,param)
            k = []
            for i in result0:
                temp = {'xh':i['xh'],'xm':i['xm'],'xb':i['xb'],'sjhm':i['sjhm'],'xy':'','pscj':i['pscj']}
                sql = 'select yxm from emsystem_d where yxh=%s'
                param =[i['yxh_id']]
                r = get_from_table(sql,param)
                temp['xy'] = r[0]['yxm']
                if(temp['pscj'] == None):
                    temp['pscj'] = '暂未打分'
                k.append(temp)
            b['k'] = k
            return render(request, "teacher_check_detial.html", context=b)
        except:
            b = find(request)
            x = str(request.POST['xq'])
            gg = b['gh']
            sql = 'select * from emsystem_c c join emsystem_o o on c.kh=o.kh where c.xq = %s and o.gh_id = %s'
            param = [x,gg]
            result = get_from_table(sql,param)
            k=[]
            kb=[['','','','',''],['','','','',''],['','','','',''],['','','','',''],
                ['','','','',''],['','','','',''],['','','','',''],['','','','',''],
                ['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','','']]
            print(kb)
            lax = ['一','二','三','四','五']
            for i in result:
                temp = {'kh' : i['kh'],'km' : i['km'],'xf' : i['xf'],'xs':i['xs'],'ct':0}
                sql = 'select * from emsystem_e where kh = %s and gh_id = %s'
                param = [i['kh'],gg]
                rt = get_from_table(sql,param)
                temp['ct']=len(rt)
                k.append(temp)
                temp = {'km':i['km'],'sj':''}
                i['sksj'] = i['sksj'].replace(':', '').replace(' ', '')
                for xt in i['sksj'].split('-'):
                    print(xt)
                    if xt[0].isdigit():
                        try:
                            if(xt[1].isdigit()):
                                second = int(xt[0:2])-1
                                rest = xt[2:]
                            else:
                                second = int(xt[0])-1
                                rest = xt[1:]
                            while first <= second:
                                print(pos,first,second)
                                kb[first][pos] = i['km']
                                first = first + 1
                            print(kb)
                            pos = lax.index(rest[0])
                            first = int(rest[1:])-1
                        except:
                            second = int(xt)-1
                            print(pos, first, second)
                            while first <= second:
                                kb[first][pos] = i['km']
                                first = first + 1
                    else:
                        pos = lax.index(xt[0])
                        first = int(xt[1:])-1
            print('end')
            b['k'] = k
            b['Xq'] = x
            time = ['8:00-8:45','8:55-9:40','10:00-10:45','10:55-11:40','12:10-12:55','13:05-13:50','14:10-14:55','15:05-15:50','16:00-16:45','16:55-17:40','18:00-18:45','18:55-19:40','19:50-20:35']
            for i,j in zip(kb,time):
                i.insert(0,j)
            b['kb'] = kb
            if(k == []):
                toast(request,1)
            return render(request, "teacher_check.html",context = b)

def write_ready(request):
    x = XQ
    b = find(request)
    gg = b['gh']
    sql = 'select * from emsystem_c c join emsystem_o o on c.kh=o.kh where c.xq = %s and o.gh_id = %s'
    param = [x, gg]
    result = get_from_table(sql, param)
    k = []
    for i in result:
        temp = {'km': str(str(i['km']) + str(i['kh']))}
        k.append(temp)
    return k

def write(request):
    b = find(request)
    if request.method == 'GET' :
        k = write_ready(request)
        b['k'] = k
        return render(request, "teacher_write.html", context=b)
    else:
        try:
            rf = request.POST['pscj']
            x = request.POST['m']
            x = x[-8:]
            rf = request.POST
            sql = 'select * from emsystem_e where xq = %s and gh_id = %s and kh = %s order by xh_id'
            param = [XQ, b['gh'], x]
            result = get_from_table(sql, param)
            for i,j,k,l in zip(rf.getlist('pscj'),rf.getlist('kscj'),rf.getlist('zpcj'),result):
                sql = 'UPDATE emsystem_e SET pscj=%s,kscj=%s,zpcj=%s WHERE xh_id=%s and gh_id=%s and kh=%s'
                param = [i,j,k,l['xh_id'],l['gh_id'],x]
                print(param)
                update_from_table(sql,param)
                print(param)
            toast(request,2)
            k = write_ready(request)
            b['k'] = k
            return render(request, "teacher_write.html", context=b)
        except:
            z = b
            k = write_ready(request)
            z['k'] = k
            try:
                x = str(request.POST['kc'])
            except:
                x = ''
            x = x[-8:]
            gg = b['gh']
            sql = 'select * from emsystem_e e join emsystem_s s on e.xh_id=s.xh where e.xq = %s and e.gh_id = %s and e.kh = %s order by xh'
            param = [XQ,gg,x]
            result = get_from_table(sql,param)
            k=[]
            for i in result:
                temp = {'xh' : i['xh_id'],'xm' : i['xm'],'pscj' : i['pscj'],'kscj':i['kscj'],'zpcj':i['zpcj']}
                k.append(temp)
            z['x'] = k
            try:
                z['Xq'] = str(request.POST['kc'])
            except:
                z['Xq'] = ''
            if(x !='' and k==[]):
                toast(request,3)
            return render(request, "teacher_write.html",context = z)

def open(request):
    b = find(request)
    if(request.POST.dict().__contains__('stats')):
        stats = request.POST['stats']
        if (stats == '开设新课程'):
            b['ck'] = 1
        elif(stats == '下学期课程提交'):
            b['ck'] = 2
        elif(stats == '审核情况查询'):
            b['ck'] = 3
            sql = 'select * from emsystem_temp where gh = %s'
            param = [b['gh']]
            result = get_from_table(sql, param)
            sub = []
            for i in result:
                print(i)
                temp={'xq':i['xq'],'km':i['km'],'tp':'新课程提交','st':'待审核'}
                if(i['xf']==0):
                    temp['tp'] = '任课申请'
                if(i['stats'] == '3'):
                    temp['st'] = '通过'
                elif(i['stats'] == '4'):
                    temp['st'] = '拒绝'
                sub.append(temp)
            if (sub ==[]):
                b['ck']=4
            b['sch'] = sub
        return render(request, "teacher_open.html", context=b)
    else:
        if request.POST.getlist('m') != []:
            xq = request.POST['m']
            x = request.POST
            if(xq == '1'):
                sql = 'insert into emsystem_temp (xq,km,xf,gh,yxh_id,stats) values (%s,%s,%s,%s,%s,%s)'
                param = [XQ[0:-4]+x['xq'],x['km'],x['xf'],b['gh'],b['yxh_id'],'0']
                print(param)
                sql2 = 'select km,xq,yxh_id from emsystem_temp where km=%s and xq=%s and yxh_id=%s'
                param2 = [x['km'],XQ[0:-4]+x['xq'],b['yxh_id']]
                t_d = get_from_table(sql2,param2)
                if t_d ==[] :
                    update_from_table(sql,param)
                    b['ck'] = 0
                    toast(request,2)
                else:
                    toast(request,4)
            elif(xq == '2'):
                n = ['kh1','kh2','kh3','kh3','kh4','kh5','kh6']
                for i in n:
                    if (x[i] == ''):
                        continue
                    sql = 'insert into emsystem_temp (xq,km,xf,gh,yxh_id,stats) values (%s,%s,%s,%s,%s,%s)'
                    param = [XQ,x[i],0,b['gh'],b['yxh_id'],'1']
                    sql2 = 'select kh from emsystem_c where kh=%s'
                    param2 = [x[i]]
                    t_d = get_from_table(sql2, param2)
                    if(t_d == []):
                        toast(request,5,x[i])
                        continue
                    update_from_table(sql,param)
                b['ck'] = 0
                toast(request, 2)
            return render(request, "teacher_open.html", context=b)
        else:
            b['ck'] = 0
            b['xueqi'] = XQ
            return render(request, "teacher_open.html", context=b)