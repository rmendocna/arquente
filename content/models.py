from django.conf import settings
from django.db import models
from django.utils.safestring import mark_safe

from ckeditor.fields import RichTextField
from mptt.models import MPTTModel
from photologue.models import Photo

PRESSROOM_DIR = 'docs/'

MENU_CHOICES = (
    ('top', 'Todo'),
    ('bottom', 'Rodapé'),
    ('sidebar', 'Lateral')
)


class Article(MPTTModel):
    weight = models.PositiveSmallIntegerField('Peso', blank=True,
                                              help_text='Os artigos mais leves flutuam, os mais pesados afundam')
    is_highlight = models.BooleanField('Destaque', default=False)
    menu = models.CharField(max_length=10, blank=True, choices=MENU_CHOICES)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='Ascendente', null=True, blank=True)
    title = models.CharField('Título', max_length=128)
    short_title = models.CharField('Título abrev.', max_length=50, blank=True,
                                   help_text='Que aparece em listas. Reverte para as 3 primeiras palavras do título')
    body = RichTextField('Text', help_text=mark_safe('Em caso de Copy+Paste, <b>copiar sempre de texto simples</b> '
                                                     'e não directamente do `Word` ou da Internet'))
    slug = models.SlugField(max_length=192, blank=True)
    image = models.ForeignKey(Photo, on_delete=models.CASCADE, verbose_name='Imagem', null=True, blank=True)

    edited_on = models.DateTimeField(auto_now=True, blank=True)
    edited_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Artigo'
        ordering = ('weight', 'title')

    def save(self, *args, **kwargs):
        if self.weight in ['', None]:
            weight_list = Article.objects.filter(parent=self.parent).values_list('weight',
                                                                                 flat=True).order_by('-weight')
            try:
                weight = weight_list[0] + 1
            except:
                weight = 1
            self.weight = weight
        if self.short_title in ['', None]:
            first_three = self.title.split()[:2]
            self.short_title = ' '.join(first_three)
        super(Article, self).save(*args, **kwargs)
