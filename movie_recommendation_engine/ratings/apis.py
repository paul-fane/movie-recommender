from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from rest_framework import serializers, status
from movie_recommendation_engine.ratings.services import rating_create
from movie_recommendation_engine.ratings.selectors import ratings_list, compar_ratings_list
from movie_recommendation_engine.ratings.serializers import RateSerializer, RatePlaylistSerializer
from movie_recommendation_engine.api.pagination import (
    LimitOffsetPagination,
    get_paginated_response,
)

class RateCreateView(APIView):
    permission_classes = [IsAuthenticated]
        
    class FilterSerializer(serializers.Serializer):
        object_id = serializers.IntegerField()
        rating_value = serializers.IntegerField()
        ctype = serializers.CharField()
        review_text = serializers.CharField(required=False, allow_blank=True)
    
    def post(self, request):
        serializer = self.FilterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        rating_create(data=serializer.validated_data, user=request.user, request=request)
        return Response(status=status.HTTP_201_CREATED)
    

        
class RateListBaseView(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 20

    class FilterSerializer(serializers.Serializer):
        query = serializers.CharField(required=True)

    def get(self, request, *args, **kwargs):
        # Make sure the filters are valid, if passed
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        # Determine which parameter is provided
        playlist_id = kwargs.get('playlist_id')
        user_username = kwargs.get('user_username')

        if playlist_id:
            ratings = ratings_list(playlist_id=playlist_id, filters=filters_serializer.validated_data)
            serializer_class = RateSerializer
        elif user_username:
            ratings = ratings_list(user_username=user_username, filters=filters_serializer.validated_data)
            serializer_class = RatePlaylistSerializer
        else:
            return Response({'error': 'Invalid request'}, status=400)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=serializer_class,
            queryset=ratings,
            request=request,
            view=self,
        )
        
        
class CompareRateListView(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 20
        
    class FilterSerializer(serializers.Serializer):
        query = serializers.CharField(required=True)
        
    def get(self, request, user_username, *args, **kwargs):
        # Make sure the filters are valid, if passed
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        
        ratings = compar_ratings_list(user= request.user, user_username=user_username, filters=filters_serializer.validated_data)
        
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=RatePlaylistSerializer,
            queryset=ratings,
            request=request,
            view=self,
        )