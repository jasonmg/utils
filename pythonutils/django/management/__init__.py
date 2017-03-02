# -*- coding:utf8 -*-

from django.db.models.signals import post_migrate
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

def add_print_permissions(sender, **kwargs):
    """
    This syncdb hooks takes care of adding a print permission too all our
    content types. reference from: https://gist.github.com/nicpottier/880901
    pls put it under app module directory
    usage:
       python3 manage.py makemigrations
       python3 manage.py migrate
    """
    # for each of our content types
    for content_type in ContentType.objects.all():
        # build our permission slug
        codename = "print_%s" % content_type.model

        # if it doesn't exist..
        if not Permission.objects.filter(content_type=content_type, codename=codename):
            # add it
            Permission.objects.create(content_type=content_type,
                                      codename=codename,
                                      name="Can print %s" % content_type.name)
            print("Added print permission for %s" % content_type.name)

# check for all our print permissions after a syncdb
post_migrate.connect(add_print_permissions)