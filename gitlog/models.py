'''
Created on Oct 25, 2011

@author: masarliev
'''
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from gitlog import settings
import datetime
class Project(models.Model):
    owner = models.ForeignKey(User, related_name='owner', blank=True, null=True)
    writable = models.ManyToManyField(User, related_name='writable')
    readonly = models.ManyToManyField(User, related_name='readonly')
    name = models.CharField(_("name"), max_length=30, unique=True,help_text=_("Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters"))
    public = models.BooleanField(_('private'))
    url = models.URLField(_("url"), max_length=30, blank=True, null=True, verify_exists=True)
    description = models.TextField(blank=True, null=True)
    def __unicode__(self):
        return self.name
    
    @property
    def giturl(self):
        return 'git://%s/%s.git' % (getattr(settings, 'DOMAIN'), self.name)
    
    @property
    def sshurl(self):
        return '%s@%s:%s.git' % (getattr(settings, 'GITOSIS_USER'), getattr(settings, 'DOMAIN'), self.name)
    
    
class Push(models.Model):
    project = models.ForeignKey(Project)
    oldrev = models.CharField(_('old revision'), max_length=40)
    newrev = models.CharField(_('new revision'), max_length=40)
    reference = models.CharField(_('reference'), max_length=150)
    timestamp = models.DateTimeField()
    
    def save(self):
        self.timestamp = datetime.datetime.today()
        super(Push, self).save()