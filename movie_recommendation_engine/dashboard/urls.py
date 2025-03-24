from django.urls import path

from movie_recommendation_engine.dashboard.apis import PlaylistListView

urlpatterns = [
    #path("suggestions/<str:ctype>/", views.MovieSuggestionsView.as_view(), name="movie-suggestions"),
    path("list/", PlaylistListView.as_view(), name="playlists-list"),
]