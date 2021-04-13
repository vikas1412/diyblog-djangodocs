from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic import CreateView

from blog.forms import SignUpForm
from blog.models import Blog, Author, Comment


def index(request):
    blogs = Blog.objects.count()
    author = Author.objects.count()
    params = {
        'blogs': blogs,
        'authors': author,
    }
    return render(request, 'blog/index.html', params)


class NewBlogCreateView(LoginRequiredMixin, generic.CreateView):
    model = Blog
    template_name = "blog/create_new_post.html"
    success_url = '/'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        try:
            author_object = Author.objects.get(username=self.request.user)
            form.instance.user = author_object
        except Author.DoesNotExist:
            author_object = None

        if author_object is None:
            user = self.request.user
            author_new_object = Author(first_name=user, last_name='', bio='Not updated', username=self.request.user)
            author_new_object.save()
            form.instance.user = Author.objects.get(username=user)

        form.save()
        return super(NewBlogCreateView, self).form_valid(form)


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
        context['comments'] = Comment.objects.filter(blog=blog_obj).order_by('-timestamp')
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


class AuthorCreate(LoginRequiredMixin, generic.CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'bio', 'date_of_birth']
    template_name = 'blog/author_form.html'
    context_object_name = 'new_author'
    initial = {'date_of_birth': '01/01/1990'}

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not self.request.user.is_staff:
            return render(request, 'blog/unauthorized.html')
        return super(AuthorCreate, self).dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.test_func


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


class CommentDeleteView(UserPassesTestMixin, LoginRequiredMixin, generic.DeleteView):
    success_message = "Deleted Successfully"
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    context_object_name = 'delete_comment'
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.username != self.request.user:
            return render(request, 'blog/unauthorized.html')
        return super(CommentDeleteView, self).dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.test_func


class UpdateCommentUpdateView(UserPassesTestMixin, LoginRequiredMixin, generic.UpdateView):
    model = Comment
    template_name = 'blog/update_comment_form.html'
    context_object_name = 'update_comment'
    fields = ['comment']

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.username != self.request.user:
            return render(request, 'blog/unauthorized.html')
        return super(UpdatePostUpdateView, self).dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.test_func


class UpdatePostUpdateView(UserPassesTestMixin, LoginRequiredMixin, generic.UpdateView):
    model = Blog
    template_name = 'blog/update_post_form.html'
    context_object_name = 'update_blog'
    fields = ['title', 'content']

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            return render(request, 'blog/unauthorized.html')
        return super(UpdatePostUpdateView, self).dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.test_func

def handler404(request, exception):
    return render(request, 'blog/pnf.html', {'exception': exception})


def handler505(request, exception):
    return render(request, 'blog/pnf.html', {'exception': exception})
