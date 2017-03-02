# -*- coding:utf8 -*-

import os
import os.path
import logging
from core.utils.encode import *
from xhtml2pdf import pisa
from core.utils import dateutils
from django.conf import settings

logger = logging.getLogger("pdfutils")


def delete_intermediate_file(func):
    def wrapper(*args, **kw):
        (pdf, output_file) = func(*args, **kw)

        # delete intermediate file before return to file stream
        if os.path.exists(output_file):
            logger.info("delete intermediate file: %s" % output_file)
            os.remove(output_file)
        return pdf

    return wrapper


@delete_intermediate_file
def convert_html_pdf(html, output_file=""):
    html = str(html).encode('utf-8')
    if not output_file:
        output_file = os.path.join(settings.BASE_DIR, "xadmin_model_print_%s.pdf" % dateutils.get_epoch_now())

    with open(output_file, "w+b") as result_file:
        pisa.CreatePDF(html, dest=result_file, link_callback=link_callback, encoding='utf-8')

        # Return PDF document through a Django HTTP response
        result_file.seek(0)
        pdf = result_file.read()

    return pdf, output_file


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """

    def remove_first_slash(_str):
        if _str and _str[0] == "/":
            return remove_first_slash(_str[1:])
        return _str

    # use short variable names
    sUrl = settings.STATIC_URL  # Typically /static/
    sRoot = settings.PROJECT_STATIC_ROOT  # Typically /home/userX/project_root/static/
    mUrl = settings.MEDIA_URL  # Typically /static/media/
    mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_root/static/media/

    # convert URIs to absolute system paths
    if mUrl and uri.startswith(mUrl):
        path = os.path.join(mRoot, remove_first_slash(uri.replace(mUrl, "")))
    elif sUrl and uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
        # path = os.path.join(sRoot, remove_first_slash(uri.replace(sUrl, "")))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path
