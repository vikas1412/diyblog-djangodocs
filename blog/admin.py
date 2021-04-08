from django.contrib import admin

from blog.models import Blog, Author


@admin.register(Blog)
class BlogInstanceAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')


@admin.register(Author)
class AuthorInstanceAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')