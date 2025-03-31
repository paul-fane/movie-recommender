from django.db.models import Subquery, Exists, OuterRef
from movie_recommendation_engine.playlists.models import Playlist, MovieProxy, TVShowProxy #type=Playlist.PlaylistTypeChoices.PLAYLIST

#from watchlists.models import Watchlist
from movie_recommendation_engine.ratings.models import Rating
from movie_recommendation_engine.watchlists.models import Watchlist
from django.db.models.query import QuerySet
from django.db.models import F
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
            qs = qs.popular()
        elif sort_by == 'unpopular':
            qs = qs.popular(reverse=True)
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

    return qs



def movies_dataset() -> QuerySet[MovieProxy]:
    '''Retrieves movies and formats them for further processing.'''
    qs = MovieProxy.objects.all()
    qs = qs.annotate(movieId=F('id'), movieIdx=F("idx"))
    return qs.values('movieIdx', 'movieId', 'title', 'release_date', 'rating_count', 'rating_avg')