'''
Created on Oct 25, 2011

@author: masarliev
'''
from django.contrib.auth.decorators import login_required
from gitlog.decorators import auto_render
from django.db.models import Q
from gitlog.models import Project
@login_required
@auto_render
def dashboard(request):
    projects = Project.objects.filter(Q(writable=request.user)|Q(readonly=request.user))            
    return 'account/dashboard.html', {'projects':projects}
@login_required
@auto_render
def settings(request):
    return 'account/settings.html', {}