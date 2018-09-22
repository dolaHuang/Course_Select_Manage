#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/5 11:36
# @Author  : DollA
# @Site    :
# @File    : Manager.py
# @Software: PyCharm
import os
import re
import time

from conf import config
from core import my_pickle
from core.Teacher import Teacher
from core import school
from core.Student import Student
from core.Utility_class import Show
from core import Utility_class
from core import logger

# 管理员类
class Manager(Show):
    menu = [('创建讲师账号', 'create_teacher'),
            ('创建学生账号', 'create_student'),
            ('创建课程', 'create_course'),
            ('创建班级', 'create_classes'),
            ('查看学校', 'show_school'),
            ('查看讲师', 'show_teacher'),
            ('查看课程', 'show_course'),
            ('查看班级', 'show_classes'),
            ('为班级指定老师', 'class_bound_teacher'),
            ('退出', 'exit_func')]

    # 添加用户登录信息到文件,非绑定方法
    @staticmethod
    def userinfo_handle(content):
        f = open(config.userinfo_path, 'r+', encoding='utf-8')
        data = f.read()
        f.write(content)
        f.close()

    # 创建老师对象
    def create_teacher(self, *args):
        """
        创建讲师角色时要关联学校，
        :return:
        """
        name_teacher = input('讲师姓名>>')
        password_teacher = input('登陆密码>>')
        self.show_school()
        # self.show_obj_dicts(obj_dicts)
        # 规范学校名字
        input_msg = '指定学校>>'
        school = self.standard_input(input_msg, config.school_list)
        # 老师登陆信息写入文件
        content = '\n%s|%s|Teacher' % (name_teacher, password_teacher)
        Manager.userinfo_handle(content)
        teacher = Teacher(name_teacher)
        teacher.school = school
        teacher.classes = []
        self.teacher_picke_obj.dump(teacher)
        print('老师<%s>创建成功!' % name_teacher)
        # 日志
        msg = '创建老师账号<%s>' % name_teacher
        log_file = os.path.join(config.log_path, config.LOG_TYPES['manager'])
        logger.logger(log_file, msg)

    # 创建课程对象
    def create_course(self, *args):
        """
        输入:学科名称、价格、周期
        创建一个课程对象，dump进course文件

        :return:
        """
        # 规范课程名字
        # print(tabulate([config.course_list], headers=['name', 'name', 'name'], tablefmt='gird'))
        print('课程名称'.center(40, '-'))
        for name in config.course_list:
            print('corse_name:', name)
        input_msg = '请输入课程名称>>'
        name_course = self.standard_input(input_msg, config.course_list)
        if name_course:
            # 规范价格
            while True:
                price_course = input('请输入课程价格>>').strip()
                if price_course.isdigit():
                    price_course = int(price_course)
                    # 规范课程周期，以月为单位
                    while True:
                        period_course = input('请输入课程周期>>')
                        ret = re.fullmatch('\w+个月', period_course)
                        if ret:
                            # 规范课程所属学校
                            # print(tabulate([config.school_list], headers=['name', 'name', 'name'], tablefmt='gird'))
                            print('学校名称'.center(40, '-'))
                            for name in config.school_list:
                                print('school_name:', name)
                            input_msg = '请输入学校名称>>'
                            school_course = self.standard_input(input_msg, config.school_list)

                            # 创建课程对象
                            course_obj = school.Course(name_course, period_course, price_course, school_course)
                            self.course_picke_obj.dump(course_obj)
                            print('课程<%s>创建成功' % name_course)
                            # 日志
                            msg = '创建课程<%s>' % name_course
                            log_file = os.path.join(config.log_path, config.LOG_TYPES['manager'])
                            logger.logger(log_file, msg)
                            return
                        elif period_course == 'q':
                            print('返回上一级！')
                            break
                        else:
                            print('输入错误！eg：6个月')
                elif price_course == 'q':
                    print('返回上一级！')
                    break
                else:
                    print('课程价格必须是一个数字！')

    # 创建班级对象
    def create_classes(self, *args):
        print('学校列表'.center(40, '-'))
        self.show_school()
        # 规范学校名字
        input_msg = '班级所在学校>>'
        school_name = self.standard_input(input_msg, config.school_list)
        # 提取 学校对象
        school_data = my_pickle.MyPickle(config.school_obj_path).loaditer()
        school_class = self.bound(school_data, school_name)
        if school_class:
            # 提取该学校课程到列表
            obj_dicts = self.get_obj_dict('course_picke_obj')
            course_obj_dicts = []
            course_names = []
            # 按用户选择，添加符合条件的课程到空列表
            for i in obj_dicts:
                if i['school'] == school_name:
                    course_obj_dicts.append(i)
                    course_names.append(i['name'])
            print('课程列表'.center(40, '-'))
            # 展示符合条件的课程
            self.show_obj_dicts(course_obj_dicts)
            #  规范课程名字
            input_msg = '班级课程>>'
            course_name = self.standard_input(input_msg, course_names)
            # 提取 课程对象
            couse_data = my_pickle.MyPickle(config.course_obj_path).loaditer()
            course_class = self.bound(couse_data, course_name)
            if course_class:
                # 规范班级名字，因为正则语法不一样，所以不能用standard_input方法
                print('请添加班级名称！')
                print('班级名称格式<课程名_期号>eg：Python_s1')
                while True:
                    name_class = input('班级名称>>').strip()
                    ret = re.fullmatch('(Python|Linux|Go)_[a-z]\d', name_class)
                    if ret:
                        # 如果格式正确并且是以课程名开头
                        if ret.group().startswith(course_name):

                            # 班级的学生对象所在文件路径
                            student_path = os.path.join(config.base_dir, r'db\class_students(%s)' % name_class)
                            open(student_path, 'w').close()
                            # 班级对象
                            class_obj = school.Classes(school_class, name_class, course_class, student_path)
                            class_obj.start_time = time.strftime("%Y-%m-%d", time.localtime(time.time()))
                            class_obj.teacher = '未指定'
                            # 班级对象上课记录
                            class_obj.class_logger = []
                            # 作业空间
                            class_obj.homework_zone = []
                            self.class_picke_obj.dump(class_obj)
                            print('班级<%s>创建成功' % name_class)
                            # 日志
                            msg = '创建班级<%s>' % name_class
                            log_file = os.path.join(config.log_path, config.LOG_TYPES['manager'])
                            logger.logger(log_file, msg)
                            return
                        else:
                            print('输入错误！班级名称必须用已选择的课程名称开头')
                    elif name_class == 'q':
                        print('返回上一级')
                        break
                    else:
                        print('班级输入错误！请重新输入！格式<课程名_期号>eg：Python_s1')
        else:
            print('添加失败')

    # 创建学生对象
    def create_student(self, *args):
        """
        创建学员时，选择学校，关联班级
        1、输入：学生姓名，密码
        2、直接指定班级，因为，班级有自己的学校和课程属性
        3、将学生信息写入userinfo文件中
        4、创建一个学生对象
        :return:
        """
        name_student = input('学生姓名>>')
        password_student = input('登陆密码>>')
        class_names = []
        print('班级列表'.center(40, '-'))
        flag = self.show_classes()
        if flag:
            # 规范班级名字
            obj_dicts = self.get_obj_dict('class_picke_obj')
            for i in obj_dicts:
                class_names.append(i['name'])
            input_msg = '指定班级>>'
            class_student = self.standard_input(input_msg, class_names)
            class_data = self.class_picke_obj.loaditer()  # 得到的是班级生成器
            for class_i in class_data:
                if class_i.name == class_student:
                    # 保存学生账号到userinfo文件
                    content = '\n%s|%s|Student' % (name_student, password_student)
                    Manager.userinfo_handle(content)
                    # 生成 学生对象
                    stu_obj = Student(name_student)
                    stu_obj.school = class_i.school
                    stu_obj.classes = class_i
                    stu_obj.course_not_paid = []
                    stu_obj.homework_no_finished = []
                    # 保存到班级文件和学员
                    my_pickle.MyPickle(class_i.student_path).dump(stu_obj)
                    my_pickle.MyPickle(config.students_obj_path).dump(stu_obj)
                    print('学员<%s>创建成功' % name_student)
                    # 日志
                    msg = '创建学生<%s>，并加入班级<%s>' % (name_student, class_student)
                    log_file = os.path.join(config.log_path, config.LOG_TYPES['manager'])
                    logger.logger(log_file, msg)
                    break
            else:
                print('您输入的信息有误，创建学生失败')
        else:
            print('无班级信息，请创建班级！')

    # 为班级指定老师
    def class_bound_teacher(self, *args):
        """
        管理员选择为老师还是学生指定班级
        如果是为老师绑定班级
            找到指定的老师和对应的班级（都是通过show方法查看之后选择）
            给讲师对象的班级属性的列表中加入一个新的项 ，值为班级的对象
            给班级对象中的讲师属性列表加入一个新的项，值为讲师的对象
        如果为学生绑定班级
            找到指定的学生和对应的班级（都是通过show方法查看之后选择）
            给学生创建新的班级属性，将属性的值设置为班级对象
            将学生对象的信息 根据班级对象中存储的学生信息存储路径 dump入对应文件
        :return:
        """
        # 选择需要指定的班级
        class_list = []
        ret = self.show_classes()
        if ret:
            while True:
                name_class = input('请输入要指定的班级>>').strip()
                if name_class == 'q':
                    break
                else:
                    class_g = self.class_picke_obj.loaditer()
                    for class_obj in class_g:
                        if class_obj.name == name_class and class_obj.teacher == '未指定':
                            class_list.append(class_obj)
                            self.show_teacher()
                            while True:
                                name_teacher = input('请输入要指定的老师>>')
                                if name_teacher == 'q':
                                    break
                                else:
                                    teacher_g = self.teacher_picke_obj.loaditer()
                                    for teacher_obj in teacher_g:
                                        if teacher_obj.name == name_teacher:
                                            # 老师和班级互相绑定
                                            teacher_obj.classes.append(class_list[0])
                                            class_list[0].teacher = teacher_obj
                                            teacher_g.close()
                                            class_g.close()
                                            # 跟新文件
                                            self.class_picke_obj.edit(class_list[0])
                                            self.teacher_picke_obj.edit(teacher_obj)
                                            print('为班级<%s>指定老师<%s>成功！' % (name_class, name_teacher))
                                            # 日志
                                            msg = '为班级<%s>指定了老师<%s>' % (name_class, name_teacher)
                                            log_file = os.path.join(config.log_path, config.LOG_TYPES['manager'])
                                            logger.logger(log_file, msg)
                                            return
                                    else:
                                        print('输入错误！请重新输入')
                    else:
                        print('输入错误或者该班级已指定老师！请重新输入')

    # 退出功能
    def exit_func(self, *args):
        # 日志
        msg = '管理员<%s>退出系统' % args[0].name
        log_file = os.path.join(config.log_path, config.LOG_TYPES['access'])
        logger.logger(log_file, msg)
        exit('您已退出系统！')
