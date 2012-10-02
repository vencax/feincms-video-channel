'''
Created on Sep 13, 2012

@author: vencax
'''
from django import forms
import re
import os
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import pickle

CONV_INFO_FOLDER = '_vidConversion'
f = os.path.join(settings.MEDIA_ROOT, CONV_INFO_FOLDER)
if not os.path.exists(f):
    os.mkdir(f)

class YTConvForm(forms.Form):
    videoURL = forms.CharField(label=_('video URL'), 
                               help_text=_('paste address bar content of the page with the video'))
    videoName = forms.CharField(required=False, label=_('video name'), 
                               help_text=_('paste name of the video (optional)'))
    subtitlesURL = forms.CharField(required=False, label=_('subtitles URL'), 
                               help_text=_('paste address on which the subtitles to this video are (optional)'))
    
    def clean(self):
        cleaned = super(YTConvForm, self).clean()
        videoURL = cleaned['videoURL']
        try:
            vidID = re.search('v=(?P<id>[^&]*)', videoURL).group(1)
        except AttributeError:
            raise ValidationError(_('bad youtuybe video URL'))
        vidFile = os.path.join(settings.MEDIA_ROOT, '_vidConversion', vidID)
        with open(vidFile, 'w') as f:
            pickle.dump((videoURL, cleaned['videoName'], cleaned['subtitlesURL']), f)

            
class SubDownloadForm(forms.Form):
    desiredType = forms.ChoiceField(label=_('desired format'), choices=(
        ('SRT', 'SRT'),
        ('PLAIN', 'PLAIN')
    ))
    videoURL = forms.CharField(label=_('video URL'))
    lang = forms.ChoiceField(label=_('subtitle language'), choices=(
        ('cs', 'czech'),
    ))