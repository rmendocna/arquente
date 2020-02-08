from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from content.views import index

admin.autodiscover()

urlpatterns = [
    path('tinymce/', include('tinymce.urls')),
    path('photologue/', include('photologue.urls', namespace='photologue')),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    # path('admin/filebrowser/', include('filebrowser.urls')),
    path('admin/', include(admin.site.urls)),
    # path('arti/', include('content.urls')),
    path('prod/', include('production.urls')),
    path('', index, name="index"),
]

if settings.DEBUG:
    urlpatterns += + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
