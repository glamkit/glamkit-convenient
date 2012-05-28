from django import template
register = template.Library()

from urlparse import urlparse

def domain_only(full_url):
    parsed = urlparse(full_url)
    return parsed.netloc.lstrip("www.")

register.filter('domain_only', domain_only)