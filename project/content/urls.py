from django.conf.urls.defaults import *
from project.content.views import index
from project.content.models import Article, News


urlpatterns = patterns('django.views.generic.list_detail',
    # Example:
    url(r'^news/$', 'object_list', {"queryset": News.objects.filter(is_public=True).order_by('-date_pub'),}, name="news_list"),
    url(r'^news/(?P<slug>[\w-]+)/$', 'object_detail', {"queryset": News.objects.filter(is_public=True).order_by('-date_pub'), }, name="news_detail"),
    url(r'^(?P<slug>[\w-]+)/$', 'object_detail', {"queryset": Article.objects.filter(is_public=True), }, name="article_detail"),
)
