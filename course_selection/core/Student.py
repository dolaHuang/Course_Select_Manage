#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/7 18:02
# @Author  : DollA
# @Site    : 
# @File    : Student.py
# @Software: PyCharm
import os

from core.Utility_class import Show
# from core.Teacher import Teacher
from conf import config
from core.my_pickle import MyPickle
from core import logger

from tabulate import tabulate


# 学生类
class Student(Show):
    """
    学员视图， 可以注册， 交学费， 选择班级，
        选择课程之后，会增加一项课程数据，包括是否付款的信息
        付完款，可以绑定班级
            查看班级
            查看讲师
            查看学校
            这些数据都在班级对象中
    """
    menu = [
        ('选择班级', 'select_classes'),
        ('学费缴纳', 'tuition_payments'),
        ('查看班级', 'show_my_class'),
        ('查看同学', 'show_students'),
        ('提交作业', 'do_homework'),
        ('退出', 'exit')

    ]

    def __init__(self, name):
        Show.__init__(self, name)
        self.name = name

    # 更新文件
    def update(self, obj, filename):
        mp_st = MyPickle(filename)
        mp_st.edit(obj)

    # 选择课程 ，选择班级
    def select_classes(self, *args):
        """
        选择学校
        选择课程
        选择班级
        加入属性，和未付款标志
        :return:
        """
        # 学生对象
        student = args[0]
        # 选择学校
        print('学校列表'.center(40, '-'))
        self.show_school()
        # 规范学校名称
        input_msg = '请输入要选择的学校名称>>'
        choice_school = self.standard_input(input_msg, config.school_list)
        school_data = self.school_picke_obj.loaditer()
        ret1 = self.bound(school_data, choice_school)
        if ret1:
            student.school = ret1
            # 选择课程
            print('课程列表'.center(40, '-'))
            for i, course in enumerate(student.school.course, 1):
                print(course)

            # 规范课程名称
            input_msg = '请输入要选择的课程>>'
            names = map(lambda j: str(j), student.school.course)
            choice_course = self.standard_input(input_msg, names)
            course_data = self.course_picke_obj.loaditer()
            ret2 = self.bound(course_data, choice_course)
            if ret2:
                student.course_not_paid.append(ret2)
                print('添加课程<%s>成功！' % choice_course)
                # 选择班级
                class_names = []
                class_objs = []
                class_data = self.class_picke_obj.loaditer()
                print('可选班级列表'.center(40, '-'))
                for class_obj in class_data:
                    if class_obj.course.name == student.course_not_paid[-1].name:
                        print(class_obj.name)
                        class_objs.append(class_obj)
                        class_names.append(class_obj.name)
                        print('end'.center(40, '-'))
                        input_msg = '请输入您想要进入的班级名称>>'
                        class_choice = self.standard_input(input_msg, class_names)
                        # class_data.close()
                        for obj in class_objs:
                            if obj.name == class_choice:
                                student.classes = obj

                                # 对象放进指定班级文件中
                                file_path = os.path.join(config.base_dir,
                                                         r'db\class_students(%s)' % student.classes.name)
                                mp_class = MyPickle(file_path)
                                mp_class.dump(student)
                                # 修改学生文件中对象
                                mp_st = MyPickle(config.students_obj_path)
                                mp_st.edit(student)
                                print('已成功选择课程<%s>并加入班级<%s>' % (choice_course, class_choice))
                                # 日志
                                msg = '学生<%s>成功选择课程<%s>并加入班级<%s>' % \
                                      (args[0].name, choice_course, class_choice)
                                log_file = os.path.join(config.log_path, config.LOG_TYPES['student'])
                                logger.logger(log_file, msg)
                                return
                        else:
                            print('添加班级失败！')
                else:
                    print('该课程暂时没有班级上线，请稍等，或者联系在线客服。')
        else:
            print('添加学校失败！')

    # 缴学费
    # 待添加ATM
    def tuition_payments(self, *args):
        """
        选择课程之后，会增加一项课程数据，包括是否付款的信息
            查看课程信息
            打印是否有未付款课程
        :return:
        """
        # 展示未付款课程
        course_list = []
        if hasattr(args[0], 'course_not_paid'):
            for i, v in enumerate(args[0].course_not_paid, 1):
                course = []
                course.append(i)
                for j in v.__dict__.values():
                    course.append(j)
                course_list.append(course)
            if course_list:
                print('未付款课程'.center(40, '-'))
                print(tabulate(course_list, headers=['序号', '名称', '周期', '价格', '学校'], floatfmt='grid'))
                # 去除要交费的课程
                while True:
                    choice = input('请输入要缴费的课程序号>>')
                    if choice.isdigit():
                        choice = int(choice)
                        if 0 <= choice <= len(course_list):
                            args[0].course_not_paid.pop(choice - 1)
                            # 去除后，修改学生文件中的数据
                            self.update(args[0], config.students_obj_path)
                            # 修改，班级文件中的数据
                            file_path = os.path.join(config.base_dir,
                                                     r'db\class_students(%s)' % args[0].classes.name)
                            self.update(args[0], file_path)
                            print('您为课程<%s>缴费成功，花费%s' %
                                  (course_list[choice - 1][1], course_list[choice - 1][3]))
                            # 日志
                            msg = '学生<%s>成功为课程<%s>缴费<%s>' % \
                                  (args[0].name, course_list[choice - 1][1], course_list[choice - 1][3])
                            log_file = os.path.join(config.log_path, config.LOG_TYPES['student'])
                            logger.logger(log_file, msg)
                            return
                        else:
                            print('请输入列表中的序号')
                else:
                    print('请输入列表中的序号')
            else:
                print('没有未付款的课程！')
        else:
            print('ERROR:查看未付款课程错误！')

    # 提交作业
    def do_homework(self, *args):
        """
        1、提取学生待完成作业homework_no_finished:列表中的字典格式
            {'作业名字': homework_name, '作业内容': homework_info}}
        2、班级对象中的课程记录
            class_logger =
            {'讲课时间': class_time,
            '课程内容': class_info,
            '作业%s'%class_time: {'作业名字': homework_name, '作业内容': homework_info}}
            class_obj.class_logger = []
            class_obj.homework_zone = []
        得到班级对象，
        查看班级作业
            输入 作业
        添加到班级已完成作业 {作业名字：[姓名，作业，成绩]}
        跟新文件
        :param args: students_obj
        :return:
        """
        # 查看作业
        homeworks = args[0].homework_no_finished  # 未完成作业 字典格式{'作业名字': homework_name, '作业内容': homework_info}}
        print('作业列表'.center(40, '-'))
        if homeworks:
            for i, homework in enumerate(homeworks, 1):
                print(i, homework['作业名字'])
                print('-' * 32)
            while True:
                choice = input('请选择要提交的作业序号>>').strip()
                if choice.isdigit():
                    choice = int(choice)
                    if 0 < choice <= len(homeworks):
                        print('作业详情'.center(40, '-'))
                        print('作业名:', homeworks[choice - 1]['作业名字'])
                        print('作业详情:', homeworks[choice - 1]['作业内容'])

                        # 输入完成作业内容
                        my_homework = input('输入作业答案>>')
                        # # 把作业添加到班级作业空间
                        homework_zip = [homeworks[choice - 1]['作业名字'], {'姓名': args[0].name, '作业': my_homework, '成绩': ''}]
                        class_data = self.class_picke_obj.loaditer()
                        for class_obj in class_data:
                            if class_obj.name == args[0].classes.name:
                                class_obj.homework_zone.append(homework_zip)
                                class_data.close()
                                self.class_picke_obj.edit(class_obj)
                                print('作业<%s>已成功提交！' % homeworks[choice - 1]['作业名字'])
                                # 日志
                                msg = '学生<%s>完成作业<%s>' % (args[0].name, homeworks[choice - 1]['作业名字'])
                                log_file = os.path.join(config.log_path, config.LOG_TYPES['student'])
                                logger.logger(log_file, msg)
                                # 删除待完成作业
                                del args[0].homework_no_finished[choice-1]
                                self.students_picke_obj.edit(args[0])
                                return
                        else:
                            print('更新数据失败！')
                    else:
                        print('输入错误，请输入列表中的数字！')
                elif choice == 'q':
                    break
                else:
                    print('输入错误，请输入列表中的数字！')
        else:
            print('暂时没有待完成作业！')

    # 查看我的班级
    def show_my_class(self, *args):
        if hasattr(args[0], 'classes'):
            # 先跟新一下班级信息
            class_data = self.class_picke_obj.loaditer()
            for class_obj in class_data:
                if class_obj.name == args[0].classes.name:
                    args[0].classes = class_obj
                    class_data.close()
                    self.class_picke_obj.edit(args[0])
                    break
            # 跟新完后 判定 班级老师 是否指定
            teacher = '未指定' if args[0].classes.teacher == '未指定' else args[0].classes.teacher.name
            # 打印班级信息
            print('所在班级'.center(40, '-'))
            print("""
            班级名称:%s
            老师姓名:%s
            开班时间:%s
            课程周期:%s
            """ % (args[0].classes.name, teacher,
                   args[0].classes.start_time, args[0].classes.course.period))  # 创建班级之前添加的是字符串，需要修改
            # 日志
            msg = '学生<%s>查看班级信息' % args[0].name
            log_file = os.path.join(config.log_path, config.LOG_TYPES['student'])
            logger.logger(log_file, msg)
        else:
            print('无班级信息，请先选择课程！')

    # 查看班级同学
    def show_students(self, *args):
        """
        学生对象的班级属性，找到班级路径
        打开路径
        提取所有学员
        :param args: 学生对象的列表
        :return:
        """
        if hasattr(args[0], 'classes'):
            student_path = args[0].classes.student_path
            classes_name = args[0].classes.name
            self.show_students_Utility(student_path, classes_name)
            # 日志
            msg = '学生<%s>查看班级同学列表' % args[0].name
            log_file = os.path.join(config.log_path, config.LOG_TYPES['student'])
            logger.logger(log_file, msg)

    def exit(self, *args):
        msg = '学生<%s>退出系统' % args[0].name
        log_file = os.path.join(config.log_path, config.LOG_TYPES['access'])
        logger.logger(log_file, msg)
        exit('您已退出系统！')
