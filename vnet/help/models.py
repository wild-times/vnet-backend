from django.db import models
from django.urls import reverse


class HelpArticle(models.Model):
    title = models.CharField(max_length=1000)
    content = models.TextField()
    tags = models.CharField(max_length=100, help_text='Comma separated values')
    objects = models.Manager()

    def __repr__(self):
        return f'<HelpArticle: {self.title}>'

    def __str__(self):
        return f'HelpArticle: {self.title}'

    def get_absolute_url(self):
        return reverse('help:article', kwargs={'article_pk': self.pk})

    def get_all_tags(self):
        return list(map(lambda tag: tag.strip(), self.tags.split(','))) if self.tags else []
