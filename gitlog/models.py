'''
Created on Oct 25, 2011

@author: masarliev
'''
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
class Project(models.Model):
    owner = models.ForeignKey(User, related_name='owner', blank=True, null=True)
    writable = models.ManyToManyField(User, related_name='writable')
    readonly = models.ManyToManyField(User, related_name='readonly')
    name = models.CharField(_("name"), max_length=30, unique=True,help_text=_("Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters"))
    public = models.BooleanField(_('private'))
    url = models.URLField(_("url"), max_length=30, blank=True, null=True, verify_exists=True)
    description = models.TextField(blank=True, null=True)
    def __unicode(self):
        return self.name