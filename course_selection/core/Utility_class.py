#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/8 12:03
# @Author  : DollA
# @Site    : 
# @File    : Utility_class.py
# @Software: PyCharm
import re
import os

from conf import config
from core import my_pickle
from core.my_pickle import MyPickle
from core import logger

class Show:
    def __init__(self, name):
        self.name = name
        # 用文件路径，拿到了my_pickle的实例化对象，可以对文件进行pickle操作
        self.teacher_picke_obj = my_pickle.MyPickle(config.teacher_obj_path)
        self.course_picke_obj = my_pickle.MyPickle(config.course_obj_path)
        self.school_picke_obj = my_pickle.MyPickle(config.school_obj_path)
        self.class_picke_obj = my_pickle.MyPickle(config.class_obj_path)
        self.students_picke_obj = my_pickle.MyPickle(config.students_obj_path)

    # 判断对象的名字是不是和输入一样，并返回对象
    def bound(self, data, choice):
        for obj in data:
            if obj.name == choice:
                return obj

    # 查看指定对象信息
    def show(self, pickle_obj):
        flag = True
        pickle_obj = getattr(self, pickle_obj)  # 反射对应方法
        load_data = pickle_obj.loaditer()
        if load_data:
            for obj in load_data:
                flag = False
                if obj.__dict__:
                    for i in obj.__dict__:
                        if i in ['student_path',
                                 'class_logger',
                                 'homework_zone',
                                 'teacher_picke_obj',
                                 'course_picke_obj',
                                 'school_picke_obj',
                                 'class_picke_obj',
                                 'students_picke_obj']:
                            continue
                        elif isinstance(obj.__dict__[i], list):
                            class_list = []
                            for j in obj.__dict__[i]:
                                class_list.append(j.name)
                            print(i, class_list)
                        elif isinstance(obj.__dict__[i], str) or isinstance(obj.__dict__[i], int):
                            print(i, obj.__dict__[i])
                        else:
                            print(i, obj.__dict__[i].name)
                    print('-' * 44)

            if flag:
                print('暂时没有相关数据！')
                return False
            return True

    # 规范输入功能
    def standard_input(self, input_msg, names):
        re_rule = '|'.join(names)
        while True:
            name = input(input_msg).strip()
            if re.fullmatch(re_rule, name):
                return name
            elif name == 'q':
                print('返回上一级')
                return
            else:
                print('输入错误！请按照列表中name重新输入！')

    # 提取对象字典
    def get_obj_dict(self, pickle_obj):  # 查看指定对象信息
        pickle_obj = getattr(self, pickle_obj)  # 反射对应方法
        load_g = pickle_obj.loaditer()  # 得到的是一个生成器，eg：课程文件夹包含所有课程....
        # global obj_dicts
        obj_dicts =[]
        for obj in load_g:
            obj_dicts.append(obj.__dict__)

        return obj_dicts

    # 展示对象字典
    def show_obj_dicts(self, obj_dicts):
        for i in obj_dicts:
            for j in i:
                print(j, i[j])
            print('-' * 50)

    # 查看所有老师
    def show_teacher(self, *args):
        print('讲师列表'.center(40, '-'))
        self.show('teacher_picke_obj')
        # 日志
        msg = '用户<%s>查看老师列表' % args[0].name
        log_file = os.path.join(config.log_path, config.LOG_TYPES['manager'])
        logger.logger(log_file, msg)
    # 查看所有课程
    def show_course(self, *args):
        print('课程列表'.center(40, '-'))
        self.show('course_picke_obj')
        # 日志
        msg = '用户<%s>查看课程列表' % args[0].name
        log_file = os.path.join(config.log_path, config.LOG_TYPES['manager'])
        logger.logger(log_file, msg)

    # 查看所有学校
    def show_school(self, *args):
        print('学校列表'.center(40, '-'))
        self.show('school_picke_obj')
        # 日志
        msg = '用户<%s>查看学校列表' % args[0].name
        log_file = os.path.join(config.log_path, config.LOG_TYPES['manager'])
        logger.logger(log_file, msg)

    # 查看所有班级
    def show_classes(self, *args):
        print('班级列表'.center(40, '-'))
        # 日志
        msg = '用户<%s>查看班级列表' % args[0].name
        log_file = os.path.join(config.log_path, config.LOG_TYPES['manager'])
        logger.logger(log_file, msg)
        return self.show('class_picke_obj')


    # 查看班级同学
    def show_students_Utility(self, path, name):
        flag = True
        mp = MyPickle(path)
        students_data = mp.loaditer()    # 没有得到数据 没有返回值
        print('班级<%s>学员列表'.center(30, '-') % name)
        for student_obj in students_data:
            flag = False
            print(student_obj.name)
        if flag:
            print('无相关信息')
        print('end'.center(40, '-'))
        students_data.close()






