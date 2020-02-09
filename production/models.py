from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ckeditor.fields import RichTextField
from mapbox_location_field.models import LocationField
from mptt.models import MPTTModel, TreeForeignKey
from photologue.models import Gallery, Photo


class BaseMixin(object):
    edited_on = models.DateTimeField(auto_now=True, blank=True)
    edited_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)


class BaseModel(BaseMixin, models.Model):

    class Meta:
        abstract = True


class Person(BaseModel):
    first_name = models.CharField('Nome', max_length=30)
    last_name = models.CharField('Sobrenome', max_length=30)
    email = models.EmailField(blank=True)
    biosketch = RichTextField(blank=True)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, verbose_name='Foto', blank=True, null=True)

    class Meta:
        verbose_name = 'Pessoa'

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class Place(BaseModel):
    name = models.CharField('Name', max_length=100)
    place = LocationField('Local')
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, verbose_name='Foto', blank=True, null=True)

    class Meta:
        verbose_name = 'Local'
        verbose_name_plural = 'Locais'

    def __str__(self):
        return self.name


# Tipo_patrocinio (
# peso, *designacao ('apoios', 'patrocinio', 'em colaboracao com...', 'com apoio tecnico de','')
# )

# class SupportType(models.Model):
#     weight = models.PositiveSmallIntegerField(_("Weight"), blank=True)
#     name = models.CharField(_("Name"), max_length=50,
#                             help_text=_("Sponsored by | In colaboration with | Suppported by | Technical Support..."))
#
#     class Meta:
#         verbose_name = _("Support Type")
#         verbose_name_plural = _("Support Types")
#         ordering = ('weight', 'name')
#
#     def __unicode__(self):
#         return u"%s" % self.name
#
#     def save(self, *args, **kwargs):
#         self.modified = datetime.now()
#         if self.weight in ['', None]:
#             weight_list = SupportType.objects.values_list('weight', flat=True).order_by('-weight')
#             try:
#                 weight = weight_list[0] + 1
#             except:
#                 weight = 1
#             self.weight = weight
#         super(SupportType, self).save(*args, **kwargs)
#
#
# class Sponsoring(models.Model):
#     weight = models.PositiveSmallIntegerField(_("Weight"), blank=True)
#     sponsor = models.ForeignKey('production.Entity', verbose_name=_("Sponsor"))
#     support_type = models.ForeignKey(SupportType, verbose_name=_("Support type"))
#     content_type = models.ForeignKey(ContentType)
#     object_id = models.PositiveIntegerField()
#     content_object = generic.GenericForeignKey()
#
#     class Meta:
#         verbose_name = _("Sponsorship")
#         verbose_name_plural = _("Sponsorships")
#         order_with_respect_to = 'support_type'
#         ordering = ('weight',)
#
#     def __unicode__(self):
#         return u"%s" % self.sponsor
#
#     def save(self, *args, **kwargs):
#         self.modified = datetime.now()
#         if self.weight in ['', None]:
#             weight_list = Sponsoring.objects.filter(content_type=self.content_type,
#                                                     object_id=self.object_id).values_list('weight', flat=True
#                                                     ).order_by('-weight')
#             try:
#                 weight = weight_list[0] + 1
#             except:
#                 weight = 1
#             self.weight = weight
#         super(Sponsoring, self).save(*args, **kwargs)
#
#
# class Entity(Base):
#     name = models.CharField(_("Name"), max_length=100)
#     is_producer = models.BooleanField(_("Is Producer"), default=True, blank=True,
#                                       help_text=_('Allows for proper filtering when assigning entity to productions'))
#     company = models.CharField(_("Company"), max_length=100, blank=True)
#     venue = models.ForeignKey(Venue, null=True, blank=True)
#     sponsors = generic.GenericRelation(Sponsoring)
#     logo = ForeignPhotoField(verbose_name=_("Logo"), null=True, blank=True)
#     bio = HTMLField(_("Short Bio"), blank=True)
#     website = models.URLField(max_length=255, blank=True)
#
#     class Meta:
#         verbose_name = _('Entity')
#         verbose_name_plural = _('Entities')
#
#     def __unicode__(self):
#         if self.company.upper() != self.name.upper() and self.company not in ['', None]:
#             return "%s (%s)" % (self.company, self.name)
#         return u"%s" % self.name
#
#
# class Kind(models.Model):
#     name = models.CharField(_("Name"), max_length=50,
#                             help_text=_("Theatre | Dance | Performance | Poetry | Course | Workshop..."))
#     is_performative = models.BooleanField(_("Is Performative?"), default=True, blank=True)
#
#     class Meta:
#         verbose_name = _('Kind')
#         ordering = ('name',)
#
#     def __unicode__(self):
#         return u"%s" % self.name

GENRE_CHOICES = (
    ('performance', 'Performance',),
    ('theatre', 'Teatro'),
    ('dance', 'Dança'),
    ('dance-theatre', 'Dança-teatro'),
    ('theatre-dance', 'Teatro-dança')
)

ROLE_CHOICES = (
    ('operacao', 'Operacao'),
    ('cenografia', 'Cenografia'),
    ('coreografia', 'Coreografia'),
    ('criacao', 'Criação'),
    ('desenho-luz', 'Desenho de Luz'),
    ('desenho-som', 'Desenho de Som'),
    ('direcao', 'Direção'),
    ('direcao-production', 'Direção de Produção'),
    ('interpretacao', 'Interpretação'),
    ('assistente-direcao', 'Assistente de Direcão'),
)


class Production(BaseModel):
    is_staging = models.BooleanField('Em cena', blank=True)
    title = models.CharField('Título', max_length=255)
    subtitle = models.CharField('Sub-título', max_length=255, blank=True,
                                help_text='Baseado no conto de | Sobre piolhos e actores | A verdadeira historia d...')
    slug = models.SlugField(max_length=255, blank=True)
    poster = models.ForeignKey(Photo, on_delete=models.CASCADE, null=True, blank=True)
    gallery = models.ForeignKey(Gallery, verbose_name='Galeria', on_delete=models.CASCADE, null=True, blank=True)
    video = models.URLField('Vídeo', help_text="youtube, vimeo, etc", blank=True)
    # sponsors = generic.GenericRelation(Sponsoring)
    duration = models.TimeField("Duração", null=True, blank=True)
    authors = models.CharField('Autores', max_length=255, blank=True)
    genre = models.CharField('Género', max_length=2, null=True, blank=True, choices=GENRE_CHOICES)
    synopsys = RichTextField("Sinopse", blank=True)
    credits = models.ManyToManyField(Person, verbose_name='Ficha Técnica', through='production.Participation')

    class Meta:
        verbose_name = "Produção"
        verbose_name_plural = "Producões"
        # order_with_respect_to = 'presentations'

    def __str__(self):
        return self.title


class Participation(BaseModel):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    production = models.ForeignKey(Production, on_delete=models.CASCADE)
    role = models.CharField(choices=ROLE_CHOICES, max_length=50)
    weight = models.PositiveSmallIntegerField(_("Weight"), blank=True)

    class Meta:
        ordering = ('production', 'weight', 'person')
        verbose_name = 'Participação'
        verbose_name_plural = 'Participações'

    def __str__(self):
        return "%s, %s, %s" % (self.person, self.get_role_display(), self.production)

    def save(self, *args, **kwargs):
        if self.weight in ['', None]:
            weight_list = Participation.objects.values_list('weight', flat=True).order_by('-weight')
            try:
                weight = weight_list[0] + 1
            except:
                weight = 1
            self.weight = weight
        super(Participation, self).save(*args, **kwargs)


class Presentation(BaseModel):
    production = models.ForeignKey(Production, on_delete=models.CASCADE, related_name="presentations")
    date_time = models.DateTimeField()
    place = models.ForeignKey(Place, on_delete=models.CASCADE, null=True, blank=True)
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, null=True, blank=True)
    # sponsors = generic.GenericRelation(Sponsoring)
    notes = RichTextField(blank=True, config_name='basic_ckeditor')
    video = models.URLField(help_text="youtube, vimeo, etc", blank=True)

    class Meta:
        verbose_name = "Apresentação"
        verbose_name_plural = "Apresentações"
        # order_with_respect_to = 'production'
        ordering = ('-date_time',)

    def __str__(self):
        return '%s | %s | %s' % (self.production, self.date_time, self.place)


# class Part(models.Model):
#     production = models.ForeignKey(Production, verbose_name=_("Production"), related_name="cast")
#     person = models.ForeignKey(Person, verbose_name=_("Person"))
#     role = models.ForeignKey(Role, verbose_name=_("Role"))
#     character = models.CharField(_("Character"), max_length=100, blank=True)
#     weight = models.PositiveSmallIntegerField(_("Weight"), null=True, blank=True)
#
#     class Meta:
#         verbose_name = _("Part")
#         verbose_name_plural = _("Parts")
#         unique_together = ('production', 'person', 'role', 'character')
#         order_with_respect_to = 'role'
#         ordering = ('weight', 'role__weight', 'person__name')
#
#     def __unicode__(self):
#         s = u"%s" % self.person
#         if self.character not in ['', None]:
#             s += u" %s" % self.character
#         return s


class Event(BaseMixin, MPTTModel):
    date_time = models.DateTimeField(blank=True)
    title = models.CharField('Título', max_length=200, blank=True)
    # producer = models.ForeignKey(Entity, null=True)
    synopsys = RichTextField(blank=True)
    # sponsors = generic.GenericRelation(Sponsoring)
    website = models.URLField(blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    # presentations = models.ManyToManyField(Presentation, null=True,  blank=True, through='EventPresentation')

    class Meta:
        ordering = ('date_time', 'title')
        verbose_name = 'Evento'

    def get_title(self):
        if not self.title and self.parent:
            return self.parent.title
        else:
            return self.title

    def __str__(self):
        return self.get_title()


# class EventPresentation(models.Model):
#    event = models.ForeignKey(Event)
#    presentation = models.ForeignKey(Presentation)
