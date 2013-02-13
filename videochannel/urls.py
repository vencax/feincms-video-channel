from django.conf.urls.defaults import url, patterns
from feeds import LatestVideosFeed
import views
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url('^$', views.IndexView.as_view(),
        name='videoch-index'),

    url('^cat-(?P<slug>[-\w]+)/$', views.IndexView.as_view(),
        name='videoch-category'),

    url('^(?P<slug>[-\w]+)/$', views.DetailView.as_view(),
        name='videoch-detail'),

    url(r'^youtubeconv/$', login_required(views.YoutubeConvView.as_view()),
        name='videoch-youtubeconv'),

    url('^subdownload/$', views.DownloadSubView.as_view(),
        name='videoch-sub-download'),

    url(r'^feed/$', LatestVideosFeed(),
        name='videoch-feed'),
)
