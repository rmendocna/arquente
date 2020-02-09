from datetime import date, timedelta
from itertools import chain

from django.shortcuts import render

from .models import Event, Production


def index(request):
    from content.models import Article
    productions = Production.objects.filter(is_staging=True)
    events = Event.objects.filter(date_time__gt=date.today()-timedelta(30))
    carousel = list(chain(productions, events))
    context = dict(
        carousel=carousel,
        highlights=Article.objects.filter(is_highlight=True).order_by('-weight')[:5],
        count=len(carousel)
    )
    return render(request, 'index.html', context)
