'''
Created on Oct 26, 2011

@author: masarliev
'''
from django import template
from django.template.defaultfilters import stringfilter
import datetime
from django.contrib.auth.models import User
from django.template.base import TemplateSyntaxError, Node
from django.utils.translation import pgettext, ungettext, ugettext as _
from django.utils.tzinfo import LocalTimezone
from datetime import date, timedelta
from django.template import defaultfilters
register = template.Library()
from django.conf import settings
DATE_FORMAT = '%d %b %Y %H:%M:%S'
@stringfilter
def timetodate(value):
    return datetime.datetime.fromtimestamp(int(value))
register.filter('timetodate', timetodate)

@stringfilter
def substr(value, arg):
    return value[:int(arg)]
register.filter('substr', substr)


def get_username_by_email(value, attr):
    try:
        user =  User.objects.get(email=value)
        return getattr(user, attr)
    except :
        return value
register.filter('user', get_username_by_email)

@register.filter
def naturaltime(value):
    """
    For date and time values shows how many seconds, minutes or hours ago
    compared to current timestamp returns representing string.
    """
    try:
        value = datetime.datetime(value.year, value.month, value.day, value.hour, value.minute, value.second)
    except AttributeError:
        return value
    except ValueError:
        return value

    if getattr(value, 'tzinfo', None):
        now = datetime.datetime.now(LocalTimezone(value))
    else:
        now = datetime.datetime.now()
    now = now - timedelta(0, 0, now.microsecond)
    if value < now:
        delta = now - value
        if delta.days != 0:
            return pgettext(
                'naturaltime', '%(delta)s ago'
            ) % {'delta': defaultfilters.timesince(value)}
        elif delta.seconds == 0:
            return _(u'now')
        elif delta.seconds < 60:
            return ungettext(
                u'a second ago', u'%(count)s seconds ago', delta.seconds
            ) % {'count': delta.seconds}
        elif delta.seconds // 60 < 60:
            count = delta.seconds // 60
            return ungettext(
                u'a minute ago', u'%(count)s minutes ago', count
            ) % {'count': count}
        else:
            count = delta.seconds // 60 // 60
            return ungettext(
                u'an hour ago', u'%(count)s hours ago', count
            ) % {'count': count}
    else:
        delta = value - now
        if delta.days != 0:
            return pgettext(
                'naturaltime', '%(delta)s from now'
            ) % {'delta': defaultfilters.timeuntil(value)}
        elif delta.seconds == 0:
            return _(u'now')
        elif delta.seconds < 60:
            return ungettext(
                u'a second from now', u'%(count)s seconds from now', delta.seconds
            ) % {'count': delta.seconds}
        elif delta.seconds // 60 < 60:
            count = delta.seconds // 60
            return ungettext(
                u'a minute from now', u'%(count)s minutes from now', count
            ) % {'count': count}
        else:
            count = delta.seconds // 60 // 60
            return ungettext(
                u'an hour from now', u'%(count)s hours from now', count
            ) % {'count': count}
            
@register.inclusion_tag('projects/commit_head.html',takes_context=True)
def commithead(context):
    commit_obj = context['commit']
    commit_id, commit_ref = commit_obj.name_rev.split(' ')
    current = True
    if commit_obj.repo.commit(commit_obj.repo.active_branch.name).name_rev != commit_obj.name_rev:
        for ref in commit_obj.repo.refs:
            if ref.commit.name_rev == commit_obj.name_rev:
                commit = ref.name
                break
        if not commit:
            commit = commit_id
        #return {'current':False, 'name':commit, 'commit':commit_obj, 'ref':commit_ref}
        current = False
    else:
        commit = commit_ref
    return {'current':current, 'name':commit, 'commit':commit_obj, 'ref':commit_ref}
@register.inclusion_tag('projects/commit_row.html',takes_context=True)
def render_commit_row(context, commit, item, *args, **kwargs):
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
    if commit.repo.commit(commit.repo.active_branch.name).name_rev != commit.name_rev:
        for ref in commit.repo.refs:
            if ref.commit.name_rev == commit.name_rev:
                commit = ref.name
                break
        if not commit:
            commit = commit_id
    else:
        commit = commit_ref
    project = context['project'].name
    return {'project':project, 'image':item.type, 'name':item.name, 'path':item.path, 'age':age, 'message':message, 'author':author, 'static_url':static_url, 'commit':commit}

@register.inclusion_tag('projects/breadcrumb.html', takes_context=True)
def breadcrumb(context):
    if 'blob' in context:
        item = context['blob']
    else:
        item = context['tree']
    commit = context['commit']
    commit_id, commit_ref = commit.name_rev.split(' ')
    if commit.repo.commit(commit.repo.active_branch.name).name_rev != commit.name_rev:
        for ref in commit.repo.refs:
            if ref.commit.name_rev == commit.name_rev:
                commit = ref.name
                break
        if not commit:
            commit = commit_id
    else:
        commit = commit_ref
    breadcrumb = []
    cdir = ''
    for item in item.path.split('/'):
        if cdir == '':
            cdir = item
        else:
            cdir += '/'+item
        breadcrumb.append({'path':cdir, 'name':item})
    return {'project':context['project'],'breadcrumb':breadcrumb, 'commit':commit}
    