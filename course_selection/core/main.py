#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/5 11:26
# @Author  : DollA
# @Site    : 
# @File    : main.py
# @Software: PyCharm
import os
import sys
import hashlib
import time

from conf import config
from core.Manager import Manager
from core.Teacher import Teacher
from core.Student import Student
from core.my_pickle import MyPickle
from core.auth import login
from core import logger

# 学员注册
def sign_up():
    username = input('请输入姓名>>').strip()
    password = input('请输入密码>>').strip()
    content = '\n%s|%s|Student' % (username, password)
    Manager.userinfo_handle(content)
    print('学员<%s>注册成功！\n请记录您的登陆账号%s' % (username, 'xxxxxx'))
    student = Student(username)
    student.course_not_paid = []
    student.homework_no_finished = []
    mp = MyPickle(config.students_obj_path)
    mp.dump(student)
    # 日志
    msg = '用户<%s>注册账号' % username
    log_file = os.path.join(config.log_path, config.LOG_TYPES['access'])
    logger.logger(log_file, msg)
    return


@login
def main(user,*args):
    """
    1、显示欢迎信息
    2、根据login返回值，提取登陆用户的类别，显示用户功能
    3、用户选择功能
    :return:
    """
    # ret = login()
    if user['user_data']:
        ret = user['user_data']
        print('欢迎%s'.center(40, '-') % ret[0])
        # 提取对象
        login_obj = []
        file_path = os.path.join(config.base_dir, r'db\%s_obj' % ret[2])
        mp = MyPickle(file_path)
        objs_data = mp.loaditer()
        for obj in objs_data:
            if obj.name == ret[0]:
                login_obj = obj
        objs_data.close()
        # # 根据登陆用户的类别，显示用户可用功能，账户类别在账户信息中，账户可用功能放在该种类中
        # 得到这些信息，然后实例化对象
        user_class = getattr(sys.modules[__name__], ret[2])  # 要用反射
        user_obj = user_class(ret[0])

        while True:
            # 显示可用功能
            for i, v in enumerate(user_obj.menu, 1):
                print(i, v[0])
            choice = input('输入功能序号>>')
            if choice.isdigit():
                choice = int(choice)
                if 0 < choice <= len(user_obj.menu):
                    user_func = getattr(user_obj, user_obj.menu[choice-1][1])
                    user_func(login_obj)
                else:
                    print('您输入的信息有误！请输入列表中的序号！')
            elif choice == 'q':
                print('返回上一级')
                break
            else:
                print('您输入的信息有误！')


# 把注册信息转换成MD5
def trans_md5(username, password):
    m = hashlib.md5()
    m.update(b'%s%s'%(username, time.time()))
    print(m.digest)
    n = hashlib.md5()
    n.update(b'%s'%password)
    print(n.digest)
