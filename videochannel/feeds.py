from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.utils.translation import ugettext_lazy as _
from feincms.module.medialibrary.models import MediaFile
from feincms.content.application.models import app_reverse

site = Site.objects.get_current()


class LatestVideosFeed(Feed):
    """An Atom 1.0 feed of the latest ten videos on the channel."""

    feed_type = Atom1Feed
    title = u'%s: %s' % (site.name, _('Latest videos'))
    
    def link(self):
        return app_reverse('videoch-feed', 'videochannel.urls') 
        
    def items(self):
        return MediaFile.objects.filter(type__in=['video'])\
            .order_by('-created')[:10]

    def item_pubdate(self, item):
        return item.created

    def item_link(self, item):
        return app_reverse('videoch-detail', 'videochannel.urls', 
                           kwargs={'mfile_id': item.id,})