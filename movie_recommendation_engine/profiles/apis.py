from rest_framework.response import Response
from rest_framework.views import APIView

from movie_recommendation_engine.ratings.models import Rating
from movie_recommendation_engine.suggestions.selectors import suggestions_list
from movie_recommendation_engine.watchlists.selectors import watchlist_list
from movie_recommendation_engine.ratings.serializers import RateSerializer, RatePlaylistSerializer
from movie_recommendation_engine.playlists.serializers import PlaylistSerializer
from movie_recommendation_engine.users.models import BaseUser


        
        
class ProfilePage(APIView):
        
        
    def get(self, request, user_username, *args, **kwargs):
        
        user = request.user
        profile_user = BaseUser.objects.get(email=user_username)
        
        # Select ratings from the current user
        user_ratings_count = Rating.objects.filter(user=profile_user, active=True).count()
        user_ratings = Rating.objects.filter(user=profile_user, active=True)[:5]
        
        
        # If user.is_authenticated && on OWN profile
        own_recommendations = None
        own_watchlist = None
        
        # If user.is_authenticated && on OTHER profile
        # Compared to You(authenticated)! 
        ratings_compar = None # titles other user rated that you haven't rated
        
        
        if user.is_authenticated:
            # User on his own profile
            if user.email == user_username:
                own_recommendations = suggestions_list(user=user, filters={"category":"all"})[:4]
                own_watchlist = watchlist_list(user=user)[:4]
            # User on other profiles
            else:
                own_ratings = Rating.objects.filter(user=user, active=True).values_list('object_id', flat=True)
                ratings_compar = Rating.objects.filter(user=profile_user, active=True).exclude(object_id__in=own_ratings).order_by("-value")[:5] 
                
                
        return Response({
            "profile_username": profile_user.email,
            "user_ratings": RatePlaylistSerializer(user_ratings, many=True).data,
            "user_ratings_count": user_ratings_count,
            "own_recommendations": PlaylistSerializer(own_recommendations, many=True).data,
            "own_watchlist": PlaylistSerializer(own_watchlist, many=True).data,
            "ratings_compar": RatePlaylistSerializer(ratings_compar, many=True).data,
        })
                