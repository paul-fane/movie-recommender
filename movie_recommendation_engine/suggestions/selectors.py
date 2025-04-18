import datetime
from django.utils import timezone
from django.db.models import Subquery, OuterRef, Exists, F
from django.db.models.query import QuerySet
from django.contrib.contenttypes.models import ContentType
from movie_recommendation_engine.suggestions.models import Suggestion
from movie_recommendation_engine.playlists.models import Playlist, MovieProxy, TVShowProxy #type=Playlist.PlaylistTypeChoices.PLAYLIST
from movie_recommendation_engine.ratings.models import Rating
from movie_recommendation_engine.watchlists.models import Watchlist

def suggestions_list(user, filters=None) -> QuerySet[Suggestion]:
    filters = filters or {}
    
    category = filters['category']
    # query = None
    # if "query" in filters:
    #     query = filters["query"]
    
    
    # Initial category = "all" => select all
    # Select all Movies and TVShows suggestions for the user
    suggestion_qs = Suggestion.objects.filter(user=user, did_rate=False)
    # Select All Movies and TVShows
    # playlist_qs = Playlist.objects.all().movie_or_show()
    playlist_qs = Playlist.objects.none()
    
    
    # If exists suggestions for the user
    if suggestion_qs.exists():
        # If the user select only movies or only tvshows
        if category == "movies":
            content_type = ContentType.objects.get_for_model(MovieProxy, for_concrete_model=False)
            suggestion_qs = Suggestion.objects.filter(user=user, did_rate=False, content_type=content_type)
        elif category == "shows":
            content_type = ContentType.objects.get_for_model(TVShowProxy, for_concrete_model=False)
            suggestion_qs = Suggestion.objects.filter(user=user, did_rate=False, content_type=content_type)
    else:
        return playlist_qs
    
    
    # If does exist a list of suggestions then select the Movies & TVShows in that specific order
    if suggestion_qs.exists():
        ids = suggestion_qs.order_by("-value").values_list('object_id', flat=True) 
        if category == "all":
            playlist_qs = Playlist.objects.by_id_order(ids)
        if category == "movies":
            playlist_qs = MovieProxy.objects.by_id_order(ids)
        elif category == "shows":
            playlist_qs = TVShowProxy.objects.by_id_order(ids)
    else:
        return playlist_qs
    
    playlist_qs = playlist_qs.annotate(
        user_rate=Subquery(Rating.objects.filter(user=user, object_id=OuterRef('pk'), active=True).values('value')),
        in_watchlist=Exists(Watchlist.objects.filter(user=user, object_id=OuterRef('pk')))
        )
    
    return playlist_qs


def get_recently_suggested(movie_ids=[], user_ids=[], days_ago=7):
    '''
    Get the list of movies that have been suggested to the users in the last days_ago.
    The function returns a dictionary with the movie_id as key and the list of users as value who have been suggested that movie
    '''
    data = {}
    delta = datetime.timedelta(days=days_ago)
    time_delta = timezone.now() - delta
    ctype = ContentType.objects.get_for_model(MovieProxy, for_concrete_model=False)
    filter_args = {
        "content_type": ctype,
        "object_id__in": movie_ids,
        "user_id__in": user_ids,
        "active": True,
        "timestamp__gte": time_delta
    }
    dataset = Suggestion.objects.filter(**filter_args)
    dataset = dataset.annotate(movieId=F('object_id'), userId=F('user_id')).values("movieId", "userId")
    for d in dataset:
        # print(d) # [{'movieId': abac, 'userId': ad}]
        movie_id = str(d.get("movieId"))
        user_id = d.get('userId')
        if movie_id in data:
            data[movie_id].append(user_id)
        else:
            data[movie_id] = [user_id]
    return data