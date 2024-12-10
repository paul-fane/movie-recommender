from .models import Watchlist
from playlists.models import Playlist
from ratings.models import Rating
from django.db.models import Subquery, OuterRef, Exists
from django.db.models import Value, BooleanField

def watchlist_list(user):
    watchlist_ids = Watchlist.objects.filter(user=user).values_list('object_id', flat=True) 
    
    playlist_qs = Playlist.objects.by_id_order(watchlist_ids)
    
    
    playlist_qs = playlist_qs.annotate(
        user_rate=Subquery(Rating.objects.filter(user=user, object_id=OuterRef('pk'), active=True).values('value')),
        in_watchlist=Value(True, output_field=BooleanField())
        )
    
    return playlist_qs