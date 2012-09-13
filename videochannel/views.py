
from django.views.generic.base import TemplateView
from django.utils.translation import ugettext_lazy as _
from feincms.module.medialibrary.models import MediaFile
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404
from django.views.generic.edit import FormView

from .utils import FcmsMixin
from .forms import YTConvForm
from django.contrib import messages

# -----------------------------------------------------------------------------   

class IndexView(FcmsMixin, TemplateView):
    template_name = 'videochannel/index.html'
    presented_types = ['video']

    def get_context_data(self, **kwargs):
        foundmedia = MediaFile.objects.filter(type__in=self.presented_types)\
            .order_by('-created')
            
        paginator = Paginator(foundmedia, 8)
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

class YoutubeConvView(FcmsMixin, FormView):
        
    template_name = 'videochannel/conv.html'
    form_class = YTConvForm
    success_url = '.'

    def form_valid(self, form):
        messages.info(self.request, _('Video was added for conversion'))
        return super(YoutubeConvView, self).form_valid(form)

# -----------------------------------------------------------------------------