from django.urls import path

from movie_recommendation_engine.ratings.apis import RateCreateView, RateListBaseView, RateListBaseView, CompareRateListView

urlpatterns = [
    path("create/", RateCreateView.as_view(), name="create"),
    path("list/<int:playlist_id>/", RateListBaseView.as_view(), name="list"), # Returns ratings for a specific playlist
    path("user-list/<str:user_username>/", RateListBaseView.as_view(), name="user-list"), # Returns ratings for a specific user
    path("compar-list/<str:user_username>/", CompareRateListView.as_view(), name="compar-list"),
]