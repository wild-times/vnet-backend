from django.views.generic import TemplateView


class CoreIndex(TemplateView):
    template_name = 'core/index.html'
