'''
Created on Dec 15, 2012

@author: vencax
'''
from django.db import models
from django.utils.translation import ugettext_lazy as _
from feincms.module.medialibrary.models import MediaFile
from django.db.models.signals import post_save, pre_save

from .signals import videoPostSavedHandler, videoPreSavedHandler


class Video(models.Model):

    class Meta:
        verbose_name = _('video')
        verbose_name_plural = _('videos')

    mediaFile = models.ForeignKey(MediaFile, verbose_name=_('media file'))
    thumbnail = models.ImageField(upload_to='vids_thumbs',
                                 null=True,
                                 verbose_name=_('thumbnail file'),
                                 help_text=_('Thumbnail picture of the video'))
    subtitles = models.FileField(upload_to='vids_subtitles',
                                 null=True, blank=True,
                                 verbose_name=_('subtitles file'),
                                 help_text=_('Only SRT files are supported'))
    slug = models.SlugField(_('slug'), max_length=100, blank=True)

    @models.permalink
    def get_absolute_url(self):
        return ('infoch-detail', (), {'slug': self.slug})

post_save.connect(videoPostSavedHandler, sender=Video,
                 dispatch_uid='video_post_save')
pre_save.connect(videoPreSavedHandler, sender=Video,
                 dispatch_uid='video_pre_save')
