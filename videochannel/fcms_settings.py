'''
Created on Oct 15, 2012

@author: vencax

This file is processes by vxk-cms to prevent models.py
CMS definition module extra long.
'''


def videochannel_url_app(self):
    from feincms.content.application.models import app_reverse
    return app_reverse('videoch-detail', 'videochannel.urls', kwargs={
        'slug': self.slug,
        })

app_content = ('videochannel.urls', 'VideoChannel')

available_page_contents = (
    (('NewestVideosContent', ), 'contents'),
)

url_overrides = {
    'videochannel.video': videochannel_url_app,
}
