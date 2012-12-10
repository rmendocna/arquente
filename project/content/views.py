# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response
from project.content.models import News, Article

INDEX_NEWS_COUNT = 3

def index(request):
    news = News.objects.filter(is_public=True).exclude(headline__isnull=1).order_by('-date_pub')[:INDEX_NEWS_COUNT]
    highlight = Article.objects.filter(is_highlight=True).get()
    return render_to_response('index.html',locals(),context_instance=RequestContext(request))
