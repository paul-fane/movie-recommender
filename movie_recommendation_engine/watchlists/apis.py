from rest_framework.response import Response
from movie_recommendation_engine.watchlists.models import Watchlist
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from movie_recommendation_engine.playlists.serializers import PlaylistSerializer
from movie_recommendation_engine.api.pagination import (
    LimitOffsetPagination,
    get_paginated_response,
)
from rest_framework import serializers, status
from django.shortcuts import get_object_or_404
from movie_recommendation_engine.watchlists.services import watchlist_create
from movie_recommendation_engine.watchlists.selectors import watchlist_list


class WatchlistListView(APIView):
    permission_classes = [IsAuthenticated]
    
    class Pagination(LimitOffsetPagination):
        default_limit = 50
    
    def get(self, request):
        
        watchlist = watchlist_list(user=request.user)
    
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=PlaylistSerializer,
            queryset=watchlist,
            request=request,
            view=self,
        )
        
class WatchlistCreateView(APIView):
    permission_classes = [IsAuthenticated]
        
    class InputSerializer(serializers.Serializer):
        object_id = serializers.IntegerField()
        ctype = serializers.CharField()
    
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        watchlist_create(data=serializer.validated_data, user=request.user)
        return Response(status=status.HTTP_201_CREATED)
        
        
class WatchlistDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, *args, **kwargs):
        # Fetch the movie instance or return 404 if not found
        watchlist = get_object_or_404(Watchlist, object_id=pk, user=request.user)
        #watchlist = Watchlist.objects.get(user=request.user, object_id=pk)
        # Delete the instance
        watchlist.delete()
        
        # Return a successful response
        return Response(status=status.HTTP_204_NO_CONTENT)