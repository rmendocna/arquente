from datetime import datetime

from django.contrib import admin
from django.conf import settings
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from reversion.admin import VersionAdmin

from project.content.models import Article, News, Annex, Section, RemoteImage
from project.content.forms import ArticleAdminForm, NewsAdminForm

class VersionBaseAdmin(VersionAdmin):
    def save_model(self, request, obj, form, change):
        obj.modifier = request.user
        obj.modified = datetime.now()
        obj.save()

class AnnexInline(generic.GenericTabularInline):
    model = Annex
    
class ArticleAdmin(VersionBaseAdmin):
    form = ArticleAdminForm
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('modifier','modified',)
    list_display = ('title', 'is_public', 'is_highlight')
    fieldsets = (
      ('',{'fields':(('date_pub','is_public','is_highlight'),'title',('short_title','keywords'),'body'),}),
      (_('Images'),{'classes':('collapse',),'fields':('illustration', 'images', 'is_gallery'),}),
      (_('Advanced options'),{'classes':('collapse',),'fields':(
              ('weight','menu','parent','is_index'),
              ('extra_style','extra_script'),
              ('modifier','modified','slug'),
              ),}
      ),
    )
    inlines = [AnnexInline,]
    change_list_template = settings.TEMPLATE_DIRS[0] + '/admin/content/article/change_list.html'
    raw_id_fields = ('parent',)
    
class NewsAdmin(VersionBaseAdmin):
    form = NewsAdminForm
    prepopulated_fields = {'slug': ('headline',)}
    readonly_fields = ('modifier','modified',)
    list_display = ('headline', 'author', 'date_pub', 'is_public')
    list_filter = ['date_pub',]
    date_hierarchy = 'date_pub'
    fieldsets = (
          (_('Images'),{'classes':('collapse',),'fields': ('images',),}),
          ('',{'fields':(('date_pub','is_public'),('headline','author'),'summary','body'),}),
          (_('Advanced options'),{'classes':('collapse',),'fields':(
                ('modifier','modified'),'slug',
                ),}
          ),
    )
    inlines = [AnnexInline,]
    
class SectionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title',)
    
admin.site.register(News, NewsAdmin)
admin.site.register(Article,ArticleAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(RemoteImage)
