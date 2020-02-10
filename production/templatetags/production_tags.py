from django import template

from production.models import Production, ROLE_CHOICES

register = template.Library()

ROLE_CHOICES_DICT = dict(ROLE_CHOICES)


@register.filter()
def role_display(role_id):
    return ROLE_CHOICES_DICT.get(role_id, role_id)


def checkBitsCount(bits,count):
    if len(bits) != count:
        raise template.TemplateSyntaxError('%s tag requires %d arguments' % (bits[0],(count-1)))
        return False
    if bits[count-2] != 'as':
        raise template.TemplateSyntaxError("before-last argument to %s tag must be 'as'" % bits[0])
        return False
    return True

class productions(template.Node):
    def __init__(self, onstage, context_var):
        self.context_var = context_var
        self.onstage = onstage
    
    def render(self, context):
        context[self.context_var] = Production.objects.exclude(title__isnull=True,).filter(is_staging=self.onstage, is_public=True, kind__is_performative=True)[:3]
        return ''
        
def do_get_article(parser, token):
    """
    Populates a template variable with a ``Instance`` of an Article with the
    designated id
    Usage::
      {% instance [id] as [varname] %}
    Example::
      {% get_article 1 as genres %}
    """
    bits = token.contents.split()
    if checkBitsCount(bits,4):
      return InstanceNode(Article, bits[1], bits[3])
    

def do_get_productions(parser, token):
  bits = token.contents.split()
  if checkBitsCount(bits,4):
    return productions(bits[1],bits[3])
    
register.tag('get_productions', do_get_productions)
