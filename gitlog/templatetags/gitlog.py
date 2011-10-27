'''
Created on Oct 26, 2011

@author: masarliev
'''
from django import template
from django.template.defaultfilters import stringfilter
import datetime
from django.contrib.auth.models import User
from django.template.base import TemplateSyntaxError, Node
register = template.Library()
from django.conf import settings
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

@register.inclusion_tag('projects/commit_row.html')
def render_commit_row(commit, item, *args, **kwargs):
    static_url = getattr(settings, 'STATIC_URL')
    cm = commit.repo.iter_commits(commit,item.path).next()
    if cm.message.__len__() > 35:
        message = substr(cm.message, 35) + ' ...'
    else:
        message = cm.message
    try:
        author =  User.objects.get(email=cm.author.email)
    except :
        author = cm.author.email
    age = timetodate(cm.authored_date)
    commit_id, commit_ref = commit.name_rev.split(' ')
    return {'image':item.type, 'name':item.name, 'age':age, 'message':message, 'author':author, 'static_url':static_url, 'commit_id':commit_id, 'commit_ref':commit_ref}
    