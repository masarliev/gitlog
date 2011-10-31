'''
Created on Oct 25, 2011

@author: masarliev
'''
from gitlog.decorators import auto_render
from django.contrib.auth.decorators import login_required
from gitlog.models import Project
from django.http import  Http404
from django.shortcuts import get_object_or_404
from gitlog import settings
import git
from git.db import GitCmdObjectDB

@auto_render
@login_required
def tree(request, project, commit=None, path=None):
    project = get_object_or_404(Project, name=project)
    repo = git.Repo('%s%s.git' %(getattr(settings, 'REPOSITORY_DIR'), project.name), odbt=GitCmdObjectDB)
    assert repo.bare == True
    if not commit:
        commit = repo.commit(repo.active_branch.name)
    else:
        commit = repo.commit(commit)
    if path:
        tree = commit.tree[path]
    else:
        tree = commit.tree
    return 'projects/tree.html', {'project':project, 'repo':repo, 'commit':commit, 'tree':tree}

@auto_render
@login_required
def blob(request, project, commit=None, path=None):
    project = get_object_or_404(Project, name=project)
    repo = git.Repo('%s%s.git' %(getattr(settings, 'REPOSITORY_DIR'), project.name), odbt=GitCmdObjectDB)
    assert repo.bare == True
    commit = repo.commit(commit)
    if not path:
        raise Http404
    blob = commit.tree[path]
    return 'projects/blob.html', {'project':project, 'repo':repo, 'commit':commit, 'blob':blob}

@auto_render
@login_required
def commit(request, project, commit):
    project = get_object_or_404(Project, name=project)
    repo = git.Repo('%s%s.git' %(getattr(settings, 'REPOSITORY_DIR'), project.name), odbt=GitCmdObjectDB)
    assert repo.bare == True
    commit = repo.commit(commit)
    if commit.parents:
        parent = repo.commit(commit.parents[0])
        diff = parent.diff(commit, create_patch=True, p=True)
    else:
        diff = commit.diff(create_patch=True)
    return 'projects/commit.html', {'project':project, 'repo':repo, 'commit':commit, 'diff':diff}
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
@login_required
@auto_render
def history(request, project, commit, path=None, ):
    project = get_object_or_404(Project, name=project)
    repo = git.Repo('%s%s.git' %(getattr(settings, 'REPOSITORY_DIR'), project.name), odbt=GitCmdObjectDB)
    assert repo.bare == True
    commit = repo.commit(commit)
    page = int(request.GET.get('page', 1))
    skip = (page-1)*2
    paginator = Paginator(list(repo.iter_commits(commit, paths=path)), 20)
    try:
        history = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        history = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        history = paginator.page(paginator.num_pages)
    if path:
        item = commit.tree[path]
        if item.type == 'blob':
            return 'projects/history.html', {'project':project, 'repo':repo, 'commit':commit, 'blob':item, 'history':history}
    else:
        item = commit.tree
    return 'projects/history.html', {'project':project, 'repo':repo, 'commit':commit, 'tree':item, 'history':history}