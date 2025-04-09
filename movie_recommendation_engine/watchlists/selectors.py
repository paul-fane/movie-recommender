from movie_recommendation_engine.watchlists.models import Watchlist
from movie_recommendation_engine.playlists.models import Playlist
from movie_recommendation_engine.ratings.models import Rating
from django.db.models import Subquery, OuterRef, Exists
from django.db.models import Value, BooleanField
from django.db.models.query import QuerySet
from movie_recommendation_engine.playlists.selectors import playlist_list_by_id_order

def watchlist_list(user) -> QuerySet[Playlist]:
    # Select all playlists ids in the watchlist for the user
    watchlist_ids = Watchlist.objects.filter(user=user).values_list('object_id', flat=True) 
    
    # Select the playlists by the order of the watchlist ids
    if watchlist_ids.exists():
        playlist_qs = playlist_list_by_id_order(watchlist_ids)
        
        # Annotate with the user rate and in_watchlist status
        playlist_qs = playlist_qs.annotate(
            user_rate=Subquery(Rating.objects.filter(user=user, object_id=OuterRef('pk'), active=True).values('value')),
            in_watchlist=Value(True, output_field=BooleanField())
            )
        
        return playlist_qs
    
    return Playlist.objects.none()