from django.contrib import admin

from blog.models import Blog, Author, Comment


@admin.register(Blog)
class BlogInstanceAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')


@admin.register(Comment)
class CommentInstanceAdmin(admin.ModelAdmin):
    list_display = ('comment', 'username', 'timestamp')


@admin.register(Author)
class AuthorInstanceAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')