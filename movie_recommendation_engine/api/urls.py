from django.urls import include
from django.urls import path

urlpatterns = [
    path("users/", include(("movie_recommendation_engine.users.urls", "users"))),
    path("auth/", include(("movie_recommendation_engine.authentication.urls", "authentication"))),
]
