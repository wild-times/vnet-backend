from django.views.generic import ListView, DetailView

from .models import HelpArticle


class HelpIndexPage(ListView):
    model = HelpArticle
    template_name = 'help/index.html'
    context_object_name = 'articles'


class HelpDetailPage(DetailView):
    model = HelpArticle
    template_name = 'help/article.html'
    pk_url_kwarg = 'article_pk'
    context_object_name = 'article'
