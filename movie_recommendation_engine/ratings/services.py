from django.core.cache import cache
from django.contrib.contenttypes.models import ContentType
from movie_recommendation_engine.ml import tasks as ml_tasks

from movie_recommendation_engine.ratings.models import Rating
from movie_recommendation_engine.playlists.models import MovieProxy, TVShowProxy, Playlist
from movie_recommendation_engine.suggestions.models import Suggestion

def rating_create(data, user) -> Rating:
    '''
    Create a rating for a specific user and content type.
    If the user has rated 5 items, trigger a task to generate new suggestions.
    '''
    object_id = data['object_id']
    rating_value = data['rating_value']
    ctype = data['ctype']
    review_text = data['review_text']
    
    if review_text == "":
        review_text = None
        
    content_type = None
    
    if ctype == Playlist.PlaylistTypeChoices.MOVIE:
        content_type = ContentType.objects.get_for_model(MovieProxy, for_concrete_model=False)
    elif ctype == Playlist.PlaylistTypeChoices.SHOW:
        content_type = ContentType.objects.get_for_model(TVShowProxy, for_concrete_model=False)
    elif ctype == Playlist.PlaylistTypeChoices.PLAYLIST:
        content_type = ContentType.objects.get_for_model(Playlist)
    
    rating_obj = Rating.objects.create(content_type=content_type, object_id=object_id, value=rating_value, user=user, review_text=review_text)
    
    
    # Generate new suggestions each 5 ratings from the same user
    if rating_obj.content_object is not None:
        # Increment rating count in cache
        cache_key = f"user_{user.id}_rating_count"
        items_rated = cache.get(cache_key, 0)
        items_rated += 1
        cache.set(cache_key, items_rated, timeout=86400)  # 1-day expiration
        
        if items_rated % 5 == 0:
            #total_suggestions = Suggestion.objects.filter(user=user, did_rate=False).count() or 0
            total_suggestions = Suggestion.objects.filter(user=user).count() or 0
            print("trigger new suggestions")
            print(total_suggestions)
            users_ids = [user.id] # Importatnt! Should be a list, even if it contains only one user id
            # apply_async() function in Celery is used to schedule the execution of a task asynchronously
            ml_tasks.batch_users_prediction_task.apply_async(kwargs ={
                "users_ids": users_ids,
                "start_page": total_suggestions,
                "max_pages": 20
            }) # kwargs: A dictionary of keyword arguments to pass to the task.
            
            #pass
        
    return rating_obj