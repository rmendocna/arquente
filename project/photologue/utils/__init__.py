from django.utils.translation import ugettext_lazy as _

def highlight(modeladmin,request,queryset):
    highlighted = queryset.update(is_highlight=True)
    otherset = queryset.model.objects.all().exclude(id__in=[qs.id for qs in queryset.all()])
    dimmed = otherset.update(is_highlight=False)
    #self.message_user(request,_("%s highlighted, % dimmed" % (highlighted, dimmed)))
highlight.short_description = _("Highlight selected")
                