'''
Created on Sep 12, 2012

@author: vencax
'''
from django.contrib.sitemaps import Sitemap
from feincms.module.medialibrary.models import MediaFile
from feincms.content.application.models import app_reverse


class VideoSitemap(Sitemap):
    """Sitemap for the Video media file."""

    def items(self):
        return MediaFile.objects.filter(type__in=['video'])

    def lastmod(self, obj):
        return obj.created

    def location(self, item):
        return app_reverse('videoch-detail', 'videochannel.urls',
                           kwargs={'mfile_id': item.id})
