import re
import urllib2
import StringIO
from django.views.generic.base import TemplateView
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404
from django.views.generic.edit import FormView
from django.http import HttpResponse, HttpResponseServerError
from django.contrib import messages

from .utils import FcmsMixin
from .forms import YTConvForm, SubDownloadForm
from .models import Video


class IndexView(FcmsMixin, TemplateView):
    template_name = 'videochannel/index.html'

    def get_context_data(self, **kwargs):
        foundmedia = Video.objects.all().order_by('-mediaFile__created')

        paginator = Paginator(foundmedia, 8)
        page = self.request.GET.get('page')
        try:
            found = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            found = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results
            found = paginator.page(paginator.num_pages)

        kwargs.update({'found': found})
        return super(IndexView, self).get_context_data(**kwargs)


class DetailView(FcmsMixin, TemplateView):
    template_name = 'videochannel/detail.html'

    def get_context_data(self, **kwargs):
        rv = super(DetailView, self).get_context_data(**kwargs)
        mfile = get_object_or_404(Video, slug=self.kwargs['slug'])
        rv.update({'fm': mfile})
        return rv


class YoutubeConvView(FcmsMixin, FormView):

    template_name = 'videochannel/conv.html'
    form_class = YTConvForm
    success_url = '.'

    def form_valid(self, form):
        messages.info(self.request, _('Video was added for conversion'))
        return super(YoutubeConvView, self).form_valid(form)


class DownloadSubView(FcmsMixin, FormView):

    template_name = 'videochannel/sub_download.html'
    form_class = SubDownloadForm
    success_url = '.'
    url = 'http://video.google.com/\
timedtext?hl=%(LANG)s&v=%(ID)s&lang=%(LANG)s'

    def form_valid(self, form):
        vidurl = form.cleaned_data['videoURL']
        if re.search('www.youtube.com', vidurl) != None:
            vid = re.search('v=(?P<vid>[-\w]+)', vidurl).group('vid')
            url = self.url % {'LANG': form.cleaned_data['lang'], 'ID': vid}
        try:
            remoteStr = urllib2.urlopen(url, timeout=3)
            outStr = StringIO.StringIO()
            if remoteStr.code == 200:
                f = getattr(self,
                            '_save_%s' % form.cleaned_data['desiredType'])
                mime = f(remoteStr, outStr)
                return HttpResponse(unicode(outStr.getvalue()), mime)
        except Exception, e:
            return HttpResponseServerError(str(e))

    def _save_SRT(self, input_stream, output_stram):
        import sub2srt
        sub2srt.convert(input_stream, output_stram)

    def _save_PLAIN(self, input_stream, output_stram):
        from xml.sax import make_parser, handler

        class _Parser(handler.ContentHandler):
            def __init__(self):
                self.content = ''

            def characters(self, content):
                self.content += content

            def endElement(self, name):
                output_stram.write(self.content.replace('&quot;', '"'))
                output_stram.write('\n')
                self.content = ''

        parser = make_parser()
        parser.setContentHandler(_Parser())
        parser.parse(input_stream)

        return 'text/srtplain'
