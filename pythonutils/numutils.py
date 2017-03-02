# -*- coding:utf8 -*-

import random


def to_int(num, default=None):
    """
    转化正整数
    如果参数为空或者非数字返回None
    :param num:
    :return:
    """
    try:
        return int(num)
    except:
        return default


def to_float(num, default=None):
    """
    转化正浮点数
    如果参数为空或者非数字返回None
    :param num:
    :return:
    """
    try:
        return float(num)
    except:
        return default


def get_random_array(digit):
    """
    获取指定长度随机组合
    :param digit:
    :return:
    """
    random_array = ""
    for i in range(0, digit, 1):
        random_array += "%s" % random.randint(0, 9)
    return random_array
