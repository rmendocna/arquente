from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from project.countries.models import Country
from project.photologue.models import ForeignPhotoField,  ManyToManyPhotosField
from tinymce.models import HTMLField

#from almasrah.models import Base

GENDER_CHOICES = (
                  (1, _('Female')), (0, _('Male')), 
                  )
# Create your models here.

class Base(models.Model):
    #creator = models.ForeignKey(User,  editable=False, related_name='%(class)s_creator',)
    #created = models.DateTimeField(editable=False)
    modifier = models.ForeignKey(User,  related_name='%(class)s_modifier',)
    modified = models.DateTimeField()
                
    #def save(self, *args,  **kwargs):
    #    self.modified = datetime.now()
    #    if not self.created:
    #        self.created=self.modified
    #        self.creator=self.modifier
    #    super(Base, self).save(*args,  **kwargs)

class Person(Base):
    name = models.CharField(_("Name"),  max_length=100)
    is_gender_female = models.NullBooleanField(_("Gender"), blank=True,  choices=GENDER_CHOICES)
    telephone = models.CharField(_("Telephone"),  max_length=30,  blank=True)
    email = models.EmailField(_("E-mail"),  blank=True)
    biosketch = HTMLField(_("BioSketch"), blank=True)
    photo = ForeignPhotoField(verbose_name=_("Photo"), blank=True, null=True)
    
    class Meta:
        verbose_name=_('Person')
        
    def __unicode__(self):
        return u"%s" % self.name
        
class Venue(Base):
    name = models.CharField(_("Name"),  max_length=100)
    city = models.CharField(_("City"),  max_length=100)
    address = models.CharField(_("Address"),  max_length=255, blank=True)
    zip_code = models.CharField(_("Zip Code"),  max_length=30,  blank=True)
    country = models.ForeignKey(Country, verbose_name=_("Country"),  blank=True)
    telephone = models.CharField(_("Telephone"),  max_length=20,  blank=True)
    email = models.EmailField(_("E-mail"),  blank=True)
    website = models.URLField(max_length=255,  blank=True)
    
    class Meta:
        verbose_name=_("Venue")
        verbose_name_plural=_("Venues")
        ordering=('city','name',)
    
    def __unicode__(self):
        return u"%s" % self.name
#
#Tipo_patrocinio (
# peso, *designacao ('apoios', 'patrocinio', 'em colaboracao com...', 'com apoio tecnico de','')
#)
  
class SupportType(models.Model):
    weight = models.PositiveSmallIntegerField(_("Weight"), blank=True)
    name = models.CharField(_("Name"),  max_length=50,  help_text=_("Sponsored by | In colaboration with | Suppported by | Technical Support..."))
    
    class Meta:
        verbose_name=_("Support Type")
        verbose_name_plural=_("Support Types")
        ordering = ('weight', 'name')
    
    def __unicode__(self):
        return u"%s" % self.name
        
    def save(self, *args, **kwargs):
        self.modified = datetime.now()
        if self.weight in ['',None]:
            weight_list = SupportType.objects.values_list('weight',flat=True).order_by('-weight')
            try:
                weight = weight_list[0]+1
            except:
                weight = 1
            self.weight = weight
        super(SupportType, self).save(*args, **kwargs)
                                     
        
class Sponsoring(models.Model):
    weight = models.PositiveSmallIntegerField(_("Weight"), blank=True)
    sponsor = models.ForeignKey('production.Entity', verbose_name=_("Sponsor"))
    support_type = models.ForeignKey(SupportType,  verbose_name=_("Support type"))
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    
    class Meta:
        verbose_name=_("Sponsorship")
        verbose_name_plural=_("Sponsorships")
        order_with_respect_to = 'support_type'
        ordering=('weight', )
    
    def __unicode__(self):
        return u"%s" % self.sponsor
        
    def save(self, *args, **kwargs):
        self.modified = datetime.now()
        if self.weight in ['',None]:
            weight_list = Sponsoring.objects.filter(content_type=self.content_type, object_id=self.object_id).values_list('weight',flat=True).order_by('-weight')
            try:
                weight = weight_list[0]+1
            except:
                weight = 1
            self.weight = weight
        super(Sponsoring, self).save(*args, **kwargs)

class Entity(Base):
    name = models.CharField(_("Name"),  max_length=100)
    is_producer = models.BooleanField(_("Is Producer"),  default=True,  blank=True,  
                                      help_text=_('Allows for proper filtering when assigning entity to productions'))
    company = models.CharField(_("Company"),  max_length=100,  blank=True)
    venue = models.ForeignKey(Venue,  null=True,  blank=True)
    sponsors = generic.GenericRelation(Sponsoring)
    logo = ForeignPhotoField(verbose_name=_("Logo"), null=True,  blank=True)
    bio = HTMLField(_("Short Bio"), blank=True)
    website = models.URLField(max_length=255,  blank=True)
    
    class Meta:
        verbose_name=_('Entity')
        verbose_name_plural=_('Entities')
    
    def __unicode__(self):
        if self.company.upper() != self.name.upper() and self.company not in ['',None]:
            return "%s (%s)" % (self.company, self.name)
        return u"%s" % self.name

class Kind(models.Model):
    name = models.CharField(_("Name"),  max_length=50,  help_text=_("Theatre | Dance | Performance | Poetry | Course | Workshop..."))
    is_performative = models.BooleanField(_("Is Performative?"), default=True, blank=True)
    
    class Meta:
        verbose_name=_('Kind')
        ordering=('name', )
    
    def __unicode__(self):
        return u"%s" % self.name
    
class Role(models.Model):
    weight = models.PositiveSmallIntegerField(_("Weight"), blank=True)
    name = models.CharField(_("Name"),  max_length=50)
    is_artistic = models.NullBooleanField(_('Is artistic?'), blank=True)
    
    class Meta:
        ordering=('weight', 'name')
        verbose_name=_('Role')
        verbose_name_plural=_('Roles')
        
    def __unicode__(self):
        return u"%s" % self.name
        
    def save(self, *args, **kwargs):
        self.modified = datetime.now()
        if self.weight in ['',None]:
            weight_list = Role.objects.values_list('weight',flat=True).order_by('-weight')
            try:
                weight = weight_list[0]+1
            except:
                weight = 1
            self.weight = weight
        super(Role, self).save(*args, **kwargs)

class Production(Base):
    company = models.ForeignKey(Entity,  verbose_name=_('Company'),  )
    opening_night = models.DateField(_("Opening Night"),  #blank=True,  
                                     help_text=_("Allows proper ordering of Productions lists"))
    is_staging = models.BooleanField(_('Is staging?'),  blank=True)
    is_public = models.BooleanField(_('is public'), blank=True)
    title = models.CharField(_('Title'),  max_length=255)
    subtitle = models.CharField(_('Sub-title'),  max_length=255,  blank=True,  
            help_text=_("Based on the novel by | About bedbugs and actors | The true stoy of ..."))
    poster = ForeignPhotoField(verbose_name=_('Poster'),  null=True,  blank=True)
    images = ManyToManyPhotosField(verbose_name=_('Images'),  null=True,  blank=True,  related_name="%(class)s_related")
    sponsors = generic.GenericRelation(Sponsoring)
    duration = models.TimeField(_("duration"), null=True,  blank=True)
    authors = models.CharField(_("Author(s)"),  max_length=255,  blank=True)
    kind = models.ForeignKey(Kind,  verbose_name=_("Kind"),  null=True,  blank=True)
    synopsis = HTMLField(_("Synopsis"), blank=True)
    video = models.URLField(help_text=_("Enter the address of your youtube, vimeo, etc, presentation"), blank=False)
    slug = models.SlugField(max_length=255, blank=True,  help_text=_('This should be filled in automatically'))
    
    class Meta:
        verbose_name=_("Production")
        verbose_name_plural=_("Productions")
        ordering = ('-opening_night', )
        #order_with_respect_to = 'presentations'

    def __unicode__(self):
        return u"%s" % self.title
    
    @models.permalink
    def get_absolute_url(self):
        pass
    
class Presentation(Base):
    production = models.ForeignKey(Production,  verbose_name=_("Production"),  related_name="presentations")
    date_time = models.DateTimeField(_("Date and time"))
    venue = models.ForeignKey(Venue,  verbose_name=_('Venue'))
    images = ManyToManyPhotosField(verbose_name=_('Images'),  null=True,  blank=True)
    sponsors = generic.GenericRelation(Sponsoring)
    obs = HTMLField(_("Comments"),  blank=True)
    video = models.URLField(help_text=_("Enter the address of your youtube, vimeo, etc, presentation"),)
    slug = models.SlugField(max_length=255, blank=True)
    ## late addition
    event = models.ForeignKey('Event', null=True, blank=True)
    
    class Meta:
        verbose_name=_("Presentation")
        verbose_name_plural=_("Presentations")
        order_with_respect_to = 'production'
        ordering=('-date_time', 'venue' )
    
    def production_title(self):
        return u"%s" % self.production.title
    production_title.short_description=_("Title")
    
    def __unicode__(self):
        return self.production_title()
    
    def save(self, *args, **kwargs):
        if self.id in ['', None]:
            self.slug = slugify("%s %s" % (self.venue.name, self.date_time))
        #if self.event.modifier:
	try:
            self.modifier = self.event.modifier
	except:
	   pass
        if self.modified in ['',None]:
            self.modified = datetime.now()
        super(Presentation, self).save(*args, **kwargs)

class Part(models.Model):
    production=models.ForeignKey(Production,  verbose_name=_("Production"), related_name="cast")
    person=models.ForeignKey(Person,  verbose_name=_("Person"))
    role=models.ForeignKey(Role,  verbose_name=_("Role"))
    character=models.CharField(_("Character"),  max_length=100,  blank=True)
    weight=models.PositiveSmallIntegerField(_("Weight"), null=True,  blank=True)
    
    class Meta:
        verbose_name = _("Part")
        verbose_name_plural = _("Parts")
        unique_together = ('production','person', 'role', 'character')
        order_with_respect_to = 'role'
        ordering = ('weight', 'role__weight', 'person__name')
    
    def __unicode__(self):
        s=u"%s" % self.person
        if self.character not in ['',None]:
            s+=u" %s" % self.character
        return s
    
class Event(Base): 
    year = models.PositiveIntegerField(_("Year"))
    title = models.CharField(_("Title"), max_length=200,  blank=True)
    producer = models.ForeignKey(Entity, null=True)
    synopsis = HTMLField(_("Synopsis"),  blank=True)
    sponsors = generic.GenericRelation(Sponsoring)
    website = models.URLField(blank=True,)
    #presentations = models.ManyToManyField(Presentation, null=True,  blank=True, through='EventPresentation')
    
    class Meta:
        verbose_name=_("Event")
        verbose_name_plural=_("Events")
        ordering = ('-year', 'title')

    def __unicode__(self):
        return u"%s /%s" % (self.title,  self.year)

#class EventPresentation(models.Model):
#    event = models.ForeignKey(Event)
#    presentation = models.ForeignKey(Presentation)
    
