from django.urls import path

from . import views

urlpatterns = [
    path("create/", views.RateCreateView.as_view(), name="create"),
    path("list/<int:playlist_id>/", views.RateListBaseView.as_view(), name="list"),
    path("user-list/<str:user_username>/", views.RateListBaseView.as_view(), name="user-list"),
    path("compar-list/<str:user_username>/", views.CompareRateListView.as_view(), name="compar-list"),
]