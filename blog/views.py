from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

from blog.models import Blog, Author


def index(request):
    blogs = Blog.objects.count()
    params = {
        'blogs': blogs,
    }
    return render(request, 'blog/index.html', params)


class BlogListView(generic.ListView):
    model = Blog
    template_name = 'blog/blogs.html'
    context_object_name = 'blogs'


class BlogDetailView(generic.DetailView):
    model = Blog
    template_name = "blog/blog.html"
    context_object_name = 'blog'


class AuthorListView(generic.ListView):
    model = Author
    template_name = 'blog/authors.html'
    context_object_name = 'authors'


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'blog/author.html'
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        context = super(AuthorDetailView, self).get_context_data(**kwargs)
        context['author_blogs'] = Blog.objects.all()
        return context