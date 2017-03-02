# -*- coding: UTF-8 -*-

import logging
import traceback

import requests
import time
from django.utils.encoding import smart_str

from core.exception.biz_exception import ParamException
from core.utils.numutils import to_int, to_float

logger = logging.getLogger('biz')


def get_int_no_none(request, key):
    if key in request.REQUEST:
        return to_int(request.REQUEST[key])
    raise ParamException(key, "参数不存在,%s" % key)


def get_int(request, key, default=None):
    if key in request.REQUEST:
        return to_int(request.REQUEST[key])
    return default


def get_float_no_none(request, key):
    if key in request.REQUEST:
        return to_float(request.REQUEST[key])
    raise ParamException(key, "参数不存在,%s" % key)


def get_str_no_none(request, key):
    if key in request.REQUEST:
        return str(request.REQUEST[key])
    raise ParamException(key, "参数不存在,%s" % key)


def get_str(request, key, default=None):
    if key in request.REQUEST:
        return str(request.REQUEST[key])
    return default


def get_page_no(request):
    p_list = request.path.split("-p")
    if len(p_list) >= 2:
        p_list = p_list[1].split("-")
        return to_int(p_list[0])
    return 1


def encode_params(params):
    """
        将dict转换为url请求的参数形式:a=b&c=d
    """
    args = []
    for (k, v) in params.items():
        args.append("%s=%s" % (str(k), str(v)))
    return "&".join(args)


def parse_qs(response_data):
    return urlparse.parse_qs(response_data, True)


def get(url, **kwargs):
    try:
        start_time = time.time()
        logger.info("REQUEST GET URL:%s,PARAMS:%s" % (url, smart_str(kwargs)))

        r = requests.request('get', url, **kwargs)

        end_time = time.time()
        use_time = int((end_time - start_time) * 1000)
        if r.headers.get('Content-Type').split("/")[0] in ['image']:
            content = r.headers.get('Content-Type')
        else:
            content = r.content

        logger.info("REQUEST GET RESPONSE:%sms[%s]" % (use_time, content))
        return r
    except:
        logger.warn("REQUEST ERROR:" + traceback.format_exc())


def post(url, data=None, json=None, **kwargs):
    try:
        start_time = time.time()
        logger.info("REQUEST POST URL:%s,PARAMS:%s,JSON:%s,DATA:%s" % (url, smart_str(kwargs), json, data))

        r = requests.request('post', url, data=data, json=json, **kwargs)

        end_time = time.time()
        use_time = int((end_time - start_time) * 1000)
        logger.info("REQUEST POST RESPONSE:%sms[%s]" % (use_time, r.content))
        return r
    except:
        logger.warn("REQUEST ERROR:" + traceback.format_exc())


def get_ip(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    return ip
