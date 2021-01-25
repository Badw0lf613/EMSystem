import MySQLdb
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import S,D,T,C,O,E

def index(request):
    views_num = 0
    return render(request,"teacher_index.html",)
