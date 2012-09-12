from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from feincms.module.medialibrary.models import MediaFile

class NewestVideoChannelContent(models.Model):
    count = models.IntegerField(verbose_name=_('video count'), default=5,
                                help_text=_('count of videos to show.'))
    
    class Meta:
        abstract = True # Required by FeinCMS, content types must be abstract
        verbose_name=_('newest videos content')

    def render(self, **kwargs):
        found = MediaFile.objects.filter(type__in=['video'])\
            .order_by('-created')[:self.count]
        return render_to_string('videochannel/newestvideos.html', {
            'content': self, # Not required but a convention followed by
                             # all of FeinCMS' bundled content types
            'found': found,
        })