# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/16 9:06
# @Author  : DolA
# @Site    :
# @File    : logger.py
# @Software: Pycharm
import logging

from conf import config


# 记录账户登录日志
def logger(log_file, msg):

    # 生成logging对象
    logger = logging.getLogger()
    logger.setLevel(config.LOG_LEVEL)
    # 生成handler 对象
    fh = logging.FileHandler(log_file, encoding='utf-8')
    fh.setLevel(config.LOG_LEVEL)
    # 生成 formatter 对象
    formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
    # 绑定
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    # 日志消息
    logger.info(msg)
    logger.removeHandler(fh)
    return logger





