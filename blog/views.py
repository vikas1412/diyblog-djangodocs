from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

from blog.models import Blog


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
