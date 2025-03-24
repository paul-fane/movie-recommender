from rest_framework.views import APIView
from rest_framework import serializers
from movie_recommendation_engine.playlists.selectors import dashboard_movie_list
from movie_recommendation_engine.playlists.serializers import PlaylistSerializer
from movie_recommendation_engine.api.pagination import (
    LimitOffsetPagination,
    get_paginated_response,
)
    
class PlaylistListView(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 20
        
    class FilterSerializer(serializers.Serializer):
        category = serializers.ChoiceField(choices=["all", "movies", "shows", "playlists"] )
        sort_by = serializers.ChoiceField(choices=["popular", "unpopular", "-rating_avg", "rating_avg", "-release_date", "release_date"])
        query = serializers.CharField(required=False)
    
    def get(self, request):
        
        # Make sure the filters are valid, if passed
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        
        movies = dashboard_movie_list(user=request.user, filters=filters_serializer.validated_data)
    
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=PlaylistSerializer,
            queryset=movies,
            request=request,
            view=self,
        )
    