from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserRegistrationView, GetUsername, ProfilePage

urlpatterns = [
    # JWT token URLs
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Registration URL
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    
    path('getUser/', GetUsername.as_view(), name='get-username'),
    path('profile/<str:user_username>/', ProfilePage.as_view(), name='profile'),
]