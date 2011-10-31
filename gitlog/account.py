'''
Created on Oct 25, 2011

@author: masarliev
'''
from django.contrib.auth.decorators import login_required
from gitlog.decorators import auto_render
from django.db.models import Q
from gitlog.models import Project, Push
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
@login_required
@auto_render
def dashboard(request):
    projects = Project.objects.filter(Q(writable=request.user)|Q(readonly=request.user))   
    feeds = Push.objects.filter(project__in=projects)     
    return 'account/dashboard.html', {'projects':projects, 'feeds':feeds}

@login_required
@auto_render
def settings(request):
    return 'account/settings.html', {}

@auto_render
@login_required
def account(request, user):
    user = get_object_or_404(User, username=user)
    return 'account/account.html', {'account':user}