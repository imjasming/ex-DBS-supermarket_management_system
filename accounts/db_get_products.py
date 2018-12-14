from django.db import connection


def get_products():
    temp = {'pid':[], 'pname':[], }

    cursor = connection.cursor()
    cursor.execute("call quiry_goods();")


#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pymysql


def get_city_data_form_table(table):
    # 存数据的list
    db_temps = {'avg': [], 'min': [], 'max': []}

    avg_temps = []
    min_temps = []
    max_temps = []

    # 打开数据库连接
    db = pymysql.connect('172.31.34.225', 'root', '123456')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    sql = "SELECT * FROM PredictionData." + table
    try:
        # 使用 execute()  方法执行 SQL 查询
        cursor.execute(sql)
        # 使用获取单全部数据
        dataRows = cursor.fetchall()

        for row in dataRows:
            avg_temps.append(row[1])
            max_temps.append(row[2])
            min_temps.append(row[3])

    except Exception as e:
        raise e
    finally:
        db.close()  # 关闭数据库连接

    db_temps['avg'] = db_temps['avg'] + avg_temps
    db_temps['min'] = db_temps['min'] + min_temps
    db_temps['max'] = db_temps['max'] + max_temps

    return db_temps


beijing = {'name': 'Beijing', 'data': get_city_data_form_table('ori_beijing')}
guangzhou = {'name': 'Guangzhou', 'data': get_city_data_form_table('ori_guangzhou')}
kunming = {'name': 'Kunming', 'data': get_city_data_form_table('ori_kunming')}
shanghai = {'name': 'Shanghai', 'data': get_city_data_form_table('ori_shanghai')}
json_city_data = {'beijing': beijing, 'guangzhou': guangzhou, 'kunming': kunming, 'shanghai': shanghai}


def get_predict_data_form_table(city, mode):
    # 存数据的list
    db_temps = {'avg': [], 'min': [], 'max': []}
    max_ = []
    min_ = []
    avg = []
    max_ori = []
    min_ori = []
    avg_ori = []
    max_pre = []
    min_pre = []
    avg_pre = []

    # 打开数据库连接
    db = pymysql.connect('172.31.34.225', 'root', '123456')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    try:
        # 使用 execute()  方法执行 get origin data
        cursor.execute("SELECT * FROM PredictionData.ori_" + city)
        # 使用获取单全部数据
        dataRows = cursor.fetchall()
        # get origin data
        for row in dataRows:
            max_ori.append(row[1])
            avg_ori.append(row[2])
            min_ori.append(row[3])

        if mode == 'ari':
            # 使用 execute()  方法执行 get predict data
            cursor.execute("SELECT * FROM PredictionData.ari_" + city)
        else:
            cursor.execute("SELECT * FROM PredictionData.ten_" + city)

        # 使用获取单全部数据
        dataRows = cursor.fetchall()
        # get predict data
        for row in dataRows:
            max_pre.append(row[1])
            avg_pre.append(row[2])
            min_pre.append(row[3])

        for i in range(0, len(max_ori)):
            max_.append(max_ori[i])
            min_.append(min_ori[i])
            avg.append(avg_ori[i])

        for n in range(0, len(max_pre)):
            max_.append(max_pre[n])
            min_.append(min_pre[n])
            avg.append(avg_pre[n])

    except Exception as e:
        raise e
    finally:
        db.close()  # 关闭数据库连接

    db_temps['avg'] = db_temps['avg'] + avg
    db_temps['min'] = db_temps['min'] + min_
    db_temps['max'] = db_temps['max'] + max_

    return db_temps


beijing_pre = {'name': 'Beijing', 'data': get_predict_data_form_table('beijing', 'ten')}
guangzhou_pre = {'name': 'Guangzhou', 'data': get_predict_data_form_table('guangzhou', 'ten')}
kunming_pre = {'name': 'Kunming', 'data': get_predict_data_form_table('dali', 'ten')}
shanghai_pre = {'name': 'Shanghai', 'data': get_predict_data_form_table('shanghai', 'ten')}
beijing_ari = {'name': 'beijing_ari', 'data': get_predict_data_form_table('beijing', 'ari')}
json_predict_data = {'beijing': beijing_pre, 'guangzhou': guangzhou_pre, 'kunming': kunming_pre,
                     'shanghai': shanghai_pre, 'beijing_ari': beijing_ari}


def get_account_from_db():
    users = []
    # 打开数据库连接
    db = pymysql.connect('172.31.34.225', 'root', '123456')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    sql = "SELECT * FROM PredictionData.Accounts"
    try:
        # 使用 execute()  方法执行 SQL 查询
        cursor.execute(sql)
        # 使用获取单全部数据
        dataRows = cursor.fetchall()

        for row in dataRows:
            user = {'level': row[2], 'username': row[0], 'password': row[1]}
            users.append(user)

    except Exception as e:
        raise e
    finally:
        db.close()  # 关闭数据库连接

    return users
