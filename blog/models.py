from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Blog(models.Model):
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=10000)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True,)

    def __str__(self):
        return self.title


class Author(models.Model):
    """Model representing name of bloggers"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(max_length=10000, blank=True)
    date_of_birth = models.DateField(null=True, blank=True, default='1998-10-12')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse('author', args=[str(self.id)])


class Comment(models.Model):
    username = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    blog = models.ForeignKey('Blog', on_delete=models.SET_NULL, null=True)
    comment = models.TextField(max_length=2000)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True,)

    def __str__(self):
        return self.comment
