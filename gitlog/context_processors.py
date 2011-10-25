'''
Created on Apr 23, 2011

@author: root
'''
from gitlog import settings as git_settings
def gitlog(request):
    context = {}
    context['page_title'] = getattr(git_settings, 'TITLE');
    context['public_access'] = getattr(git_settings, 'PUBLIC_ACCESS');
    return context