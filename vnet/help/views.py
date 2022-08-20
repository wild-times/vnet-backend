from django.views.generic import ListView, DetailView

from .models import HelpArticle


class HelpIndexPage(ListView):
    model = HelpArticle
    template_name = 'help/index.html'
    context_object_name = 'articles'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        articles_tags = [article.get_all_tags() for article in context.get('articles')]
        context['major_tags'] = set([tag for tag_list in articles_tags for tag in tag_list])
        return context


class HelpDetailPage(DetailView):
    model = HelpArticle
    template_name = 'help/article.html'
    pk_url_kwarg = 'article_pk'
    context_object_name = 'article'
