from django.conf import settings
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

from project.content.views import index

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^almasrah/', include('almasrah.foo.urls')),
    (r'^tinymce/', include('tinymce.urls')),
    (r'^photologue/', include('project.photologue.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Django-filebrowser
    (r'^admin/filebrowser/', include('filebrowser.urls')),
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^article/', include('project.content.urls')),
    (r'^production/', include('project.production.urls')),
    url(r'^$', index, name="index"),
)
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^sitemedia/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
