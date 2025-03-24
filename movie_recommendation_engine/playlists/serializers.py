from rest_framework import serializers
from movie_recommendation_engine.playlists.models import Playlist, MovieProxy, TVShowProxy, TVShowSeasonProxy
from movie_recommendation_engine.categories.models import Category
from movie_recommendation_engine.videos.models import Video

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['video_id']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title']

class PlaylistSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)
    #has_watched = serializers.BooleanField(required=False)
    in_watchlist = serializers.BooleanField(required=False)
    user_rate = serializers.IntegerField(required=False)
    
    class Meta:
        model = Playlist
        fields = '__all__'
        
        
    
    
class MovieDetailSerializer(serializers.ModelSerializer):
    video = VideoSerializer(read_only=True)
    category = CategorySerializer(many=True, read_only=True)
    in_watchlist = serializers.BooleanField(required=False)
    user_rate = serializers.IntegerField(required=False)
    class Meta:
        model = MovieProxy
        fields = '__all__'
        

        
class PlaylistDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)
    in_watchlist = serializers.BooleanField(required=False)
    user_rate = serializers.IntegerField(required=False)
    class Meta:
        model = Playlist
        fields = '__all__'
    
    
class SeasonDetailSerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()
    in_watchlist = serializers.BooleanField(required=False)
    user_rate = serializers.IntegerField(required=False)
    class Meta:
        model = TVShowSeasonProxy
        fields = '__all__'
        
    def get_parent(self, obj):
        return obj.parent.title
        
        
        
        
class TVShowDetailSerializer(serializers.ModelSerializer):
    video = VideoSerializer(read_only=True)
    seasons = serializers.SerializerMethodField()
    category = CategorySerializer(many=True, read_only=True)
    in_watchlist = serializers.BooleanField(required=False)
    user_rate = serializers.IntegerField(required=False)
    class Meta:
        model = TVShowProxy
        fields = '__all__'
        
    def get_seasons(self, obj):
        # Access the seasons property from the model instance
        seasons = obj.seasons
        return PlaylistSerializer(seasons, many=True).data
        
        
class PlaylistRelatedSerializer(serializers.ModelSerializer):
    playlist = PlaylistDetailSerializer(many=True, read_only=True)
    related = PlaylistDetailSerializer(many=True, read_only=True)
    in_watchlist = serializers.BooleanField(required=False)
    user_rate = serializers.IntegerField(required=False)
    class Meta:
        model = TVShowProxy
        fields = '__all__'