# -*- coding:utf8 -*-

import socket


def get_local_ip():
    # temporal solution
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("gmail.com", 80))
        ip_address = s.getsockname()[0]
    return ip_address


def get_client_ip(req):
    """
    reference from: http://www.cnblogs.com/chengmo/archive/2013/05/29/php.html
    """
    if hasattr(req, 'META'):
        try:
            # for proxy server 
            real_ip = req.META['HTTP_X_FORWARDED_FOR']
            regip = real_ip.split(",")[0]
        except Exception:
            try:
                regip = req.META['REMOTE_ADDR']
            except Exception:
                regip = ""
    else:
        regip = ""
    return regip
