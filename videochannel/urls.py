from django.conf.urls.defaults import url, patterns
from feeds import LatestVideosFeed
import views

urlpatterns = patterns('',                       
    url('^$', views.IndexView.as_view(), name='videoch-index'),
    url('^cat-(?P<slug>[-\w]+)/$', views.IndexView.as_view(), name='videoch-category'),
    url('^(?P<mfile_id>\d+)/$', views.DetailView.as_view(), name='videoch-detail'),
    url(r'^feed/$', LatestVideosFeed(), name='videoch-feed'),
)
