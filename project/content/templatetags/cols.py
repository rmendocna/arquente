from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import strip_tags

register = template.Library()

@register.filter
@stringfilter
def colz(text):
    "aim for 45 words per colum"
    worded_text = text.replace('.', '. ')
    worded_text = worded_text.replace('  ', ' ')
    words = len(worded_text.split(' '))
    cols = words / 45
    if cols < 1:
        cols = 1
    return cols


