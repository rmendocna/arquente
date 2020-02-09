from django.contrib import admin

from mptt.admin import MPTTModelAdmin
from reversion.admin import VersionAdmin

from .models import Article


class VersionBaseAdmin(VersionAdmin):

    def save_model(self, request, obj, form, change):
        obj.edited_by = request.user
        obj.save()


@admin.register(Article)
class ArticleAdmin(VersionBaseAdmin, MPTTModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('edited_by',)
    list_display = ('title', 'is_highlight')
