from django.urls import path
from django.views.generic.detail import DetailView

from .models import Article


urlpatterns = [
    # path('news/$', 'object_list', {"queryset": News.objects.filter(is_public=True).order_by('-date_pub'),},
    # name="news_list"),
    # path('news/(?P<slug>[\w-]+)/$', 'object_detail', {"queryset":
    # News.objects.filter(is_public=True).order_by('-date_pub'), }, name="news_detail"),
    path('<slug:slug>/', DetailView(queryset=Article.objects.all()), name="article_detail"),
]
