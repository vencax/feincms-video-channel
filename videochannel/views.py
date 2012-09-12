
from django.views.generic.base import TemplateView


from .utils import FcmsMixin
from feincms.module.medialibrary.models import MediaFile
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404

# -----------------------------------------------------------------------------   

class IndexView(FcmsMixin, TemplateView):
    template_name = 'videochannel/index.html'
    presented_types = ['video']

    def get_context_data(self, **kwargs):
        foundmedia = MediaFile.objects.filter(type__in=self.presented_types)\
            .order_by('-created')
            
        paginator = Paginator(foundmedia, 10)
        page = self.request.GET.get('page')
        try:
            found = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            found = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            found = paginator.page(paginator.num_pages)
                
        kwargs.update({'found' : found})
        return super(IndexView, self).get_context_data(**kwargs)

# -----------------------------------------------------------------------------

class DetailView(FcmsMixin, TemplateView):
    template_name = 'videochannel/detail.html'

    def get_context_data(self, **kwargs):
        rv = super(DetailView, self).get_context_data(**kwargs)
        mfile = get_object_or_404(MediaFile,id=self.kwargs['mfile_id'])
        rv.update({'fm' : mfile})
        return rv

# -----------------------------------------------------------------------------