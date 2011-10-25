'''
Created on Oct 25, 2011

@author: masarliev
'''
from gitlog.decorators import auto_render
from gitlog.models import Project
from gitlog import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
@auto_render
def home(request):
    if(request.user.is_authenticated()):
        projects = Project.objects.filter(owner=request.user)
        return 'account/dashboard.html', {'projects':projects}
    else:
        if not getattr(settings, 'PUBLIC_ACCESS'):
            return HttpResponseRedirect(reverse('gitlog_login'))
        return 'account/dashboard_anonymous.html', {}