# -*- coding: UTF-8 -*-

import random
from xml.dom import minidom


def is_blank(string):
    """
    检查参数是否为空

    :param string:
    :return:
           None == True
        " 123 " == False
        "     " == True
    """
    if string is None or len(string) == 0 or len(string.strip()) == 0:
        return True
    return False


def is_any_blank(*strings):
    """
    检查任意参数是否为空

    :param strings:
    :return:
    """

    for string in strings:
        if is_blank(string):
            return True
    return False


def is_not_blank(string):
    """
    检查参数是否不为空

    :param string:
    :return:
    """
    return not is_blank(string)


def str_len(string):
    """
    计算字符串长度，如果为None返回-1

    :param string:
    :return:
    """

    if is_blank(string):
        return -1
    else:
        return len(string)


def add_str(string_list, interval=" "):
    str = ""
    for string in string_list:
        if not is_blank(string):
            str += string + interval
    return str


def mobile_check(mobile_no):
    # 号码前缀，如果运营商启用新的号段，只需要在此列表将新的号段加上即可。
    prefix = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139",
              "150", "151", "152", "153", "154", "155", "156", "157", "158", "159",
              "170", "171", "172", "173", "174", "175", "176", "177", "178", "179",
              "180", "181", "182", "183", "184", "185", "186", "187", "188", "189"]
    if mobile_no is None or len(mobile_no) != 11:
        return False
    else:
        if mobile_no.isdigit():
            if mobile_no[:3] in prefix:
                return True
            else:
                return False
        else:
            return False


def dict2xml(req_dict, is_need_xml=True):
    xml = ""
    for key, value in req_dict.items():
        xml += "<%s>%s</%s>" % (key, value, key)

    if is_need_xml:
        return str("<xml>" + xml + "</xml>")
    return str(xml)


def xml2dict(xml_str):
    result = {}
    if type(xml_str) == unicode:
        xml_str = xml_str.encode('utf-8')
    elif type(xml_str) == str:
        pass

    doc = minidom.parseString(xml_str)
    params = [ele for ele in doc.childNodes[0].childNodes
              if isinstance(ele, minidom.Element)]

    for param in params:
        if param.childNodes:
            text = param.childNodes[0]
            result[param.tagName] = text.data
    return result


def random_str(count):
    str = ""
    for i in range(0, count, 1):
        str += random.choice('abcdefghigklmnopqrstuvwxyzABCDEFGHIGKLMNOPQRSTUVWXYZ0123456789')
    return str
