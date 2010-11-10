from django.template import Context, loader
from django.conf import settings
from django import http

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
        'MEDIA_URL': settings.MEDIA_URL
    })))
