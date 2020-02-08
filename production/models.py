from django.db import models
from django.utils.translation import ugettext_lazy as _

from ckeditor.fields import RichTextField
from mapbox_location_field.models import LocationField
from photologue.models import Gallery, Photo


class Pessoa(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    biosketch = RichTextField(blank=True)
    foto = models.ForeignKey(Photo, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Pessoas'

    def __str__(self):
        return self.nome


class Local(models.Model):
    name = models.CharField(max_length=100)
    local = LocationField()
    foto = models.ForeignKey(Photo, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Lugares'

    def __str__(self):
        return self.nome


#
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

GENERO_OPCOES = (
    ('performance', 'Performance',),
    ('theatre', 'Teatro'),
    ('dance', 'Dança'),
    ('dance-theatre', 'Dança-teatro'),
    ('theatre-dance', 'Teatro-dança')
)

PAPEL_OPCOES = (
    ('operacao', 'Operacao'),
    ('cenografia', 'Cenografia'),
    ('coreografia', 'Coreografia'),
    ('criacao', 'Criação'),
    ('desenho-luz', 'Desenho de Luz'),
    ('desenho-som', 'Desenho de Som'),
    ('direcao', 'Direção'),
    ('direcao-producao', 'Direção de Produção'),
    ('interpretacao', 'Interpretação'),
    ('assistente-direcao', 'Assistente de Direcão'),
)


class Producao(models.Model):
    em_cena = models.BooleanField(blank=True)
    titulo = models.CharField(max_length=255)
    subtitulo = models.CharField(max_length=255, blank=True,
                                 help_text='Baseado no conto de | Sobre piolhos e actores | A verdadeira historia d...')
    slug = models.SlugField(max_length=255, blank=True)
    poster = models.ForeignKey(Photo, null=True, blank=True)
    galeria = models.ForeignKey(Gallery, verbose_name=_('Images'), null=True, blank=True)
    video = models.URLField(help_text="youtube, vimeo, etc", blank=False)
    # sponsors = generic.GenericRelation(Sponsoring)
    duracao = models.TimeField("Duração", null=True, blank=True)
    autores = models.CharField(max_length=255, blank=True)
    genero = models.CharField(null=True, blank=True, choices=GENERO_OPCOES)
    sinopse = RichTextField(_("Synopsis"), blank=True)

    class Meta:
        verbose_name = "Produção"
        verbose_name_plural = "Producões"
        # order_with_respect_to = 'presentations'

    def __str__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        pass


class Participacao(models.Model):
    person = models.ForeignKey(Pessoa)
    production = models.ForeignKey(Producao)
    papel = models.CharField(choices=PAPEL_OPCOES)
    peso = models.PositiveSmallIntegerField(_("Weight"), blank=True)

    class Meta:
        ordering = ('weight', 'name')
        verbose_name = 'Participação'
        verbose_name_plural = 'Participações'

    def __str__(self):
        return "%s, %s, %s" % (self.pessoa, self.get_papel_display(), self.producao)

    def save(self, *args, **kwargs):
        if self.weight in ['', None]:
            weight_list = Participacao.objects.values_list('weight', flat=True).order_by('-weight')
            try:
                weight = weight_list[0] + 1
            except:
                weight = 1
            self.weight = weight
        super(Participacao, self).save(*args, **kwargs)


class Apresentacao(models.Model):
    producao = models.ForeignKey(Producao, related_name="apresentacoes")
    data_hora = models.DateTimeField()
    local = models.ForeignKey(Local)
    galeria = models.ForeignKey(null=True, blank=True)
    # sponsors = generic.GenericRelation(Sponsoring)
    obs = RichTextField(blank=True)
    video = models.URLField(help_text="youtube, vimeo, etc")

    class Meta:
        verbose_name_plural = "Apresentações"
        order_with_respect_to = 'producao'
        ordering = ('-data_time',)

    def __str__(self):
        return '%s | %s | %s' % (self.producao, self.data_hora, self.local)


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


class Evento(models.Model):
    data_hora = models.DateTimeField(blank=True)
    titulo = models.CharField(_("Title"), max_length=200, blank=True)
    # producer = models.ForeignKey(Entity, null=True)
    sinopse = RichTextField(blank=True)
    # sponsors = generic.GenericRelation(Sponsoring)
    website = models.URLField(blank=True)
    ascendente = models.ForeignKey('self', null=True, blank=True)

    # presentations = models.ManyToManyField(Presentation, null=True,  blank=True, through='EventPresentation')

    class Meta:
        ordering = ('data_hora', 'titulo')

    def get_title(self):
        if not self.title and self.ascendente:
            return self.ascendente.title
        else:
            return self.title

    def __str__(self):
        return self.get_title()


# class EventPresentation(models.Model):
#    event = models.ForeignKey(Event)
#    presentation = models.ForeignKey(Presentation)
