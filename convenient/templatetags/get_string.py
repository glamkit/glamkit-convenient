"""
Greg's magic get_string template tag allows you to substitute one parameter into a GET url
{% load get_string %}

<a href="?{% get_string "page" record_page.next_page_number %}">previous</a>

If the value of the parameter is null, it removes that parameter. It also does ampersand encoding

"""
from django import template
from django.utils.http import urlquote
from django.template.defaultfilters import fix_ampersands
from django.http import QueryDict

register = template.Library()

def zigzag(seq):
    """ returns odd values, even values """
    return seq[::2], seq[1::2]

def do_get_string(parser, token):
    import warnings
    warnings.warn("'get_string' is deprecated. use 'update_GET'", DeprecationWarning)
    try:
        # tag_name, key, value = token.split_contents()
        args = token.split_contents()[1:]
#         key = urlquote(key)
#         value = urlquote(value)
    except ValueError:
        return GetStringNode()
   
    return GetStringNode(*args)

class GetStringNode(template.Node):
    def __init__(self, *args):
        
        keys, values = zigzag(args)        

        keys = [template.Variable(k) for k in keys]
        values = [template.Variable(v) for v in values]

        self.new_values = dict(zip(keys, values))
                        
    def render(self, context):
        try:
            get = context.get('request').GET.copy()
        except AttributeError:
            get = QueryDict("", mutable=True)
        
        for k, v in self.new_values.iteritems():
            actual_key = k.resolve(context)
            actual_value = v.resolve(context)
            if actual_value:
                get[actual_key] = actual_value
            else:
                if actual_key in get:
                    del get[actual_key]
        
        return fix_ampersands(get.urlencode())
        
register.tag('get_string', do_get_string)

