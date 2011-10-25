'''
Created on Oct 25, 2011

@author: masarliev
'''
from django.core.management.base import BaseCommand, CommandError
from gitlog.models import Project
from gitlog import settings
from git import Repo
from django.contrib.auth.models import User
import ConfigParser
import io
import random
import string
class Command(BaseCommand):
    args = '<oldrev newrev refname>'
    help = 'Update project'

    def handle(self, *args, **options):
        oldrev, newrev, refname, repository = args
        if repository == 'gitosis-admin':
            repo = Repo('%sgitosis-admin.git' % getattr(settings, 'REPOSITORY_DIR'))
            assert repo.bare == True
            blob = repo.head.commit.tree[0]
            config = ConfigParser.RawConfigParser(allow_no_value=True)
            config.readfp(io.BytesIO(blob.data_stream.read()))
            for section in config.sections():
                if config.has_option(section, 'members'):
                    username = section.replace('group ', '')
                    user, created = User.objects.get_or_create(username=username)
                    if created:
                        password = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(8))
                        user.set_password(password)
                        user.save()
                        self.stdout.write('Created user: username "%s"; password "%s"\n' % (username, password))
                if config.has_option(section, 'writable'):
                    for option, items in config.items(section):
                        if option == 'writable':
                            username = section.replace('group ', '')
                            repos = items.split(' ')
                            for repo in repos:
                                user = User.objects.get(username=username)
                                project, created = Project.objects.get_or_create(name=repo, owner=user)
                                if created:
                                    project.source = True
                                    project.private = True
                                    project.owner = user
                                    project.save()
                                    self.stdout.write('Created project: "%s"\n' % repo)
                    