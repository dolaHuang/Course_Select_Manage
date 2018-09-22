#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/5 13:16
# @Author  : DollA
# @Site    : 
# @File    : Teacher.py
# @Software: PyCharm
import time
import os

from core import logger
from core.my_pickle import MyPickle
from core.Utility_class import Show
from conf import config

from tabulate import tabulate


class Teacher(Show):
    """
    老是对象在定义时，可以只用给他姓名，年龄，性别等
    讲师可管理自己的班级，
    上课时选择班级，
    查看班级学员列表 ，
    修改所管理的学员的成绩
    """
    menu = [
        ('查看班级', 'show_class'),
        ('查看学员列表', 'show_students'),
        ('选择上课班级', 'select_class'),
        ('修改学员成绩', 'revise_student_performance'),
        ('退出', 'exit_func')
    ]

    def __init__(self, name):
        Show.__init__(self, name)
        self.name = name

    # 查看班级
    def show_class(self, *args):
        """
        没有指定班级
            老师的属性是name
            school
            classes 对象
        指定了班级

        :param args:
        :return:
        """
        # print(args[0].classes) # 为什么突然就能运行了，之前说Tuple index out of range
        # 应该是我数据的问题，我发现有两个姗姗，我删除一个
        # 或者是在指定老师的时候，没有修改数据  不是这个
        if args[0].classes:
            class_list = []
            for i, class_obj in enumerate(args[0].classes, 1):
                cla = []
                cla.append(i)
                cla.append(class_obj.name)
                cla.append(class_obj.start_time)
                cla.append(class_obj.course.period)
                class_list.append(cla)
            print(tabulate(class_list, headers=['序号', '班级名称', '开班时间', '时间周期']))
            # 日志
            msg = '老师<%s>查看班级列表' % args[0].name
            log_file = os.path.join(config.log_path, config.LOG_TYPES['teacher'])
            logger.logger(log_file, msg)

        else:
            print('还没有给您指定班级，请联系学校教务处！')

    # 查看学生列表
    def show_students(self, *args):
        """
        输入序号选择班级

        查看学员
        :param args:
        :return:
        """
        self.show_class(*args)  # 原来是因为这里没有传参
        while True:
            choice = input('输入要查看的班级序号>>').strip()
            if choice.isdigit():
                choice = int(choice)
                if 0 < choice <= len(args[0].classes):  # 这里没有加=号 导致下面没有执行
                    student_path = args[0].classes[choice - 1].student_path
                    class_name = args[0].classes[choice - 1].name
                    self.show_students_Utility(student_path, class_name)
                    # 日志
                    msg = '老师<%s>查看班级同学列表' % args[0].name
                    log_file = os.path.join(config.log_path, config.LOG_TYPES['teacher'])
                    logger.logger(log_file, msg)
                else:
                    print('输入错误，请输入列表中的数字！')
            elif choice == 'q':
                break
            else:
                print('输入错误，请输入列表中的数字！')

    # 选择上课班级
    def select_class(self, *args):
        """
        显示班级列表
        选择上课班级
        开始上课
            讲知识
            发布作业
        下课了
        给班级添加上课信息
        :param args:
        :return:
        """
        self.show_class(*args)
        while True:
            choice = input('输入要上课的班级序号>>').strip()
            if choice.isdigit():
                choice = int(choice)
                if 0 < choice <= len(args[0].classes):
                    # 给班级添加上课信息
                    class_obj = args[0].classes[choice - 1]
                    print('开始上课了')
                    class_info = input('输入讲课内容>>')
                    homework_name = input('输入作业名字>>')
                    homework_info = input('输入作业内容>>')
                    class_time = time.strftime('%Y-%m-%d %p', time.localtime(time.time()))
                    class_logger = {'讲课时间': class_time,
                                    '课程内容': class_info,
                                    '作业%s'%class_time: {'作业名字': homework_name, '作业内容': homework_info}}
                    class_obj.class_logger.append(class_logger)
                    print('下课了，同学们记得按时完成作业')
                    # 跟新班级信息
                    self.class_picke_obj.edit(class_obj)
                    # 给班级学生添加 未完成 作业
                    # mp = MyPickle(class_obj.student_path)
                    students_data = self.students_picke_obj.loaditer()
                    for students_obj in students_data:
                        students_data.close()
                        if students_obj.classes.name == class_obj.name:
                            students_obj.homework_no_finished.append(class_logger['作业%s' % class_time])
                        # mp.edit(students_obj)
                            self.students_picke_obj.edit(students_obj)
                            # 日志
                            msg = '老师<%s>给班级<%s>上课，课程名称<%s>' % \
                                  (args[0].name, class_obj.name, class_info)
                            log_file = os.path.join(config.log_path, config.LOG_TYPES['teacher'])
                            logger.logger(log_file, msg)
                            return
                    else:
                        print('更新学员数据失败！')
                else:
                    print('输入错误，请输入列表中的数字！')
            elif choice == 'q':
                break
            else:
                print('输入错误，请输入列表中的数字！')

    # 修改学生成绩
    def revise_student_performance(self, *args):
        """
        提交作业格式 [作业名字,{姓名:''，作业:''，成绩:''}]
        作业提交在班级的作业空间
        提取老师班级
        显示班级学生（名字和作业成绩）
            选择学生序号
            输入成绩
        跟新
        :param args:
        :return:
        """
        self.show_class(*args)
        # 先跟新一下班级信息
        class_data = self.class_picke_obj.loaditer()
        for class_obj in class_data:
            for i, class_t in enumerate(args[0].classes):
                if class_obj.name == class_t.name:
                    args[0].classes[i] = class_obj
                    class_data.close()
                    self.class_picke_obj.edit(args[0])
                    break
        # 选择班级
        while True:
            choice = input('请输入要查看的班级>>').strip()
            if choice.isdigit():
                choice = int(choice)
                if 0 < choice <= len(args[0].classes):
                    homework_list = args[0].classes[choice-1].homework_zone  # 作业列表
                    # 输入要查看的作业的 名称
                    if homework_list:
                        print('作业列表'.center(40, '-'))
                        for i, homework in enumerate(homework_list, 1):
                            # for j in homework:
                                print(i, homework[0])
                        # 选择要批改的作业
                        while True:
                            choice_hm = input('请输入要批改的作业>>').strip()
                            if choice_hm.isdigit():
                                choice_hm = int(choice_hm)
                                if 0 < choice <= len(homework_list):
                                    # 查看作业
                                    homework_choice = homework_list[choice_hm-1][1]
                                    for item in homework_choice:
                                        print(item, homework_choice[item])
                                    # 给作业评分
                                    print('作业评分标准'.center(40, '-'))
                                    print('A+:优秀，A:很好,B+:好,B:基本符合要求,C:功能还需要完善')
                                    score_msg = '输入学生的成绩>>'
                                    score_list = ['A+', 'A', 'B+', 'B', 'C']
                                    score = self.standard_input(score_msg, score_list)
                                    args[0].classes[choice - 1].homework_zone[choice_hm-1][1]['成绩'] = score
                                    # 跟新老师对象args[0]
                                    self.teacher_picke_obj.edit(args[0])
                                    # 跟新班级对象args[0].classes[choice - 1]
                                    self.class_picke_obj.edit(args[0].classes[choice - 1])
                                    print('学员<%s>作业<%s>批改完成！' %
                                          (homework_choice['姓名'], homework_list[choice_hm-1][0]))
                                    # 日志
                                    msg = '老师<%s>给学生<%s>批改作业<%s>，作业成绩<%s>' % \
                                          (args[0].name, homework_choice['姓名'], homework_list[choice_hm-1][0], score)
                                    log_file = os.path.join(config.log_path, config.LOG_TYPES['teacher'])
                                    logger.logger(log_file, msg)
                                else:
                                    print('输入错误，请输入列表中的数字！')
                            elif choice_hm == 'q':
                                break
                            else:
                                print('输入错误，请输入列表中的数字！')
                    else:
                        print('无可修改作业！')
                else:
                    print('输入错误，请输入列表中的数字！')
            elif choice == 'q':
                break
            else:
                print('输入错误，请输入列表中的数字！')


    def exit_func(self, *args):
        # 日志
        msg = '老师<%s>退出系统' % args[0].name
        log_file = os.path.join(config.log_path, config.LOG_TYPES['access'])
        logger.logger(log_file, msg)
        exit('您已退出系统！')
