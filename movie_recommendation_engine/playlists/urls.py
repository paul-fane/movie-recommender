from django.urls import path
from movie_recommendation_engine.playlists.apis import MovieDetailView, PlaylistDetailView, TVShowDetailView, SeasonDetailView


urlpatterns = [
    path("movie-detail/<str:slug>/", MovieDetailView.as_view(), name="movie-detail"),
    path("playlist-detail/<str:slug>/", PlaylistDetailView.as_view(), name="playlist-detail"),
    path("tvshow-detail/<str:slug>/", TVShowDetailView.as_view(), name="tvshow-detail"),
    path("season-detail/<str:slug>/", SeasonDetailView.as_view(), name="season-detail"),
]