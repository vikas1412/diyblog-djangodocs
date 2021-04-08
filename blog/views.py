from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic import CreateView

from blog.models import Blog, Author, Comment


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

    def get_context_data(self, **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        blog_obj = self.kwargs['pk']
        context['comments'] = Comment.objects.order_by('-timestamp')
        return context


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


@login_required
def comment(request, pk=None):
    if request.method == 'POST':
        user_comment = request.POST['comment']
        user = request.user.username
        blog_instance = Blog.objects.get(id=pk)
        comment_obj = Comment(comment=user_comment, username=request.user, blog=blog_instance)
        comment_obj.save()
    return redirect(f'blog/{pk}/')


class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'bio', 'date_of_birth']
    template_name = 'blog/author_form.html'
    initial = {'date_of_birth': '01/01/1990'}
