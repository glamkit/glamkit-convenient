from django import http
from django.conf import settings
from django.conf.urls.defaults import url
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.template import Context, loader

def handler_500_with_media(request, template_name='500.html'):
    """
    500 error handler allowing access to MEDIA_URL.

    Templates: `500.html`
    Context:
        MEDIA_URL
            Path of static media (e.g. "media.example.org")
    """
    t = loader.get_template(template_name) # You need to create a 500.html template.
    return http.HttpResponseServerError(t.render(Context({
        'MEDIA_URL': settings.MEDIA_URL,
        'STATIC_URL': settings.STATIC_URL,
    })))

def relative_view_on_site(request, content_type_id, object_id):
    """
    Redirect to an object's page based on a content-type ID and an object ID,
    always using a relative path, thus not requiring the Sites framework to be
    set up. To use, add the following entry in the URLconf above the admin URL
    declaration (or use `relative_view_on_site_urls`):
    
    url(r'^admin/r/(?P<content_type_id>\d+)/(?P<object_id>.+)/$',
        'convenient.views.relative_view_on_site'),
    
    The code is almost entirely copied from the shortcut() view in 
    django.contrib.contenttypes.views
    """
    try:
        content_type = ContentType.objects.get(pk=content_type_id)
        if not content_type.model_class():
            raise http.Http404("Content type %s object has no associated model" % content_type_id)
        obj = content_type.get_object_for_this_type(pk=object_id)
    except (ObjectDoesNotExist, ValueError):
        raise http.Http404("Content type %s object %s doesn't exist" % (content_type_id, object_id))
    try:
        return http.HttpResponseRedirect(obj.get_absolute_url())
    except AttributeError:
        raise http.Http404("%s objects don't have get_absolute_url() methods" % content_type.name)

relative_view_on_site_urls = url(
    r'^admin/r/(?P<content_type_id>\d+)/(?P<object_id>.+)/$',
    'convenient.views.relative_view_on_site',
)