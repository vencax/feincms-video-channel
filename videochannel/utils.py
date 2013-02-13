'''
Created on Aug 8, 2012

@author: vencax
'''
from django.contrib import admin
from django.http import HttpResponse
from django.utils import simplejson
from django.utils.decorators import wraps


class FcmsMixin(object):
    """
    This mixin autodetects whether the blog is integrated through an
    ApplicationContent and automatically switches to inheritance2.0
    if that's the case.

    Additionally, it adds the view instance to the template context
    as ``view``.

    This requires at least FeinCMS v1.5.
    """

    def get_context_data(self, **kwargs):
        kwargs.update({'view': self})
        return super(FcmsMixin, self).get_context_data(**kwargs)

    def render_to_response(self, context, **response_kwargs):
        if 'app_config' in getattr(self.request, '_feincms_extra_context', {}):
            return self.get_template_names(), context

        return super(FcmsMixin, self).render_to_response(
            context, **response_kwargs)


def reverse(viewname, *args, **kwargs):
    try:
        from feincms.content.application.models import app_reverse
        return app_reverse(viewname, 'vxkmoodle.urls', *args, **kwargs)
    except ImportError:
        from django.core.urlresolvers import reverse
        return reverse(viewname, *args, **kwargs)


def permalink(func):
    @wraps(func)
    def inner(*args, **kwargs):
        bits = func(*args, **kwargs)
        return reverse(bits[0], bits[1], kwargs=bits[2])
    return inner


class InitialFieldsMixin(object):
    """ This is hack from Django snippents
    NOTE: This gonna be removed as soon as django allow specify
    initials on the go...
    """
    def get_form(self, request, obj=None, **kwargs):
        form = admin.ModelAdmin.get_form(self, request, obj, **kwargs)
        if request.method != 'GET' or not hasattr(self.__class__, 'initial'):
            return form

        old_init = form.__init__

        def new_init(_self, *args, **kwargs):
            if 'instance' not in kwargs:
                for field_name, callback in self.__class__.initial.iteritems():
                    kwargs['initial'][field_name] = \
                        callback(self, request, obj, **kwargs)
            return old_init(_self, *args, **kwargs)
        form.__init__ = new_init

        return form


class JsonResponse(HttpResponse):
    """
    Http response which has JSON content.
    """
    mimetype = 'application/json; charset=utf8'

    def __init__(self, data, status=None):
        content = simplejson.dumps(data, indent=2, ensure_ascii=False)
        super(JsonResponse, self).__init__(content=content,
                                           mimetype=self.mimetype,
                                           status=status)
