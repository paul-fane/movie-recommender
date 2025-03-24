from movie_recommendation_engine.ratings.models import Rating
from django.contrib.auth.models import User



def ratings_list(playlist_id=None, user_username=None, filters=None):
    filters = filters or {}
    
    query = filters['query']
    qs = Rating.objects.filter(active=True)
    
    if playlist_id:
        qs = Rating.objects.filter(object_id=playlist_id, active=True)
    elif user_username:
        user = User.objects.get(username=user_username)
        qs = Rating.objects.filter(user=user, active=True)
        
    if query != "see_all":
        qs = qs.filter(value=int(query))
        
    return qs

def compar_ratings_list(user, user_username, filters=None):
    filters = filters or {}
    
    query = filters['query']
    
    profile_user = User.objects.get(username=user_username)
    
    own_ratings = Rating.objects.filter(user=user, active=True).values_list('object_id', flat=True)
    ratings_compar = Rating.objects.filter(user=profile_user, active=True).exclude(object_id__in=own_ratings).order_by("-value")
    
    if query != "see_all":
        ratings_compar = ratings_compar.filter(value=int(query))
    
    return ratings_compar