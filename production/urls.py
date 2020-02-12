from datetime import datetime, timedelta

from django.urls import path
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Event, Presentation, Production, two_months_ago


urlpatterns = [
    # path('shows/', ListView.as_view(queryset=Presentation.objects.filter(date_time__gte=datetime.now())),
    #      name="prod_next_shows"),
    # path('shows-prev/', ListView.as_view(queryset=Presentation.objects.filter(date_time__lt=datetime.now())),
    #      name="prod_prev_shows"),
    # path('on/', ListView.as_view(queryset=Production.objects.filter(is_staging=True)),
    #      name="prod_staging"),
    path('ev/', ListView.as_view(queryset=Event.objects.filter(date_time__isnull=False,
                                                               date_time__gt=two_months_ago())
                                 ), name='prod-event-list'),
    path('ev/arq/', ListView.as_view(queryset=Event.objects.filter(date_time__isnull=False,
                                                                   date_time__lt=two_months_ago())
                                     ), {'extra_context': {'is_past': True}}, name='prod-event-prev'),
    path('ev/<slug:slug>/', DetailView.as_view(queryset=Event.objects.all()), name='prod-event-detail'),
    path('repertorio/', ListView.as_view(queryset=Production.objects.filter(is_staging=False)), name="prod_past"),
    path('<slug:slug>/', DetailView.as_view(queryset=Production.objects.all()), name="prod-detail"),
    path('', ListView.as_view(queryset=Production.objects.all()), name="prod-list"),
]
