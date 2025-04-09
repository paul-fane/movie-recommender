from movie_recommendation_engine.ratings.models import Rating
from movie_recommendation_engine.users.models import BaseUser
#from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.contrib.contenttypes.models import ContentType
from movie_recommendation_engine.playlists.models import MovieProxy
from django.db.models import F

def ratings_list(playlist_id=None, user_username=None, filters=None) -> QuerySet[Rating]:
    '''Retrive ratings for a specific playlist or user.'''
    filters = filters or {}
    
    query = filters['query']
    qs = Rating.objects.filter(active=True)
    
    if playlist_id:
        qs = Rating.objects.filter(object_id=playlist_id, active=True)
    elif user_username:
        user = BaseUser.objects.get(email=user_username)
        qs = Rating.objects.filter(user=user, active=True)
        
    if query != "see_all":
        qs = qs.filter(value=int(query))
        
    return qs

def compar_ratings_list(user, user_username, filters=None) -> QuerySet[Rating]:
    '''Retrives ratings from a specific user and compares them with the current user ratings.'''
    filters = filters or {}
    
    query = filters['query']
    
    profile_user = BaseUser.objects.get(email=user_username)
    
    own_ratings = Rating.objects.filter(user=user, active=True).values_list('object_id', flat=True)
    ratings_compar = Rating.objects.filter(user=profile_user, active=True).exclude(object_id__in=own_ratings).order_by("-value")
    
    if query != "see_all":
        ratings_compar = ratings_compar.filter(value=int(query))
    
    return ratings_compar

    
def ratings_dataset() -> QuerySet[Rating]:
    '''Retrieves ratings and formats them for further processing.'''
    
    ctype = ContentType.objects.get_for_model(MovieProxy, for_concrete_model=False)
    qs = Rating.objects.filter(active=True, content_type=ctype)
    qs = qs.annotate(userId=F('user_id'),movieId=F('object_id'),rating=F('value'))
    return qs.values('userId', 'movieId', 'rating') # -> [{'userId': 1, 'movieId': 10, 'rating': 4.5}, ...]

