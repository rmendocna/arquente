# Copyright (c) 2008 Joost Cassee
# Licensed under the terms of the MIT License (see LICENSE.txt)

"""
This TinyMCE widget was copied and extended from this code by John D'Agostino:
http://code.djangoproject.com/wiki/CustomWidgetsTinyMCE
"""

from django import forms
from django.conf import settings
from django.contrib.admin import widgets as admin_widgets, site
from django.utils.translation import ugettext as _
#from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
import models

LOADING = _('loading...')

def multiClick(name,to_from):
  # consider reverse() here ## or NOT
  return u"""addEvent(%(to_from)s,"click",function(e){var option;
for (var i = 0; (option = %(to_from)s.options[i]); i++) { if (option.selected){lastOpt=option;}}
%(name)s_preview.src="";%(name)s_preview.alt="%(loading)s";
%(name)s_preview.src="/photologue/photo/preview/"+lastOpt.value+"/";});
""" % {"name":name,"to_from":to_from,'loading':LOADING}
  
class ManyToManyImages(admin_widgets.FilteredSelectMultiple):
    """
    Appends image preview scripting to each ManyToManyField which relates to Photo model
    """
    #def __init__(self, verbose_name, is_stacked, attrs=None,choices=()):
    #    self.verbose_name = verbose_name
    #    self.is_stacked = is_stacked
    #    super(ManyToManyImages, self).__init__(verbose_name,is_stacked,attrs,choices)
    
    #def render(self, name, value, attrs=None, choices=()):
    #    output = [super(ManyToManyImages, self).render(name, value, attrs, choices)]
    class Media:
        js = ("/sitemedia/js/photologue.js",)

    def render(self, name, value, *args, **kwargs):
        value = value or u''
        output = [super(ManyToManyImages, self).render(name, value, *args, **kwargs)]
        #name = kwargs.get('name', None)
        #assert name, False
        try:
          thumbnail_admin = models.PhotoSize.objects.get(name='admin_thumbnail')
          size = thumbnail_admin.size
        except:
          size = [100,66]
        output.append(u"""<script type="text/javascript">addEvent(window, "load", function(e){
var from_box= document.getElementById("id_%(name)s_from");
var to_box=document.getElementById("id_%(name)s_to"); 
var %(name)s_preview=document.getElementById("%(name)s_preview");
%(from_box)s
%(to_box)s
loadImg(from_box);
loadImg(to_box);
});</script>
<img id="%(name)s_preview" src="" alt="%(alt)s" width="%(width)s" height="%(height)s" style="border: 1px #55f solid;" align="right" />
""" % {
  'name':name,
  'from_box':multiClick(name,'from_box'), 
  'to_box':multiClick(name,'to_box'),
  'alt':_('preview image'),
  'width':size[0],
  'height':size[1]
})
        #raise output
        return mark_safe(u''.join(output))

class ForeignPhotoWidget(admin_widgets.ForeignKeyRawIdWidget):#(forms.TextInput):
    """
    A Widget for displaying ForeignKeys related to Photo objects in the "raw_id" interface rather than
    in a <select> box.
    """
    def __init__(self, rel, attrs=None):#, using=None):
        self.rel = rel
        #self.admin_site = admin_site
        #self.db = using
        super(ForeignPhotoWidget, self).__init__(rel, site, attrs=attrs)
        
    def render(self, name, value, attrs=None):
        #output = [super(ForeignPhoto, self).render(name, value, attrs)]
        try:
            thumbnail_admin = PhotoSize.objects.get(name='admin_thumbnail')
            size = thumbnail_admin.size
        except:
            size = [100,66]
        output=[u"""<script type="text/javascript">addEvent(window, "load", function (e) {
var box = document.getElementById("id_%(name)s");var %(name)s_preview = document.getElementById("%(name)s_preview");
addEvent(%(name)s_preview,"click",function (e) {
  %(name)s_preview.src="";%(name)s_preview.alt="%(loading)s";
  %(name)s_preview.src="/photologue/photo/preview/"+box.value+"/";});
});  
</script><img id="%(name)s_preview" src="" alt="%(alt)s" width="%(width)s" height="%(height)s" style="border:1px #55f solid" align="right" />
""" % {'name':name,'alt':_('preview image - click to update'),'width':size[0],'height':size[1],'loading':LOADING}]
        output.append(super(ForeignPhotoWidget, self).render(name, value,attrs))
        return mark_safe(u''.join(output))
        
class AdminForeignPhotoWidget(ForeignPhotoWidget,forms.Select):#admin_widgets.ForeignKeyRawIdWidget, ForeignPhotoWidget):
  pass
  
class AdminManyToManyPhotosWidget(ManyToManyImages,forms.SelectMultiple):#admin_widgets.FilteredSelectMultiple, ManyToManyImages):
  pass
