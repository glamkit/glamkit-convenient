from django.template import Library, Node
     
register = Library()

"""
http://djangosnippets.org/snippets/889/

{% load convenient %}

{% list_to_columns people as list 3 %}
    {% for l in list %}
        <ul>
            {%for p in l %}
                <li>{{ p }}</li>
            {% endfor %}
        </ul>
    {% endfor %}

"""

class SplitListNode(Node):
    def __init__(self, list, cols, new_list):
        self.list, self.cols, self.new_list = list, cols, new_list

    def split_seq(self, list, cols=2):
        start = 0 
        for i in xrange(cols): 
            stop = start + len(list[i::cols]) 
            yield list[start:stop] 
            start = stop

    def render(self, context):
        context[self.new_list] = self.split_seq(context[self.list], int(self.cols))
        return ''

def list_to_columns(parser, token):
    """Parse template tag: {% list_to_columns list as new_list 2 %}"""
    bits = token.contents.split()
    if len(bits) != 5:
        raise TemplateSyntaxError, "list_to_columns list as new_list 2"
    if bits[2] != 'as':
        raise TemplateSyntaxError, "second argument to the list_to_columns tag must be 'as'"
    return SplitListNode(bits[1], bits[4], bits[3])
    
list_to_columns = register.tag(list_to_columns)