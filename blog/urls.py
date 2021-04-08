from django.urls import path, include
from blog import views


urlpatterns = [
    path('', views.index, name="index"),
    path('all/', views.BlogListView.as_view(), name="blogs"),
    path('blog/<int:pk>/', views.BlogDetailView.as_view(), name="blog"),

    path('authors/', views.AuthorListView.as_view(), name="authors"),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name="author"),

    path('comment/<int:pk>', views.comment, name="comment"),
]
