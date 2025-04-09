from django.urls import path

from movie_recommendation_engine.users.apis import (
    UserCreateApi, UserDetailApi, UserListApi, UserUpdateApi, UserMeApi
)

urlpatterns = [
    path("", UserListApi.as_view(), name="list"),
    path("create/", UserCreateApi.as_view(), name="create"),
    path("<int:user_id>/", UserDetailApi.as_view(), name="detail"),
    path("<int:user_id>/update/", UserUpdateApi.as_view(), name="update"),
    path("me/", UserMeApi.as_view(), name="me"),
]