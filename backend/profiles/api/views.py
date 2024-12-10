from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Subquery

from .serializers import UserRegistrationSerializer
from ratings.models import Rating
from suggestions.selectors import suggestions_list
from watchlists.selectors import watchlist_list
from ratings.api.serializers import RateSerializer, RatePlaylistSerializer
from playlists.api.serializers import PlaylistSerializer
from django.contrib.auth.models import User

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # This calls the `create` method in the serializer
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class GetUsername(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        # print(username)
        # currentUser = User.objects.get(username=username)
        
        return Response({
            "id": user.pk,
            "username": user.username
        })
        
        
class ProfilePage(APIView):
        
        
    def get(self, request, user_username, *args, **kwargs):
        
        user = request.user
        profile_user = User.objects.get(username=user_username)
        
        # Select ratings from the current user
        user_ratings_count = Rating.objects.filter(user=profile_user, active=True).count()
        user_ratings = Rating.objects.filter(user=profile_user, active=True)[:5]
        
        
        # If user.is_authenticated && on OWN profile
        own_recommendations = None
        own_watchlist = None
        own_playlists = "TO DO!"
        
        # If user.is_authenticated && on OTHER profile
        # Compared to You(authenticated)! 
        ratings_compar = None # titles other user rated that you haven't rated
        
        
        if user.is_authenticated:
            # User on his own profile
            if user.username == user_username:
                own_recommendations = suggestions_list(user=user, filters={"category":"all"})[:4]
                own_watchlist = watchlist_list(user=user)[:4]
            # User on other profiles
            else:
                own_ratings = Rating.objects.filter(user=user, active=True).values_list('object_id', flat=True)
                ratings_compar = Rating.objects.filter(user=profile_user, active=True).exclude(object_id__in=own_ratings).order_by("-value")[:5] 
                
                
        return Response({
            "profile_username": profile_user.username,
            "user_ratings": RatePlaylistSerializer(user_ratings, many=True).data,
            "user_ratings_count": user_ratings_count,
            "own_recommendations": PlaylistSerializer(own_recommendations, many=True).data,
            "own_watchlist": PlaylistSerializer(own_watchlist, many=True).data,
            "own_playlists": own_playlists, #TODO
            "ratings_compar": RatePlaylistSerializer(ratings_compar, many=True).data,
        })
                
        
        