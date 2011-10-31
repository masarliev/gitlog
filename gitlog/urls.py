'''
Created on Oct 25, 2011

@author: masarliev
'''
from django.conf.urls.defaults import url, patterns
from django.views.generic.simple import redirect_to

urlpatterns = patterns('',
    url(r'^account/login/$', 'django.contrib.auth.views.login', {'template_name': 'account/login.html'}, name="gitlog_login"),
    url(r'^account/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/account/login/'}, name="gitlog_logout"),
    url(r'^accounts/profile/$', redirect_to, {'url': '/account/'}),
)
urlpatterns += patterns('gitlog.account',
    url(r'^$', 'dashboard', name='gitlog_account_dashboard'),
    url(r'^account/settings/$', 'settings', name="gitlog_account_settings"),
    url(r'^account/$', 'dashboard', name="gitlog_account_dashboard"),
    url(r'^account/(?P<user>[\w.@+-]+)/$', 'account', name="gitlog_account_dashboard"),
    
)

urlpatterns += patterns('gitlog.projects',
    url(r'^(?P<project>[\w.@+-]+)/tree/$', redirect_to, {'url': '../'}),
    url(r'^(?P<project>[\w.@+-]+)/$', 'tree', name="gitlog_project_tree"),
    url(r'^(?P<project>[\w.@+-]+)/tree/(?P<commit>[a-zA-Z0-9_\-\.]+)/$', 'tree', name="gitlog_project_tree"),
    url(r'^(?P<project>[\w.@+-]+)/tree/(?P<commit>[a-zA-Z0-9_\-\.]+)/(?P<path>.*)$', 'tree', name="gitlog_project_tree"),
    url(r'^(?P<project>[\w.@+-]+)/blob/(?P<commit>[a-zA-Z0-9_\-\.]+)/(?P<path>.*)$', 'blob', name="gitlog_project_blob"),
    url(r'^(?P<project>[\w.@+-]+)/commit/(?P<commit>[a-zA-Z0-9_\-\.]+)/$', 'commit', name="gitlog_project_commit"),
    url(r'^(?P<project>[\w.@+-]+)/commits/(?P<commit>[a-zA-Z0-9_\-\.]+)/$', 'history', name="gitlog_project_history"),
    url(r'^(?P<project>[\w.@+-]+)/commits/(?P<commit>[a-zA-Z0-9_\-\.]+)/(?P<path>.*)$', 'history', name="gitlog_project_history"),
)