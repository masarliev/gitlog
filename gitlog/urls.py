'''
Created on Oct 25, 2011

@author: masarliev
'''
from django.conf.urls.defaults import url, patterns
from django.views.generic.simple import redirect_to
urlpatterns = patterns('',
    url(r'^$', 'gitlog.views.home', name='gitlog_home'),
    url(r'^$', 'gitlog.views.home', name='gitlog_home'),
)
urlpatterns += patterns('',
    url(r'^account/login/$', 'django.contrib.auth.views.login', {'template_name': 'account/login.html'}, name="gitlog_login"),
    url(r'^account/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/account/login/'}, name="gitlog_logout"),
    url(r'^accounts/profile/$', redirect_to, {'url': '/account/'}),
)
urlpatterns += patterns('gitlog.account',
    url(r'^account/settings/$', 'settings', name="gitlog_account_settings"),
    url(r'^account/$', 'dashboard', name="gitlog_account_dashboard"),
    url(r'^account/(?P<user>[\w.@+-]+)/$', 'account', name="gitlog_account_dashboard"),
)

urlpatterns += patterns('gitlog.projects',
    url(r'^projects/create/$', 'create', name="gitlog_projects_create"),
    url(r'^(?P<project>[\w.@+-]+)/tree/$', redirect_to, {'url': '../'}),
    url(r'^(?P<project>[\w.@+-]+)/$', 'tree', name="gitlog_project_tree"),
    url(r'^(?P<project>[\w.@+-]+)/tree/(?P<commit>\w+.+)/$', 'tree', name="gitlog_project_tree"),
    url(r'^(?P<project>[\w.@+-]+)/tree/(?P<commit>\w+.+)/(?P<path>.*)$', 'tree', name="gitlog_project_tree"),
    url(r'^(?P<project>[\w.@+-]+)/blob/(?P<commit>\w+.+)/(?P<path>.*)$', 'blob', name="gitlog_project_blob"),
)