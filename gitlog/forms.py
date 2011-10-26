'''
Created on Oct 25, 2011

@author: masarliev
'''
from django import forms
from gitlog.models import Project
from django.utils.translation import ugettext_lazy as _
class ProjectForm(forms.ModelForm):
    name = forms.RegexField(label=_("Name"), max_length=30, regex=r'^[\w.@+-]+$',
        help_text = _("Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only."),
        error_messages = {'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")})
    class Meta:
        model = Project
        exclude = ('owner',)
        fields = ("name",)