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
from pygments import highlight
from pygments.lexers import guess_lexer_for_filename
from pygments.lexers.text import DiffLexer
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound
from pygments.lexers.special import TextLexer
from django.core.urlresolvers import reverse
from git import Actor, TagReference
DATE_FORMAT = '%d %b %Y %H:%M:%S'
@stringfilter
def timetodate(value):
    return datetime.datetime.fromtimestamp(int(value))
register.filter('timetodate', timetodate)

@stringfilter
def substr(value, arg):
    return value[:int(arg)]
register.filter('substr', substr)

@register.simple_tag(takes_context=True)
def user_link(context, value):
    user = None
    if isinstance(value, User):
        user = value
    if not user and isinstance(value, Actor):
        try:
            user = User.objects.get(email=value.email)
        except :
            pass
    if not user and isinstance(value, str):
        try:
            user = User.objects.get(email=value)
        except :
            pass
    if not user:
        return value
    return '<a href="%s">%s</a>' % (reverse('gitlog_account_dashboard', args=[user.username]), user.username)

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
    reference = True
    type = _('branch')
    for ref in commit_obj.repo.refs:
        if ref.commit.name_rev == commit_obj.name_rev:
            commit = ref.name
            if isinstance(ref, TagReference):
                type = _('tag')
            reference = True
            break
    if not commit:
        commit = commit_id
        reference = False
    return {'reference':reference, 'name':commit, 'commit':commit_obj, 'project':context['project'], 'type':type, 'commit_id':commit_id, 'STATIC_URL':context['STATIC_URL']}
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


@register.filter
def convert_bytes(bytes):
   abbrevs = (
        (1<<50L, 'PB'),
        (1<<40L, 'TB'),
        (1<<30L, 'GB'),
        (1<<20L, 'MB'),
        (1<<10L, 'kB'),
        (1, 'bytes')
   )
   if bytes == 1:
        return '1 byte'
   for factor, suffix in abbrevs:
        if bytes >= factor:
            break
   return '%.*f %s' % (1, bytes / factor, suffix)

    
def highlight_blob(blob):
    try:
        lexer = guess_lexer_for_filename(blob.name, blob.data_stream.read())
    except ClassNotFound:
        lexer = TextLexer()
    formater = HtmlFormatter(nobackground=True,linenos='table', cssclass="source")
    return "<style>%s</style>%s" % (formater.get_style_defs('.source'), highlight(blob.data_stream.read(), lexer, formater))
register.filter('highlight', highlight_blob)

@register.inclusion_tag('projects/readme.html', takes_context=True)
def readme(context):
    commit = context['commit']
    if 'README.md' in commit.tree:
        blob = commit.tree['README.md']
        return {'blob':blob, 'content':blob.data_stream.read(), 'md':True}
    if 'README.rst' in commit.tree:
        blob = commit.tree['README.rst']
        return {'blob':blob, 'content':blob.data_stream.read(), 'rst':True}
    
    return {'blob':False}

@register.filter
def diffstat_bar(stats):
    output = ''
    if int(stats['lines']) <= 5:
        output += '<span class="plus">&bull;</span>' * int(stats['insertions'])
        output += '<span class="minus">&bull;</span>' * int(stats['deletions'])
    else:
        stl = int(stats['lines']) / float(5) 
        if int(stats['insertions']) != 0:
            mp = int(int(stats['insertions'])/stl)
            output += '<span class="plus">&bull;</span>' * mp
        if int(stats['deletions']) != 0:
            mp = int(int(stats['deletions'])/stl)
            output += '<span class="minus">&bull;</span>' * mp
        
    return output  
diffstat_bar.is_safe = True

@register.filter
@stringfilter
def diffstat(filepath,statsfiles):
    output = ''
    for file, stats in statsfiles.items():
        if file == filepath:
            output += '<a href="#diff-0" class="tooltipped leftwards" title="%s additions &amp; %s deletions">' % (stats['insertions'], stats['deletions'])
            output += '<span class="diffstat-summary">%s &nbsp; </span>' % stats['lines']
            output += '<span class="diffstat-bar">%s</span>' % diffstat_bar(stats)
            output += '</a>'
            return output
    return output
    
@register.filter
def highlight_diff(content, filename):
    formater = HtmlFormatter(nobackground=True, cssclass="source")
    return "<style>%s</style>%s" % (formater.get_style_defs('.source'), highlight(content, DiffLexer(), formater))