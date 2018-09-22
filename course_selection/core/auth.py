#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/10 9:21
# @Author  : DollA
# @Site    : 
# @File    : auth.py
# @Software: PyCharm
import os

from conf import config
from core import logger

user = {  # 存储登陆账户的状态和数据
        'authenticated': False,
        'user_data': None
    }

# 装饰器登陆认证
def login(func, *args, **kwargs):
    """
    :param func:
    :param args:
    :param kwargs:
    :return:
    """
    def inner(*args, **kwargs):
        global user
        if user['authenticated']:
            func(user, *args)
        else:
            while not user['authenticated']:
                username = input('登陆账号>>').strip()
                password = input('登陆密码>>').strip()
                if username and password:
                    user_data = login_auth(username, password)
                    if user_data:
                        user['authenticated'] = True
                        user['user_data'] = user_data
                        # 日志
                        msg = '用户<%s>登陆系统' % username
                        log_file = os.path.join(config.log_path, config.LOG_TYPES['access'])
                        logger.logger(log_file, msg)
                        return func(user, *args)
                    else:
                        print('账号或者密码输入错误')
                else:
                    print('输入错误！')
    return inner


# 账号认证模块
def login_auth(username, password):
    with open(config.userinfo_path, 'r', encoding='utf-8') as f:
        data = f.readlines()
    for i in data:
        re = i.strip().split('|')
        if username == re[0] and password == re[1]:
            return re