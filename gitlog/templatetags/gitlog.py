'''
Created on Oct 26, 2011

@author: masarliev
'''
from django import template
from django.template.defaultfilters import stringfilter
import datetime
from django.contrib.auth.models import User
register = template.Library()
DATE_FORMAT = '%B %d, %Y'
@stringfilter
def timetodate(value):
    return datetime.datetime.fromtimestamp(int(value)).strftime(DATE_FORMAT)
register.filter('timetodate', timetodate)

@stringfilter
def substr(value, arg):
    return value[:int(arg)]
register.filter('substr', substr)

@stringfilter
def get_username_by_email(value, attr):
    try:
        user =  User.objects.get(email=value)
        return getattr(user, attr)
    except :
        return value
register.filter('user', get_username_by_email)