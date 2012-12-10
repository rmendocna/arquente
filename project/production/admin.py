from datetime import datetime

from django.contrib import admin
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from reversion.admin import VersionAdmin

from models import Entity,  Production,  Event,  Presentation,  Person,  Venue,  Sponsoring, SupportType,  Kind,  Part,  Role
#from forms import PresentationInlineAdminForm

class BaseAdmin(admin.ModelAdmin):
    readonly_fields = ('modifier','modified')
    
    def save_model(self, request, obj, form, change):
        obj.modifier = request.user
        obj.modified = datetime.now()
        obj.save()

class VersionBaseAdmin(VersionAdmin):
    readonly_fields = ('modifier','modified')
    
    def save_model(self, request, obj, form, change):
        obj.modifier = request.user
        obj.modified = datetime.now()
        obj.save()

class BaseTabular(admin.TabularInline):
    readonly_fields = ('modifier','modified')
    
    def save_model(self, request, obj, form, change):
        obj.modifier = request.user
        obj.modified = datetime.now()
        obj.save()
                             
        
class SponsoringInlineAdmin(generic.GenericTabularInline):
    model = Sponsoring
    fields = ('support_type', 'sponsor', 'weight')
    
class PersonAdmin(VersionBaseAdmin):
    fieldsets = (
                 ('',{'fields':(('name', 'is_gender_female'),),  }), 
                 (_('Extra'), {'fields':(('email','telephone'), ('biosketch', 'photo')), 'classes':('collapse', )}), 
                 )

class KindAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_performative')

class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_artistic')
    fieldsets = (
        ('', {'fields':(('name','weight'),'is_artistic')},),
    )
    
class PartInlineAdmin(admin.TabularInline):
    model = Part
    fk_name = 'production'
    
class VenueAdmin(VersionBaseAdmin):
    list_display = ('name', 'address')

class EntityAdmin(VersionBaseAdmin):
    list_display = ('name', 'company','venue')
    fieldsets=(
          ('', {'fields':(('name','is_producer'),('company','logo'),'website'),}),
          (_('Extra'),{'classes':('collapse',),'fields':('bio','venue',('modifier','modified'))}),
    )
    inlines = (SponsoringInlineAdmin, )

class PresentationInlineAdmin(BaseTabular):
    model = Presentation    
    #form = PresentationInlineAdminForm
    fields = ('date_time','venue','modifier','modified')
    fk_name = 'production'
        
class EventPresentationInlineAdmin(BaseTabular):
    model = Presentation
    fields = ('production','date_time','venue','modifier','modified')
    fk_name = 'event'
        
                                                    
class ProductionAdmin(VersionBaseAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'company', 'is_staging', 'is_public')
    fieldsets = (
          ('', ({'fields':(('title', 'is_staging','is_public'), ('subtitle','kind'), ('company', 'authors'), ('opening_night', 'duration'),  'synopsis'), })),
          (_('Images'), ({'fields':('poster', 'images', 'slug'), 'classes':('collapse', )})), 
          )
    inlines = (PartInlineAdmin,  SponsoringInlineAdmin, PresentationInlineAdmin)
    
    def save_formset(self, request, form, formset, change):
        if formset.model != Presentation:
            return super(ProductionAdmin, self).save_formset(request, form, formset, change)
        instances = formset.save(commit=False)
        for instance in instances:
            if not instance.pk:
                instance.modifier = request.user
                instance.modified = datetime.now()
                instance.save()
        formset.save_m2m()

class PresentationAdmin(BaseAdmin):
    list_display=('date_time', 'production_title', 'venue')
    #prepopulated_fields = {'slug': ('title','date_time')}
    fieldsets=(
        ('', {'fields':('production', ('date_time', 'venue'), 'obs'), }, ), 
        (_('Images'), {'fields':('images', 'slug'), 'classes':('collapse', ), }, ), 
    )
    date_hierarchy = 'date_time'

class EventAdmin(BaseAdmin):#admin.ModelAdmin):#VersionBaseAdmin):
    
    inlines = [
            EventPresentationInlineAdmin, 
            SponsoringInlineAdmin,]
            
admin.site.register(Production, ProductionAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(Presentation, PresentationAdmin)
admin.site.register(Entity, EntityAdmin)
admin.site.register(Sponsoring)
admin.site.register(SupportType)
admin.site.register(Kind, KindAdmin)
admin.site.register(Role, RoleAdmin)
