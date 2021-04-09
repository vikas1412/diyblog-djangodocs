from django.urls import path, include
from blog import views


urlpatterns = [
    path('', views.index, name="index"),
    path('all/', views.BlogListView.as_view(), name="blogs"),
    path('blog/<int:pk>/', views.BlogDetailView.as_view(), name="blog"),

    path('<int:pk>/comment/delete/', views.CommentDeleteView.as_view(), name='delete-comment'),

    path('authors/', views.AuthorListView.as_view(), name="authors"),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name="author"),

    path('create/author/', views.AuthorCreate.as_view(), name="create-author"),

    path('comment/<int:pk>', views.comment, name="comment"),

    path('signup/', views.signup, name="signup"),

    path('<int:pk>/update/', views.UpdatePostUpdateView.as_view(), name="update-post"),
]
