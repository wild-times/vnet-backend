from django.db import models


class Help(models.Model):
    title = models.CharField(max_length=1000)
    content = models.TextField()
    tags = models.CharField(max_length=100, help_text='Comma separated values')
    objects = models.Manager()

    def __str__(self):
        return f'<Help entry titled {self.title}>'
