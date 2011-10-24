'''
Created on Oct 25, 2011

@author: masarliev
'''
from django.conf.urls.defaults import url, patterns
urlpatterns = patterns('',
    url(r'^$', 'gitlog.views.home', name='gitlog_home'),
)