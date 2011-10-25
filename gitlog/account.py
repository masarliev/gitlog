'''
Created on Oct 25, 2011

@author: masarliev
'''
from django.contrib.auth.decorators import login_required
from gitlog.decorators import auto_render

@login_required
@auto_render
def dashboard(request):
    return 'account/dashboard.html', {}
@login_required
@auto_render
def settings(request):
    return 'account/settings.html', {}