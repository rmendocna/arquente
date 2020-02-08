from django.contrib import admin

from reversion.admin import VersionAdmin

from .models import Apresentacao, Evento, Local, Participacao, Pessoa, Producao


# class SponsoringInlineAdmin(generic.GenericTabularInline):
#     model = Sponsoring
#     fields = ('support_type', 'sponsor', 'weight')
#

@admin.register(Pessoa)
class PessoaAdmin(VersionAdmin):
    pass


@admin.register(Participacao)
class ParticipacaoAdmin(VersionAdmin):
    # list_display = ('name', 'is_artistic')
    # fieldsets = (
    #     ('', {'fields': (('name', 'weight'), 'is_artistic')},),
    # )
    pass


@admin.register(Local)
class LocalAdmin(VersionAdmin):
    # list_display = ('name', 'address')
    pass


class ApresentacaoInlineAdmin(admin.TabularInline):
    model = Apresentacao
    # form = PresentationInlineAdminForm
    # fields = ('date_time', 'venue', 'modifier', 'modified')
    # fk_name = 'production'


# class EventPresentationInlineAdmin(BaseTabular):
#     model = Presentation
#     fields = ('production', 'date_time', 'venue', 'modifier', 'modified')
#     fk_name = 'event'


@admin.register(Producao)
class ProducaoAdmin(VersionAdmin):
    prepopulated_fields = {'slug': ('titulo',)}
    # list_display = ('title', 'company', 'is_staging', 'is_public')
    # fieldsets = (
    #     ('', ({'fields': (('title', 'is_staging', 'is_public'), ('subtitle', 'kind'), ('company', 'authors'),
    #                       ('opening_night', 'duration'), 'synopsis'), })),
    #     (_('Images'), ({'fields': ('poster', 'images', 'slug'), 'classes': ('collapse',)})),
    # )
    inlines = (ApresentacaoInlineAdmin)


@admin.register(Apresentacao)
class ApresentacaoAdmin(VersionAdmin):
    date_hierarchy = 'date_hora'


@admin.register(Evento)
class EventoAdmin(VersionAdmin):  # admin.ModelAdmin):#VersionBaseAdmin):
    pass
