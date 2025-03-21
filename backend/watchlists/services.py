from django.contrib.contenttypes.models import ContentType
from playlists.models import MovieProxy, TVShowProxy, Playlist
from .models import Watchlist
def watchlist_create(data, user, request):
    object_id = data['object_id']
    ctype = data['ctype']
    
    content_type = None
    
    if ctype == Playlist.PlaylistTypeChoices.MOVIE:
        content_type = ContentType.objects.get_for_model(MovieProxy, for_concrete_model=False)
    elif ctype == Playlist.PlaylistTypeChoices.SHOW:
        content_type = ContentType.objects.get_for_model(TVShowProxy, for_concrete_model=False)
    elif ctype == Playlist.PlaylistTypeChoices.PLAYLIST:
        content_type = ContentType.objects.get(app_label='playlists', model='Playlists')
    
    
    watchlist_obj = Watchlist.objects.create(user=user, content_type=content_type, object_id=object_id)
    
    return watchlist_obj
        