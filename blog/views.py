from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from django.views.generic import CreateView

from blog.forms import SignUpForm
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
    paginate_by = 8


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
    paginate_by = 8


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
    return redirect(reverse('blog', kwargs={"pk": pk}))


class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'bio', 'date_of_birth']
    template_name = 'blog/author_form.html'
    initial = {'date_of_birth': '01/01/1990'}


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password1 = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password1)
            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('index')
            else:
                return HttpResponse("Invalid username & password")

    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


