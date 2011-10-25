'''
Created on Oct 25, 2011

@author: masarliev
'''
from django.conf import settings
TITLE = getattr(settings, 'GITLOG_TITLE', 'GitLog')
PUBLIC_ACCESS = getattr(settings, 'GITLOG_PUBLIC_ACCESS', False)
REPOSITORY_DIR = getattr(settings, "GITLOG_REPOSITORY_DIR", '/home/git/repositories/')