from string import digits
from datetime import date, datetime

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User   
from django.db.models import permalink
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

import mptt
#from reversion import revision, register as _reversion_register
from project.photologue.models import ManyToManyPhotosField, ForeignPhotoField
from filebrowser.fields import FileBrowseField
from tagging.fields import TagField
from tinymce.models import HTMLField

#from sonar.models import Base,  WeightField
# Create your models here.

PRESSROOM_DIR = "docs/"

class Annex(models.Model):
    file = FileBrowseField(_("Document"), directory=PRESSROOM_DIR, max_length=200,
        extensions=['.pdf','.doc','.rtf','.txt','.xls','.csv'])
    date_pub = models.DateTimeField(_("Date published"), default=datetime.now)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=210, editable=False, blank=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    #summary = models.TextField()

    class Meta:
        ordering = ['-date_pub',]
        get_latest_by = 'date_pub'
        verbose_name=_('Annex')
        verbose_name_plural=_('Annexes')
        
    def __unicode__(self):
        return self.title

class Section(models.Model):
    title = models.CharField(_('Title'), max_length=80, unique=True)
    slug = models.SlugField(max_length=80, editable=False, blank=True)

    class Meta:
        ordering = ['title',]
        verbose_name = _('Section')
        verbose_name_plural = _('Sections')

    def __unicode__(self):
        return self.title

    #def get_absolute_url(self):
    #    return reverse('pr-section', args=[self.slug])

class ArticleManager(models.Manager):
    def get_published(self):
        return self.filter(is_public=True, date_pub__lte=datetime.now)

class Article(models.Model):
    #placement    
    weight = models.PositiveSmallIntegerField(_("Weight"), blank=True,  
            help_text=_("Light articles will float, heavier articles will sink"))#WeightField()
    date_pub = models.DateField(_('publication date'),blank=True)
    is_public = models.BooleanField(_('publish'), default=True,
            help_text=_('Articles will not appear on the site until their "publish date".'),)
    is_highlight = models.BooleanField(_('highlighted'),default=False)
    menu = models.CharField(_("Menu"), max_length=1, blank=True, choices=settings.MENU_CHOICES)
    is_index = models.BooleanField(_('Show sub-article index'), default=False,
            help_text=_('Articles which descend from this one will be listed at the end of the main body'))
    ## related
    parent = models.ForeignKey('self', verbose_name=_("ascendant"), related_name='children',
                null=True, blank=True)
    annexes = generic.GenericRelation(Annex)
    ##images
    images = ManyToManyPhotosField(verbose_name=_("images"), null=True, blank=True, related_name='article_gallery')
    is_gallery =  models.BooleanField(_('show thumbnails'), default=False,
          help_text=_('Images will show on the webpage as zoomable thumbnails'))
    illustration = ForeignPhotoField(verbose_name=_("illustration"), null=True, blank=True,
          related_name='illustration', help_text=_("Top illustration. Min. width 900px. Defaults to parent article"))
    ##extra
    extra_style = models.CharField(_('extra Style'), max_length=512, blank=True)
    extra_script = models.CharField(_('extra Script'), max_length=512, blank=True)
    ##content
    title = models.CharField(_('title'), max_length=128)
    short_title = models.CharField(_('short title'),max_length=50, blank=True,
                help_text=_("This is the title that will show on the menus. Defaults to max of 3 words"))
    body = HTMLField(_('text'), help_text='Copy+paste procedure: always copy from plain text, I cannot stress this enough, do not copy directly from MS Word')
    ##meta
    modifier = models.ForeignKey(User, related_name='%(class)s_modified', null=True, blank=True)
    modified = models.DateTimeField(blank=True)# to hide editable=False)
    keywords = TagField(_('keywords'),max_length=255)
    slug = models.SlugField(max_length=192, blank=True)
    
    def public_children(self):
        return self.get_children().filter(is_public=True).exclude(title="")

    objects = ArticleManager()
    
    def __unicode__(self):
        return u"%s" % self.title
    
    def longtitle(self):
        return u"%s (%s)" % (self.title, self.short_title)
    longtitle.short_description = _('title (short)')

    class Meta:
        verbose_name=_("Article")
        ordering = ('weight','date_pub', 'title')
        get_latest_by = 'date_pub'

    @models.permalink
    def get_absolute_url(self):
        return ('article_detail',(),{'slug':self.slug})
        
    def save(self, *args, **kwargs):
        self.modified = datetime.now()
        if self.weight in ['',None]:
            weight_list = Article.objects.filter(parent=self.parent).values_list('weight',flat=True).order_by('-weight')
            try:
                weight = weight_list[0]+1
            except:
                weight = 1
            self.weight = weight
        if self.date_pub in ['',None]:
            self.date_pub = datetime.today()
        if self.short_title in ['',None]:
            first_three = self.title.split()[:2]
            self.short_title = " ".join(first_three)
        super(Article, self).save(*args, **kwargs)
try:
    mptt.register(Article, order_insertion_by=['weight',])
except:
    pass
        
#class ArticleAttach(models.Model):
#    article = models.ForeignKey(Article,related_name="%(class)s_related")
#    attach = models.ForeignKey(Document, verbose_name=_('Attach'))
#                  
#    class Meta:
#        verbose_name = _("Article Attachment")
#        verbose_name_plural = _("Article Attachments")
        
class News(models.Model):
    date_pub = models.DateTimeField(_("Publish date"), default=datetime.now)
    headline = models.CharField(_("Headline"), max_length=200)
    summary = HTMLField(help_text=_("A single paragraph summary or preview of the news."), blank=True)
    body = HTMLField(_("Body text"),)
    author = models.CharField(_("Author"), max_length=100, blank=True)
    is_public = models.BooleanField(_("Publish on site"), default=True,
        help_text=_('Articles will not appear on the site until their "publish date".'))
    ## related
    sections = models.ManyToManyField(Section, verbose_name=_('Section'), related_name='articles', null=True, blank=True)
    images = ManyToManyPhotosField(verbose_name=_("Photos"), null=True, blank=True, related_name='news_gallery')
    annexes = generic.GenericRelation(Annex)
    ## meta
    slug = models.SlugField(help_text='A "Slug" is a unique URL-friendly title for an object.', blank=True)
    modifier = models.ForeignKey(User, related_name='%(class)s_modified', null=True, blank=True)
    modified = models.DateTimeField(blank=True)#editable=False)    
    
    @models.permalink
    def get_absolute_url(self):
        return ('news_slug',(),{'slug':self.slug})
    
    def save(self, *args, **kwargs):
        self.modified = datetime.now()
        super(News, self).save(*args, **kwargs)
        
    class Meta:
        ordering = ('-date_pub',)
        verbose_name = _('News')
        verbose_name_plural = _('News')
        
#class NewsAttach(models.Model):
#    piece = models.ForeignKey(News,related_name="%(class)s_related")
#    attach = models.ForeignKey(Document, verbose_name=_('Attach'))
#                          
#    class Meta:   
#        verbose_name = _("News Attachment")
#        verbose_name_plural = _("News Attachments")
from picasa import PicasaField
class RemoteImage(models.Model):
    image = PicasaField()
    