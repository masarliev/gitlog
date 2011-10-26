'''
Created on Oct 25, 2011

@author: masarliev
'''
from gitlog.decorators import auto_render
from django.contrib.auth.decorators import login_required
from gitlog.models import Project
from gitlog.forms import ProjectForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from gitlog import settings
import git
from git.db import GitCmdObjectDB
@auto_render
@login_required
def create(request):
    projects = Project.objects.filter(owner=request.user)
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.source = True
            obj.save()
            return HttpResponseRedirect(reverse('gitlog_project_tree', args=[obj.owner, obj.name]));
    else:
        form = ProjectForm()
    return 'projects/create.html', {'projects':projects, 'form':form}

@auto_render
@login_required
def tree(request, project):
    project = get_object_or_404(Project, name=project)
    repo = git.Repo('%s%s.git' %(getattr(settings, 'REPOSITORY_DIR'), project.name), odbt=GitCmdObjectDB)
    assert repo.bare == True
    commit = repo.heads.master.commit
    return 'projects/tree.html', {'project':project, 'repo':repo, 'commit':commit}