from django.conf import settings

def site_info(param):
    return { 'SITE_NAME': settings.SITE_NAME,
             'SITE_URL': settings.SITE_URL, }