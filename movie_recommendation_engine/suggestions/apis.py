from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
#from watchlists.models import Watchlist

from movie_recommendation_engine.suggestions.selectors import suggestions_list
from rest_framework import serializers, status
from movie_recommendation_engine.playlists.serializers import PlaylistSerializer
from movie_recommendation_engine.api.pagination import (
    LimitOffsetPagination,
    get_paginated_response,
)

class SuggestionsListView(APIView):
    permission_classes = [IsAuthenticated]
    
    class Pagination(LimitOffsetPagination):
        default_limit = 20
        
    class FilterSerializer(serializers.Serializer):
        category = serializers.ChoiceField(choices=["all", "movies", "shows"] )
        query = serializers.CharField(required=False)
    
    def get(self, request):
        
        # Make sure the filters are valid, if passed
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        
        movies = suggestions_list(user=request.user, filters=filters_serializer.validated_data)
        
        # if not movies:
        #     return Response(status=status.HTTP_204_NO_CONTENT)
        
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=PlaylistSerializer,
            queryset=movies,
            request=request,
            view=self,
        )