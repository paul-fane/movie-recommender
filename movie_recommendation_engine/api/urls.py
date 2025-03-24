from django.urls import include
from django.urls import path

urlpatterns = [
    path("users/", include(("movie_recommendation_engine.users.urls", "users"))),
    path("auth/", include(("movie_recommendation_engine.authentication.urls", "authentication"))),
    path("suggestions/", include(("movie_recommendation_engine.suggestions.urls", "suggestions"))),
    path("ratings/", include(("movie_recommendation_engine.ratings.urls", "ratings"))),
    path("playlists/", include(("movie_recommendation_engine.playlists.urls", "playlists"))),
    path("dashboard/", include(("movie_recommendation_engine.dashboard.urls", "dashboard"))),
    path("watchlists/", include(("movie_recommendation_engine.watchlists.urls", "watchlists"))),
]
