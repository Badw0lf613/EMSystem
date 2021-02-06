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

def toast(request,a):
    if(a == 1):
        messages.success(request,"本学期没有课程")
    elif(a == 2):
        messages.success(request, "提交成功")
    elif(a == 3):
        messages.success(request,"没有需要打分的学生")

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
            content={"xm" : i.xm,'gh':i.gh,'yx':k.yxm,'zc':i.xl}
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
                if(temp['pscj'] == NULL):
                    temp['pscj'] = '暂未打分'
                k.append(temp)
            print(k)
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
            for i in result:
                temp = {'kh' : i['kh'],'km' : i['km'],'xf' : i['xf'],'xs':i['xs'],'ct':0}
                sql = 'select * from emsystem_e where kh = %s and gh_id = %s'
                param = [i['kh'],gg]
                rt = get_from_table(sql,param)
                temp['ct']=len(rt)
                k.append(temp)
            b['k'] = k
            b['Xq'] = x
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
                update_from_table(sql,param)
            toast(request,2)
            k = write_ready(request)
            b['k'] = k
            return render(request, "teacher_write.html", context=b)
        except:
            print(2.2)
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

