from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from movie_recommendation_engine.playlists.models import MovieProxy
from movie_recommendation_engine.suggestions.models import Suggestion
from movie_recommendation_engine.suggestions.selectors import get_recently_suggested
from movie_recommendation_engine.users.selectors import get_recent_users 


def generate_suggestions(model, users_ids, start_page, end_page):
    '''
    Generate suggestions in batch(start_page:end_page) for the list of users.
    If the users_ids is not provided, the function fetches recent users.
    The suggestions are generated using the model provided.
    '''
    
    #Suggestion = apps.get_model('suggestions', 'Suggestion')
    ctype = ContentType.objects.get_for_model(MovieProxy, for_concrete_model=False)
    
    
    # Fetching Movies and Users
    
    # If users_ids is not provided, the function fetches recent users
    if users_ids is None:
        users_ids = get_recent_users()
        
    # Retrieves popular movie IDs in the range [start_page:end_page].
    # The "start_page" is the number of alredy existing suggestions for those movies generated in the previous batch.
    # The "end_page" is the "start_page" + the number of suggestions to be generated in this batch
    movie_ids = MovieProxy.objects.all().popular().exclude(score=None).values_list('id', flat=True)[start_page:end_page]
    
    # Fetches movies that have already been suggested to the users to avoid duplicate recommendations.
    recently_suggested = get_recently_suggested(movie_ids, users_ids)
    
    if not movie_ids.exists():
        return 
    
    # The function iterates over the movies and users
    # Skips users who already have suggestions for the movie or if the user/movie data is invalid.
    for movie_id in movie_ids:
        users_done = recently_suggested.get(f"{movie_id}") or []
        for u in users_ids:
            if u in users_done:
                # print(movie_id, 'is done for', u, 'user')
                continue
            if u is None:
                continue
            if movie_id is None:
                continue
            # The model predicts the estimated rating (pred) for a user (uid) and a movie (iid).
            # est is the predicted rating value.
            pred = model.predict(uid=u, iid=movie_id).est
            data = {
                'user_id': u,
                'object_id': movie_id,
                'value': pred,
                'content_type': ctype
            }
            
            # Get the suggestion if alredy exists otherwise create a new one
            try:
                obj, _ = Suggestion.objects.get_or_create(user_id=u, object_id=movie_id, content_type=ctype)
            except Suggestion.MultipleObjectsReturned:
                # If duplicate Suggestion objects are found, they are deleted excluding the last one
                qs = Suggestion.objects.filter(user_id=u, object_id=movie_id, content_type=ctype)
                obj = qs.first()
                to_delete = qs.exclude(id=obj.id)
                to_delete.delete()
            # Updates the predicted rating if it has changed or if the suggestion is new
            if obj.value != pred:
                obj.value = pred
                obj.save()