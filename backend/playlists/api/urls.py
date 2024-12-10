from django.urls import path
from . import views


urlpatterns = [
    path("movie-detail/<str:slug>/", views.MovieDetailView.as_view(), name="movie-detail"),
    path("playlist-detail/<str:slug>/", views.PlaylistDetailView.as_view(), name="playlist-detail"),
    path("tvshow-detail/<str:slug>/", views.TVShowDetailView.as_view(), name="tvshow-detail"),
    path("season-detail/<str:slug>/", views.SeasonDetailView.as_view(), name="season-detail"),
]