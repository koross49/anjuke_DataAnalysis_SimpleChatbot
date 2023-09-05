import pymysql
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
import django.core.handlers.wsgi
from django.contrib import messages

import time
import pandas as pd
import os
import random
import json

import numpy as np
import jieba
from joblib import load
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from joblib import dump
import csv
# Create your views here.



def read_d(file_path):
    data = []

    # 从CSV文件中读取数据
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            # 将每一行的数据转换为float类型并添加到data列表中
            data.append([float(value) for value in row])

    return data

def read_c(file_path):
    loaded_data = []

    # 从CSV文件中读取数据
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            # 将每一行的数据添加到loaded_data列表中
            loaded_data.append(row)

    return loaded_data


# 计算 consine 余弦相似度
def consine(inputCommand, data0):
    # 把输入命令转化为数组格式
    sentence = jieba.lcut(inputCommand)
    words = str.join(' ', sentence)
    list = []
    list.insert(0, words)
    # 获取训练好的 TfidfVectorizer 模型
    pwd = os.path.dirname(__file__)
    print('我觉得这里一定进了')
    model = load('model.pkl')


    # 获取输入命令的 TF-IDF 向量
    data1 = model.transform(list).toarray().reshape(1, -1)
    # 余弦相似度对比
    result = cosine_similarity(data0, data1)
    # print('相似度对比：\n{0}'.format(result))
    print('进到这里了')
    return result


def bot(comm):
    # 相似度
    treshold = 0.2
    # 拒识话术
    jstext = '抱歉，这个问题我不会！！！'
    pwd = os.path.dirname(__file__)
    data0_filename = pwd + "/data/data.csv"
    command_filename = pwd + "/data/commands.csv"
    data0 = read_d(data0_filename)
    command = read_c(command_filename)
    # print(data0)
    # print(command)
    if comm:
        # 获取余弦相似度
        result = np.array(consine(comm, data0))
        # 获取相似度最高的命令 index
        argmax = result.argmax()
        # 读取命令回复
        data = command[argmax][1]
        # print('命令：{0}\n回复：{1}'.format(comm,data))
        if result[argmax][0] >= treshold:
            data = data
        else:
            data = jstext
    else:
        data = ''
    return data



# 处理重定向
def redirect(request):
    return HttpResponseRedirect('login')


def login(request, method=['GET','POST']):
    assert isinstance(request, django.core.handlers.wsgi.WSGIRequest)
    if request.method == 'GET':
        print('get方法')
        name = request.COOKIES.get('name') or ''
        password = request.COOKIES.get('password') or ''
        print('GET' + name + password)
        if name == '':
            print('get_login失败')
            return render(request, 'data_analysis/login.html')
            print('没有返回吗')
        db = None
        try:
            db = pymysql.connect(host='localhost', user=name, password=password, charset='utf8')
            return HttpResponseRedirect('index')
        except:
            messages.error(request, '数据库登录错误')
            return render(request, 'data_analysis/login.html')
    if request.method == 'POST':
        print('post方法')
        name = request.POST.get('name')
        password = request.POST.get('password')
        print(name, password)
        try:
            db = pymysql.connect(host='localhost', user=name, password=password, charset='utf8')
            resp = HttpResponseRedirect('index')
            resp.set_cookie('name', name)
            resp.set_cookie('password', password)
            return resp
        except:
            messages.error(request, '数据库登录错误')
            return render(request, 'data_analysis/login.html')
    # print("没进去")
    # return HttpResponseRedirect('index')

def flot(request):
    return render(request, 'data_analysis/flot.html')

def chatbot(request, method=['POST']):
    answer = ""
    if request.method == 'POST':
        question = request.POST.get('question')
        answer = bot(question)
        print('测试到没到这')
    return render(request, 'data_analysis/chatbot.html', {'answer': answer})

def index(request, method=['GET']):
    data = [{'name': '东丽区', 'number': 39, 'price': 2070.63}, {'name': '南开区', 'number': 299, 'price': 2650.0}, {'name': '和平区', 'number': 199, 'price': 2735.64}, {'name': '塘沽区', 'number': 9, 'price': 2680.8}, {'name': '大港区', 'number': 99, 'price': 1943.1}, {'name': '宁河区', 'number': 485, 'price': 3200.0}, {'name': '宝坻区', 'number': 484, 'price': 1439.8}, {'name': '武清区', 'number': 483, 'price': 2640.72}, {'name': '汉沽区', 'number': 352, 'price': 1573.94}, {'name': '河东区', 'number': 39, 'price': 1241.67}, {'name': '河西区', 'number': 152, 'price': 2820.0}, {'name': '津南区', 'number': 481, 'price': 2158.99}, {'name': '红桥区', 'number': 52, 'price': 1875.0}, {'name': '蓟县区', 'number': 487, 'price': 1992.86}, {'name': '西青区', 'number': 480, 'price': 1188.89}, {'name': '静海区', 'number': 486, 'price': 1700.0}]
    if request.GET.get('newdb'):
        print("jinlaile ")
        db = None
        name = request.COOKIES.get('name')
        password = request.COOKIES.get('password')
        try:
            db = pymysql.connect(host='localhost', user=name, password=password, charset='utf8')
        except:
            return HttpResponseRedirect('login')
        cursor = db.cursor()
        # 创建数据库
        cursor.execute("drop database if exists anjuke_data;")
        cursor.execute("create database if not exists anjuke_data;")
        cursor.execute("use anjuke_data;")

        # 创建房源表
        cursor.execute("drop table if exists house_info;")
        sql_create_star = """create table if not exists house_info(
                                id int not null primary key auto_increment,
                                rent varchar(255),
                                deposit varchar(255),
                                layout varchar(255),
                                area varchar(255),
                                orientation varchar(255),
                                floor varchar(255),
                                decoration varchar(255),
                                type varchar(255),
                                compound varchar(255),
                                street varchar(255)
                                );"""
        cursor.execute(sql_create_star)
        # 写入数据
        pwd = os.path.dirname(__file__)
        stars = pd.read_csv(pwd + '/data/house_info.csv', encoding='gbk')
        # print(stars)
        for _, curr_star in stars.iterrows():
            sql_insert_star = "insert into house_info(rent, deposit, layout, area, orientation, floor, decoration, type, compound, street) VALUE ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                curr_star['rent'], curr_star['deposit'], curr_star['layout'], curr_star['area'],curr_star['orientation'],
                curr_star['floor'], curr_star['decoration'], curr_star['type'], curr_star['compound'],curr_star['street'])
            # print(sql_insert_star)
            cursor.execute(sql_insert_star)

        db.commit()
        messages.success(request, '创建数据库成功！')
        print('创建数据库成功')
        return HttpResponseRedirect('index')
    return render(request, 'data_analysis/index.html', {'data': data})

def morris(request):
    return render(request, 'data_analysis/morris.html')

def query(request):
    return render(request, 'data_analysis/query.html')

def tables(request):
    return render(request, 'data_analysis/tables.html')

def logout(request):
    response = HttpResponseRedirect("login")
    response.delete_cookie('name')
    response.delete_cookie('password')
    return response

