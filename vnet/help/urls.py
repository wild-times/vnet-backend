from django.urls import path

from .views import HelpIndexPage, HelpDetailPage


app_name = 'help'


urlpatterns = [
    # help/
    path('', HelpIndexPage.as_view(), name='index'),

    # help/article/12/
    path('article/<int:article_pk>/', HelpDetailPage.as_view(), name='article'),
]
