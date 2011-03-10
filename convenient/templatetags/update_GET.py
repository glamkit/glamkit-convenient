"""
Greg's magic get_string template tag allows you to substitute parameters into the current request's GET url.

{% load update_GET %}

<a href="?{% update_GET attr1 += value1 attr2 -= value2 attr3 = value3 %}">foo</a>
This adds value1 to (the list of values in) attr1,
removes value2 from (the list of values in) attr2,
sets attr3 to value3.

And returns a urlencoded GET string.

Allowed values are:
    strings, in quotes
    vars that resolve to strings
    lists of strings
    None (without quotes)
    
If a attribute is set to None or an empty list, the GET parameter is removed.
If an attribute's value is an empty string, or [""], the value remains, but has a "" value.
If you try to =- a value from a list that doesn't contain that value, nothing happens.
If you try to =- a value from a list where the value appears more than once, only the first value is removed.
If you try to += None, the value is cleared.
"""
from django import template
from django.utils.http import urlquote
from django.template.defaultfilters import fix_ampersands
from django.http import QueryDict

register = template.Library()

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


class UpdateGetNode(template.Node):
    def __init__(self, triples=[]):
        self.triples = [(template.Variable(attr), op, template.Variable(val)) for attr, op, val in triples]

    def render(self, context):
        try:
            GET = context.get('request').GET.copy()
        except AttributeError:
            GET = QueryDict("", mutable=True)

        for attr, op, val in self.triples:
            actual_attr = attr.resolve(context)
            
            try:
                actual_val = val.resolve(context)
            except:
                if val.var == "None":
                    actual_val = None
                else:
                    actual_val = val.var
            
            if actual_attr:
                if op == "=":
                    if actual_val is None or actual_val == []:
                        if GET.has_key(actual_attr):
                            del GET[actual_attr]
                    elif hasattr(actual_val, '__iter__'):
                        GET.setlist(actual_attr, actual_val)
                    else:
                        GET[actual_attr] = unicode(actual_val)
                elif op == "+=":
                    if actual_val is None or actual_val == []:
                        if GET.has_key(actual_attr):
                            del GET[actual_attr]
                    elif hasattr(actual_val, '__iter__'):
                        GET.setlist(actual_attr, GET.getlist(actual_attr) + list(actual_val))
                    else:
                        GET.appendlist(actual_attr, unicode(actual_val))
                elif op == "-=":
                    li = GET.getlist(actual_attr)
                    if hasattr(actual_val, '__iter__'):
                        for v in list(actual_val):
                            if v in li:
                                li.remove(v)
                        GET.setlist(actual_attr, li)
                    else:
                        actual_val = unicode(actual_val)
                        if actual_val in li:
                            li.remove(actual_val)
                        GET.setlist(actual_attr, li)

        return fix_ampersands(GET.urlencode())

def do_update_GET(parser, token):
    try:
        args = token.split_contents()[1:]
        triples = list(chunks(args, 3))
        if triples and len(triples[-1]) != 3:
            raise template.TemplateSyntaxError, "%r tag requires arguments in groups of three (op, attr, value)." % token.contents.split()[0]
        ops = set([t[1] for t in triples])
        if not ops <= set(['+=', '-=', '=']):
            raise template.TemplateSyntaxError, "The only allowed operators are '+=', '-=' and '='. You have used %s" % ", ".join(ops)
                    
    except ValueError:
        return UpdateGetNode()
   
    return UpdateGetNode(triples)

        
register.tag('update_GET', do_update_GET)
