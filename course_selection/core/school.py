#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/6 14:02
# @Author  : DollA
# @Site    : 
# @File    : school.py
# @Software: PyCharm



# 学校对象
class School:
    def __init__(self, name):
        self.name = name
        self.course = []


# 班级对象
class Classes:
    def __init__(self, school, name, course, student_path):
        self.school = school  # 班级所在学校
        self.name = name  # 班级名称
        self.course = course
        self.student_path = student_path  # 学生信息文件路径
        # self.students = ['学生对象']


# 课程对象
class Course:
    def __init__(self, name, period, price, school):
        self.name = name
        self.period = period  # 课程周期
        self.price = price
        self.school = school

    def __repr__(self):
        return self.name




# 初始化方法,建立两个校区，三门课程,一个管理员
if __name__ == '__main__':
    """
    生成实例化对象
    保存到文件
        获取路径
        新建文件
        写入实例
    """
    import os
    import sys

    # base_dir = os.path.dirname(os.getcwd())  # 和下面是一样的 吗
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(base_dir)
    from conf.config import school_obj_path
    from conf.config import course_obj_path
    from core.my_pickle import MyPickle
    from core.Manager import Manager

    # 拿到school的pickle
    # 拿到course的pickle
    course_pickle = MyPickle(course_obj_path)
    school_pickle = MyPickle(school_obj_path)
    # 生成需要的对象
    python = Course('Python', '6个月', 19800, '北京校区')
    linux = Course('Linux', '4个月', 12800, '北京校区')
    go = Course('Go', '5个月', 9800, '上海校区')

    school_shanghai = School('上海校区')
    school_shanghai.course.append(go)

    school_beijing = School('北京校区')
    school_beijing.course.append(python)
    school_beijing.course.append(linux)
    # school_beijing.course_python = python
    # school_beijing.course_linux = linux
    # # pickle序列化
    school_pickle.dump(school_beijing)
    school_pickle.dump(school_shanghai)
    course_pickle.dump(python)
    course_pickle.dump(linux)
    course_pickle.dump(go)
    #生成管理员对象
    file = os.path.join(base_dir, r'db\Manager_obj')
    name = 'eva'

    manager = Manager(name)
    mp = MyPickle(file).dump(manager)


