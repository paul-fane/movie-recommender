from django.urls import path

from . import views

urlpatterns = [
    #path("suggestions/<str:ctype>/", views.MovieSuggestionsView.as_view(), name="movie-suggestions"),
    path("list/", views.SuggestionsListView.as_view(), name="suggestions-list"),
]