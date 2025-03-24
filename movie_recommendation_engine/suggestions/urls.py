from django.urls import path

from movie_recommendation_engine.suggestions.apis import SuggestionsListView

urlpatterns = [
    #path("suggestions/<str:ctype>/", MovieSuggestionsView.as_view(), name="movie-suggestions"),
    path("list/", SuggestionsListView.as_view(), name="suggestions-list"),
]