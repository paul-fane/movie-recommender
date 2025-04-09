from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Subquery, Exists, OuterRef

from movie_recommendation_engine.playlists.models import Playlist, MovieProxy, TVShowProxy, TVShowSeasonProxy, PlaylistRelated
from movie_recommendation_engine.playlists.serializers import MovieDetailSerializer, PlaylistDetailSerializer, TVShowDetailSerializer, SeasonDetailSerializer, PlaylistRelatedSerializer
from movie_recommendation_engine.watchlists.models import Watchlist
from movie_recommendation_engine.ratings.models import Rating


class MovieDetailView(APIView):
    
    def get(self, request, slug, *args, **kwargs):
        movie = MovieProxy.objects.filter(slug=slug)
        print(slug)
        print(movie)
        user = request.user
        
        if user.is_authenticated:
            movie = movie.annotate(
                user_rate=Subquery(Rating.objects.filter(user=user, object_id=OuterRef('pk'), active=True).values('value')),
                in_watchlist=Exists(Watchlist.objects.filter(user=user, object_id=OuterRef('pk')))
            )
        
        serializer = MovieDetailSerializer(movie[0])
        return Response(serializer.data)
        
        
    
class PlaylistDetailView(APIView):
    def get(self, request, slug, *args, **kwargs):
        playlist = Playlist.objects.filter(slug=slug)
        # related_playlists = playlist.playlists_related.all()
        
        
        user = request.user
        if user.is_authenticated:
            playlist = playlist.annotate(
                user_rate=Subquery(Rating.objects.filter(user=user, object_id=OuterRef('pk'), active=True).values('value')),
                in_watchlist=Exists(Watchlist.objects.filter(user=user, object_id=OuterRef('pk')))
            )
        
        serializer = PlaylistRelatedSerializer(playlist[0])
        return Response(serializer.data)
    
    
    
class TVShowDetailView(APIView):
    
    def get(self, request, slug, *args, **kwargs):
        movie = TVShowProxy.objects.filter(slug=slug)
        
        user = request.user
        
        if user.is_authenticated:
            movie = movie.annotate(
                user_rate=Subquery(Rating.objects.filter(user=user, object_id=OuterRef('pk'), active=True).values('value')),
                in_watchlist=Exists(Watchlist.objects.filter(user=user, object_id=OuterRef('pk')))
            )
        
        serializer = TVShowDetailSerializer(movie[0])
        return Response(serializer.data)
    
    
class SeasonDetailView(APIView):
    
    def get(self, request, slug, *args, **kwargs):
        season = TVShowSeasonProxy.objects.filter(slug=slug)
        user = request.user
        
        if user.is_authenticated:
            season = season.annotate(
                user_rate=Subquery(Rating.objects.filter(user=user, object_id=OuterRef('pk'), active=True).values('value')),
                in_watchlist=Exists(Watchlist.objects.filter(user=user, object_id=OuterRef('pk')))
            )
        
        serializer = SeasonDetailSerializer(season[0])
        return Response(serializer.data)