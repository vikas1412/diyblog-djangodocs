from django.db import models
from django.utils import timezone


class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=1000)
    date = models.DateField(auto_now_add=True, blank=True,)

    def __str__(self):
        return self.title
