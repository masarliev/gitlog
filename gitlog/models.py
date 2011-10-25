'''
Created on Oct 25, 2011

@author: masarliev
'''
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))
class Project(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(_("name"), max_length=30, unique=True,help_text=_("Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters"))
    private = models.BooleanField(_('private'), choices=BOOL_CHOICES)
    source = models.BooleanField(_('source'), choices=BOOL_CHOICES)
    
    def __unicode(self):
        return self.name
    
    @property
    def cssclass(self):
        css = ''
        if(self.private):
            css += 'private '
        else:
            css += 'public '
        if(self.source):
            css += 'source'
        else:
            css += 'fork'
        return css