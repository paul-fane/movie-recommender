from django.db.models import Subquery, Exists, OuterRef
from movie_recommendation_engine.playlists.models import Playlist, MovieProxy, TVShowProxy #type=Playlist.PlaylistTypeChoices.PLAYLIST

#from watchlists.models import Watchlist
from movie_recommendation_engine.ratings.models import Rating
from movie_recommendation_engine.watchlists.models import Watchlist
from django.db.models.query import QuerySet
from django.db.models import F, Case, When

# def dashboard_movie_list(user, filters=None):
#     '''
#     "popular": "popular",
#     "unpopular": "unpopular",
#     "top rated": "-rating_avg",
#     "low rated": "rating_avg",
#     "recent": "-release_date",
#     "old": "release_date",
#     '''
#     filters = filters or {}
    
#     category = filters['category']
#     sort_by = filters['sort_by']
#     query = None
#     if "query" in filters:
#         query = filters["query"]
        
#     qs= None
    
#     if category == "all":
#         qs = Playlist.objects.all().movies_shows_and_playlists()
#     elif category == "movies":
#         qs = MovieProxy.objects.all()
#     elif category == "shows":
#         qs = TVShowProxy.objects.all()
#     elif category == "playlists":
#         qs = Playlist.objects.featured_playlists()
    
        
#     if sort_by is not None:
#         if sort_by == 'popular':
#             qs = qs.popular()
#         elif sort_by == 'unpopular':
#             qs = qs.popular(reverse=True)
#         else:
#             qs = qs.order_by(sort_by)
        
    
#     if query and query is not None:
#         qs = qs.search(query=query)
        
#     # if user.is_authenticated:
#     #     qs = qs.annotate(
#     #         has_watched=Exists(
#     #             #Watchlist.objects.filter(user=user, playlist=OuterRef('pk'), watched=True)
#     #             Rating.objects.filter(user=user, object_id=OuterRef('pk'))
#     #         ))

#     if user.is_authenticated:
#         qs = qs.annotate(
#             user_rate=Subquery(Rating.objects.filter(user=user, object_id=OuterRef('pk'), active=True).values('value')),
#             in_watchlist=Exists(Watchlist.objects.filter(user=user, object_id=OuterRef('pk')))
#             )
        
        
#     return qs


def dashboard_movie_list(user, filters=None):
    filters = filters or {}
    category = filters.get('category', 'all')
    sort_by = filters.get('sort_by')
    query = filters.get('query')

    # Use a single queryset with conditional filters
    qs = Playlist.objects.all().movies_shows_and_playlists()
    if category == "movies":
        qs = MovieProxy.objects.all()
    elif category == "shows":
        qs = TVShowProxy.objects.all()
    elif category == "playlists":
        qs = Playlist.objects.featured_playlists()

    # Optimize sorting
    if sort_by:
        if sort_by == 'popular':
            qs = qs.popular().exclude(score=None)
        elif sort_by == 'unpopular':
            qs = qs.popular(reverse=True).exclude(score=None)
        elif sort_by == "release_date" or sort_by == "-release_date":
            qs = qs.order_by(sort_by).exclude(release_date=None)
        elif sort_by == "rating_avg" or sort_by == "-rating_avg":
            qs = qs.order_by(sort_by).exclude(rating_avg=None)
        else:
            qs = qs.order_by(sort_by)

    # Optimize search query
    if query:
        qs = qs.search(query=query)

    # Add annotations for authenticated users
    if user.is_authenticated:
        user_ratings_subquery = Rating.objects.filter(
            user=user, object_id=OuterRef('pk'), active=True
        ).values('value')[:1]
        watchlist_exists = Watchlist.objects.filter(user=user, object_id=OuterRef('pk'))

        qs = qs.annotate(
            user_rate=Subquery(user_ratings_subquery),
            in_watchlist=Exists(watchlist_exists)
        )
        
    # if user.is_authenticated:
    #     qs = qs.annotate(
    #         user_rate=Subquery(Rating.objects.filter(user=user, object_id=OuterRef('pk'), active=True).values('value')),
    #         in_watchlist=Exists(Watchlist.objects.filter(user=user, object_id=OuterRef('pk')))
    #         )

    return qs



def playlist_list_by_id_order(ids: list[int]) -> QuerySet[Playlist]:
    '''Retrieves playlists by their IDs in the order specified by watchlist_ids'''
    
    # Select the playlists that are in the watchlist
    qs = Playlist.objects.filter(pk__in=ids)
    
    # Annotate the queryset with the order of the IDs
    maintain_order = Case(*[When(pk=pki, then=idx) for idx, pki in enumerate(ids)])
    return qs.order_by(maintain_order)


def movies_dataset() -> QuerySet[MovieProxy]:
    '''Retrieves movies and formats them for further processing.'''
    qs = MovieProxy.objects.all()
    qs = qs.annotate(movieId=F('id'), movieIdx=F("idx"))
    return qs.values('movieIdx', 'movieId', 'title', 'release_date', 'rating_count', 'rating_avg')