'''
Created on Sep 12, 2012

@author: vencax
'''
from django.contrib.sitemaps import Sitemap
from feincms.content.application.models import app_reverse
from videochannel.models import Video


class VideoSitemap(Sitemap):
    """Sitemap for the Video media file."""

    def items(self):
        return Video.objects.all()

    def lastmod(self, obj):
        return obj.mediaFile.created

    def location(self, item):
        return app_reverse('videoch-detail', 'videochannel.urls',
                           kwargs={'slug': item.slug})
