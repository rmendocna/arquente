from datetime import datetime
from django.conf.urls.defaults import *

from project.production.models import Presentation, Production, Event

urlpatterns = patterns('django.views.generic.list_detail',
    url(r'^festivals/$', 'object_list', {"queryset": Event.objects.all()}, name="production_festivals"),
    url(r'^festivals/(?P<slug>[\w-]+)/$', 'object_detail', {"queryset":Event.objects.all(),}, name="production_festivals_detail"),
    url(r'^next_shows/$', 'object_list', {"queryset": Presentation.objects.filter(date_time__gte=datetime.now())}, name="production_next_shows"),
    url(r'^previous_shows/$', 'object_list', {"queryset": Presentation.objects.filter(date_time__lt=datetime.now()),}, name="prodution_previous_shows"),
    url(r'^staging/$', 'object_list', {"queryset": Production.objects.filter(is_staging=True, is_public=True),}, name="production_staging"),
    url(r'^past/$', 'object_list', {"queryset": Production.objects.filter(is_staging=False, is_public=True),}, name="production_past"),
    url(r'^$', 'object_list',{"queryset": Production.objects.all(),}, name="production_list"),
    url(r'^(?P<slug>[\w-]+)/$', 'object_detail', {"queryset": Production.objects.all(),}, name="production_detail"),
)
