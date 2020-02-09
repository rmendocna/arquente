from django.contrib import admin

from mptt.admin import MPTTModelAdmin
from reversion.admin import VersionAdmin

from .forms import PlaceForm, PresentationInlineForm
from .models import Presentation, Event, Place, Participation, Person, Production


# class SponsoringInlineAdmin(generic.GenericTabularInline):
#     model = Sponsoring
#     fields = ('support_type', 'sponsor', 'weight')
#

@admin.register(Person)
class PersonAdmin(VersionAdmin):
    pass


@admin.register(Participation)
class ParticipationAdmin(VersionAdmin):
    # list_display = ('name', 'is_artistic')
    # fieldsets = (
    #     ('', {'fields': (('name', 'weight'), 'is_artistic')},),
    # )
    pass


class ParticipationInline(admin.TabularInline):
    model = Participation


@admin.register(Place)
class PlaceAdmin(VersionAdmin):
    # list_display = ('name', 'address')
    form = PlaceForm


class PresentationInline(admin.TabularInline):
    model = Presentation
    form = PresentationInlineForm
    # form = PresentationInlineAdminForm
    # fields = ('date_time', 'venue', 'modifier', 'modified')
    # fk_name = 'production'


# class EventPresentationInlineAdmin(BaseTabular):
#     model = Presentation
#     fields = ('production', 'date_time', 'venue', 'modifier', 'modified')
#     fk_name = 'event'


@admin.register(Production)
class ProductionAdmin(VersionAdmin):
    prepopulated_fields = {'slug': ('title',)}
    # list_display = ('title', 'company', 'is_staging', 'is_public')
    # fieldsets = (
    #     ('', ({'fields': (('title', 'is_staging', 'is_public'), ('subtitle', 'kind'), ('company', 'authors'),
    #                       ('opening_night', 'duration'), 'synopsis'), })),
    #     (_('Images'), ({'fields': ('poster', 'images', 'slug'), 'classes': ('collapse',)})),
    # )
    inlines = [ParticipationInline, PresentationInline]


@admin.register(Presentation)
class PresentationAdmin(VersionAdmin):
    date_hierarchy = 'date_time'


@admin.register(Event)
class EventAdmin(VersionAdmin, MPTTModelAdmin):
    pass
