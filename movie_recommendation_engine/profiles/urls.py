from django.urls import path
from movie_recommendation_engine.profiles.apis import ProfilePage

urlpatterns = [
    path('profile/<str:user_username>/', ProfilePage.as_view(), name='profile'),
]