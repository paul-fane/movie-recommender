"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('profiles.api.urls')),  # Include accounts app URLs
    path('api/dashboard/', include('dashboard.api.urls')),
    path('api/playlists/', include('playlists.api.urls')),
    path('api/suggestions/', include('suggestions.api.urls')),
    path('api/watchlists/', include('watchlists.api.urls')),
    path('api/ratings/', include('ratings.api.urls')),
]



if settings.DEBUG:
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)