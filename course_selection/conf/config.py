#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/5 16:55
# @Author  : DollA
# @Site    : 
# @File    : config.py
# @Software: PyCharm
import os
import logging
# 根目录路径
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 登录信息文件路径
user_info = r'db\userinfo'
userinfo_path = os.path.join(base_dir, user_info)
# 学校对象文件路径
school_obj = r'db\school_obj'
school_obj_path = os.path.join(base_dir, school_obj)
# 老师对象文件路径
teacher_obj = r'db\Teacher_obj'
teacher_obj_path = os.path.join(base_dir, teacher_obj)
# 学员对象文件路径
students_obj = r'db\Student_obj'
students_obj_path = os.path.join(base_dir, students_obj)
# 课程对象文件路径
course_obj = r'db\course_obj'
course_obj_path = os.path.join(base_dir, course_obj)
# 班级对象文件路径
class_obj = r'db\class_obj'
class_obj_path = os.path.join(base_dir, class_obj)
# 所有课程名字列表
course_list = ['Python', 'Linux', 'Go']
# 所有学校名字列表
school_list = ['北京校区', '上海校区']
# 日志目录
log_dir = r'logs'
log_path = os.path.join(base_dir, r'logs')
# 日志级别
LOG_LEVEL = logging.INFO
# 日志类别
LOG_TYPES = {
    'access': 'access.log',
    'teacher': 'teachers.log',
    'student': 'students.log',
    'manager': 'manager.log'}


