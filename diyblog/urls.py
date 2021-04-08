import django.contrib.auth
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blogs/', include('blog.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', RedirectView.as_view(url="blogs/", permanent=True)),

    path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
