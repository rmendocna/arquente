#from bs4 import BeautifulSoup

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import strip_tags

from project.photologue.models import Photo
from project.content.models import Article



class SplitText(template.Node):
    def __init__(self,text,context_var):
        self.text = template.Variable(text)
        self.context_var=context_var

    def render(self,context):
      s = self.text.resolve(context).replace("\n","")
      try:
        soup = BeautifulSoup(s)
      except:
        context[self.context_var]=[s,'']
        return ''
      bsoup = [str(i) for i in soup] # big blocks
      #print bsoup
      blocks = []
      plain_chunk=''
      chunk = ''
      for p in bsoup:
        plain_chunk+=strip_tags(p)
        chunk+=p
        if len(plain_chunk.split())>=WORDS_PER_COLUMN or p == bsoup[len(bsoup)-1]:
          blocks.append(chunk)
          chunk=''
          plain_chunk=''
      context[self.context_var]=blocks
      return ''

register = template.Library()

def checkBitsCount(bits,count):
    if len(bits) != count:
        raise template.TemplateSyntaxError('%s tag requires %d arguments' % (bits[0],(count-1)))
        return False
    if bits[count-2] != 'as':
        raise template.TemplateSyntaxError("before-last argument to %s tag must be 'as'" % bits[0])
        return False
    return True

class InstanceNode(template.Node):
    def __init__(self, model, node_id, context_var):
        self.node_id = template.Variable(node_id)
        self.context_var = context_var
        self.model = model

    def render(self, context):
        context[self.context_var] = self.model.objects.filter(id=int(self.node_id.resolve(context))).exclude(title__isnull=True).get()
        return ''

class RootNodes(template.Node):
    def __init__(self, position, context_var):
        self.context_var = context_var
        self.position = position
    
    def render(self, context):
        context[self.context_var] = Article.objects.exclude(title__isnull=True,).filter(parent__isnull=True, menu=self.position, is_public=True)
        return ''

#from cca.content.forms import TellAFriend, SubscribeForm
#from ceao.registration.forms import RegistrationForm
#class GeneralForms(template.Node):
#  def __init__(self, position, context_var):
#      self.context_var = context_var
#      
#  def render(self,context):
#     from project.content.forms import TellAFriend, SubscribeForm
#     context[self.context_var] = {'tellafriend':TellAFriend(),'subscribe':SubscribeForm}
#
#from django.template.defaultfilters import stringfilter
#from django.conf import settings
#from PIL import Image, ImageChops
#from os import path, unlink
#MASK_IMAGE="img/window.jpg"
#
#def get_default_thumbnail_filename(filename):
#    dirname, ext = path.splitext(filename)
#    return dirname + '.thumb.jpg'

#@register.filter
#@stringfilter
#def window(filepath):
#    output_filename = get_default_thumbnail_filename(filepath)
#    if path.exists(output_filename) and path.getmtime(filepath)>path.getmtime(output_filename):
#          unlink(output_filename)
#    output_url = path.join(settings.MEDIA_URL,output_filename[len(settings.MEDIA_ROOT):])
#    assert output_url, True
#    if not path.exists(output_filename):
#        image = Image.open(filepath)
#        mask=Image.open(path.join(settings.MEDIA_ROOT, MASK_IMAGE))
#        if mask.mode not in ('L', 'RGB'):
#            mask = mask.convert('RGB')
#        if image.mode not in ('L', 'RGB'):
#            image = image.convert('RGB')
#        #if image.mode not in ('L', 'RGB'):
#        #    image = image.convert('RGB')
#        x,y = mask.size
#        #safe margins?
#        #size = (x,x) if x>y else (y,y)
#        if  x>y:
#          size = (x,x)
#        else:
#          size = (y,y)
#        image = image.resize((x,y), Image.ANTIALIAS)
#        result=ImageChops.lighter(image,mask)
#        result.save(output_filename, "JPEG")
#        output_url = path.join(settings.MEDIA_URL,output_filename[len(settings.MEDIA_ROOT):])
#    return path.join(output_url)
# 
class Illustration(template.Node):
  def __init__(self, instance, context_var=None):
    self.instance = template.Variable(instance)
    self.tag = instance
    self.context_var=context_var
          
  def render(self, context):
    try:
        return "background-image:url(%s)" % self.instance.resolve(context).illustration.get_wide_url()
    except:
        photo = Photo.objects.filter(is_highlight__exact=True).order_by('-date_added')[:1]
        if self.context_var:
            context[self.context_var] = "background-image:url(%s)" % photo[0].get_wide_url()
            return ''
        else:
            return "background-image:url(%s)" % photo[0].get_wide_url()

#class PreviousMonths(template.Node):
#  def __init__(self, context_var):
#      self.context_var = context_var
#  
#  def render(self, context):
#    from project.content.models import News
#    from datetime import date
#    t=date.today().replace(day=1)
#    months=[]
#    has_news=True
#    i=0
#    while has_news:
#      i+=1
#      qs = News.all_public.filter(date_pub__month=t.month,date_pub__year=t.year).values('date_pub')
#      if qs:
#        months.append(t)
#      else:
#        has_news=False
#      try:
#        t=t.replace(month=t.month-1)
#      except:
#        t=t.replace(year=t.year-1,month=12)
#      if i==4:
#        has_news=False
#    context[self.context_var] = months      
#    return ''
#    
#class PreviousEventsPerMonth(template.Node):
#  def __init__(self, context_var):
#      self.context_var = context_var
#      
#  def render(self,context):
#      from project.content.models import EventTime
#      from project.content.views import monthly_events
#      from datetime import date
#      t=date.today().replace(day=1)
#      months=[]
#      has_event=True
#      i=0
#      while has_event:
#        i+=1
#        qs = monthly_events(t)
#        if qs:
#            months.append(t)
#        else:
#            has_event=False
#        try:
#            t=t.replace(month=t.month-1)
#        except:
#            t=t.replace(year=t.year-1,month=12)
#        if i==4:
#            has_event=False
#      context[self.context_var] = months
#      return ''
#      
#class GetSubscribeForm(template.Node):
#  def __init__(self, context_var):
#      self.context_var = context_var
#      
#  def render(self, context):
#    #from project.content.forms import SubscribeForm
#    #context[self.context_var] = SubscribeForm()
#    from registration.forms import RegistrationFormUniqueEmail
#    context[self.context_var] = RegistrationFormUniqueEmail()
#    return ''
        
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
    
#def do_get_event(parser, token):
#    bits = token.contents.split()
#    if checkBitsCount(bits,4):
#        return InstanceNode(Event, bits[1], bits[3])

def do_get_menu(parser, token):
  bits = token.contents.split()
  if checkBitsCount(bits,4):
    return RootNodes(bits[1],bits[3])
    
#def do_get_forms(parser, token):
#  bits = token.contents.split()
#  if checkBitsCount(bits,3):   
#    return GeneralForm(bits[2])
#        
#def split_text(parser, token):
#  bits = token.contents.split()
#  if checkBitsCount(bits,4):
#      return SplitText(bits[1],bits[3])
#    
def do_get_illustration(parser, token):
  bits = token.contents.split()
  #if checkBitsCount(bits,2):
  return Illustration(bits[1])
  
#def do_get_previous_months(parser, token):
#  bits = token.contents.split()
#  if checkBitsCount(bits,3):   
#      return PreviousMonths(bits[2])
#      
#def do_get_previous_events_per_month(parser, token):
#  bits = token.contents.split()
#  if checkBitsCount(bits,3):
#      return PreviousEventsPerMonth(bits[2])
#
#def do_get_subscribe_form(parser, token):
#  bits = token.contents.split()
#  if checkBitsCount(bits,3):
#    return GetSubscribeForm(bits[2])
#

register.tag('get_article', do_get_article)
#register.tag('get_event', do_get_event)
register.tag('get_menu', do_get_menu)
#register.tag('loadforms', do_get_forms)
register.tag('get_illustration', do_get_illustration)
#register.tag('get_previous_months', do_get_previous_months)
#register.tag('get_previous_events', do_get_previous_events_per_month)
#register.tag('split_text', split_text)
#register.tag('get_subscribe_form', do_get_subscribe_form)

WORDS_PER_COLUMN = 40 # testing

def do_split_text(parser, token):
  bits = token.contents.split()
  if checkBitsCount(bits,4):
      return SplitText(bits[1],bits[3])        
    
register.tag('split_text', do_split_text)

