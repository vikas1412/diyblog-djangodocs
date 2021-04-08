from django.urls import path, include
from blog import views


urlpatterns = [
    path('', views.index, name="index"),
    path('blogs/', views.BlogListView.as_view(), name="blogs"),
    path('blog/<int:pk>/', views.BlogDetailView.as_view(), name="blog"),
]
