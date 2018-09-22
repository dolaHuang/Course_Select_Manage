#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/5 11:10
# @Author  : DollA
# @Site    : 
# @File    : start.py
# @Software: PyCharm
import os
import sys

# base_dir = os.path.dirname(os.getcwd())  # 和下面是一样的 吗
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from core import main
from core.school import School
from core.school import Course
from core.Manager import Manager

if __name__ == '__main__':
    print('选课系统'.center(40, '-'))
    menu = [{'登陆': main.main},
            {'学员注册': main.sign_up},
            {'退出': exit}]

    while True:
        for i, v in enumerate(menu, 1):
            print(i, list(v.keys())[0])
        print('ps:<q>为返回键')
        choice = input('输入功能序号>>').strip()
        if choice.isdigit():
            choice = int(choice)
            if 0 < choice <= len(menu):
                list(menu[choice - 1].values())[0]()

            else:
                print('ERROR:没有这个序号！')
        elif choice == 'q':
            exit('您已退出系统！')
        else:
            print('ERROR:输入错误！')
