#!/usr/bin/python
# -*- coding: utf-8 -*-
          
from django.conf import settings
from django.utils.html import strip_tags
from django.utils.encoding import smart_unicode,force_unicode
from django.utils.translation import ugettext_lazy as _
from multilingual import languages
from nltk.corpus import stopwords
import string


def highlight(modeladmin,request,queryset):
    highlighted = queryset.update(is_highlight=True)
    otherset = queryset.model.objects.all().exclude(id__in=[qs.id for qs in queryset.all()])
    dimmed = otherset.update(is_highlight=False)
    #self.message_user(request,_("%s highlighted, % dimmed" % (highlighted, dimmed)))
highlight.short_description = _("Highlight selected")
                
# list of browsable Content Types, i.e., types of content that can be addressed to
from django.db import models

class Browsable(models.Manager):
  def __call__(self):
    try:
      return self.model._meta.module_name in ['article','photo','news',]
    except:
      return False
                      
import re     
# matches a character entity reference (decimal numeric, hexadecimal numeric, or named).  
charrefpat = re.compile(r'&(#(\d+|x[\da-fA-F]+)|[\w.:-]+);?')  
def decode(text):  
    """ 
        Decode HTML entities in the given. 
        text should be a unicode string, as that is what we insert. 
 
        This is from: 
            http://zesty.ca/python/scrape.py 
    """  
    from htmlentitydefs import name2codepoint  
    if type(text) is unicode:  
        uchr = unichr  
    else:  
        uchr = lambda value: value > 255 and unichr(value) or chr(value)  
  
    def entitydecode(match, uchr=uchr):  
        entity = match.group(1)  
        if entity.startswith('#x'):  
            return uchr(int(entity[2:], 16))  
        elif entity.startswith('#'):  
            return uchr(int(entity[1:]))  
        elif entity in name2codepoint:  
            return uchr(name2codepoint[entity])  
        else:  
            return match.group(0)  
    return charrefpat.sub(entitydecode, text)

def most_frequent(text, lang, max=10):
  text = decode(force_unicode(strip_tags(text)))
  for ch in string.punctuation:
    text = text.replace(ch, '')
  counts = {}
  #disposable = settings.DISPOSABLE_WORDS[languages].split(',')
  #adverbs = settings.DISPOSABLY[lang]
  for w in text.split():
    w = w.strip().lower().encode('utf8')
    #if w[-len(adverbs):]==adverbs and len(w)>-len(adverbs)+2: # is an adverb
    #  break
    if w not in stopwords.words(languages.get_language_name(lang).encode('utf-8')): # is not a common accessory word
      counts[w] = counts.get(w,0) + 1
  items = [(c,w) for (w,c) in counts.items()]
  items.sort()
  items.reverse()
  return [item[1] for item in items[:max]]
  
import re
import unicodedata
from htmlentitydefs import name2codepoint

# From http://www.djangosnippets.org/snippets/369/
def slugify(s, entities=True, decimal=True, hexadecimal=True,
   instance=None, slug_field='slug', filter_dict=None):
    s = smart_unicode(s)

    #character entity reference
    if entities:
        s = re.sub('&(%s);' % '|'.join(name2codepoint), lambda m: unichr(name2codepoint[m.group(1)]), s)

    #decimal character reference
    if decimal:
        try:
            s = re.sub('&#(\d+);', lambda m: unichr(int(m.group(1))), s)
        except:
            pass

    #hexadecimal character reference
    if hexadecimal:
        try:
            s = re.sub('&#x([\da-fA-F]+);', lambda m: unichr(int(m.group(1), 16)), s)
        except:
            pass

    #translate
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')

    #replace unwanted characters
    s = re.sub(r'[^-a-z0-9]+', '-', s.lower())

    #remove redundant -
    s = re.sub('-{2,}', '-', s).strip('-')

    slug = s
    if instance:
        def get_query():
            query = instance.__class__.objects.filter(**{slug_field: slug})
            if filter_dict:
                query = query.filter(**filter_dict)
            if instance.pk:
                query = query.exclude(pk=instance.pk)
            return query
        counter = 1
        while get_query():
            slug = "%s-%s" % (s, counter)
            counter += 1
    return slug

def generate_username(first_name=None, last_name=None):
  valid_id = False
  from django.contrib.auth.models import User
  return slugify(first_name + last_name, instance=User(), slug_field='username')
    