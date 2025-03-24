from django.urls import path
from movie_recommendation_engine.watchlists.apis import WatchlistListView, WatchlistCreateView, WatchlistDeleteView

urlpatterns = [
    path('list/', WatchlistListView.as_view(), name='watchlist-list'),
    path('create/', WatchlistCreateView.as_view(), name='watchlist-create'),
    path('delete/<int:pk>/', WatchlistDeleteView.as_view(), name='watchlist-delete'),
]