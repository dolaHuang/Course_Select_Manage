#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/6 10:08
# @Author  : DollA
# @Site    : 
# @File    : my_pickle.py
# @Software: PyCharm
import pickle
import os

from conf.config import school_obj_path
from conf.config import course_obj_path


# 创建一个Pickle 类，用与每次都会需要 打开文件，序列化写入，或者反序列化
class MyPickle:
    def __init__(self, filename):
        self.filename = filename

    # 序列化对象
    def dump(self, obj):
        with open(self.filename, 'ab') as f:
            pickle.dump(obj, f)

    # 提取对象数据
    def loaditer(self):
        with open(self.filename, 'rb') as f:
            # 必须一次一次load，用生成器
            # 如果是空的，在这里返回假
            while True:
                try:
                    obj = pickle.load(f)
                    if obj:
                        yield obj
                        # if obj:
                        #     print(1)
                except EOFError:

                    break
    # 跟新文件内容
    def edit(self, obj):
        """
        编辑，修改
        1、接受一个新的obj
        :param obj:
        :return:
        """
        Mp = MyPickle(self.filename+'.txt')  # 创建一个新的文件
        for item in self.loaditer():  # 打开原文件
            if item.name == obj.name:
                Mp.dump(obj)     # 如果名字一样，把新的放进去
            else:
                Mp.dump(item)
        # 修改文件名，覆盖原文件
        os.replace(self.filename+'.txt', self.filename)

