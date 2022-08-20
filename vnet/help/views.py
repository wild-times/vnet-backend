from django.views.generic import ListView, DetailView

from .models import HelpArticle


class HelpIndexPage(ListView):
    model = HelpArticle
    template_name = 'help/index.html'
    context_object_name = 'articles'

    def get_queryset(self):
        q_set = self.model.objects.all()

        if self.request.GET.get('q'):
            q_set = q_set.filter(title__icontains=self.request.GET.get('q'))

        if self.request.GET.get('t'):
            q_set = q_set.filter(tags__icontains=self.request.GET.get('t'))

        return q_set

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        articles_tags = [article.get_all_tags() for article in context.get('articles')]
        context.update({
            'major_tags': set([tag for tag_list in articles_tags for tag in tag_list]),
            'q': self.request.GET.get('q'),
            't': self.request.GET.get('t')
        })
        return context


class HelpDetailPage(DetailView):
    model = HelpArticle
    template_name = 'help/article.html'
    pk_url_kwarg = 'article_pk'
    context_object_name = 'article'
