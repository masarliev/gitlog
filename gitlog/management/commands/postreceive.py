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
            config = ConfigParser.RawConfigParser()
            config.readfp(io.BytesIO(blob.data_stream.read()))
            for section in config.sections():
                if config.has_option(section, 'members') and (config.has_option(section, 'writable') or config.has_option(section, 'readonly')):
                    for option, items in config.items(section):
                        if option == 'writable' or option == 'readonly':
                            repos = items.split(' ')
                            for repo in repos:
                                project, created = Project.objects.get_or_create(name=repo)
                                if created:
                                    if config.has_section('repo %s' % repo):
                                        for option, items in config.items('repo %s' % repo):
                                            if option == 'owner':
                                                user, created = self.get_or_create_user(username=items.split(' ')[0])
                                                project.owner = user
                                                project.save()
                                            if option == 'description':
                                                project.description = items
                                                project.save()
                                            if option == 'url':
                                                project.url = items
                                                project.save()
                                    self.stdout.write('Created project: "%s"\n' % repo)
                                
                                for type, items in config.items(section):
                                    if type == 'members':
                                        users = items.split(' ')
                                        for repouser in users:
                                            if repouser.startswith('@'):
                                                user, created = self.get_or_create_user(repouser.replace('@', ''))
                                                if option == 'writable':
                                                    project.writable.add(user)
                                                if option == 'readonly':
                                                    project.readonly.add(user)
                                                project.save()
    def get_or_create_user(self, username):
        user, created = User.objects.get_or_create(username=username)
        if created:
            password = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(8))
            user.set_password(password)
            user.save()
            self.stdout.write('Created user: username "%s"; password "%s"\n' % (username, password))
        return user, created