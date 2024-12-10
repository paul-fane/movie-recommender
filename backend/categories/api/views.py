from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from ..models import Category

class WatchlistCreateView(APIView):
    class OutputSerializer(serializers.Serializer):
        title = serializers.CharField()
        
    def get(self, request):
        category_list = Category.objects.all()
        
        serializer = self.OutputSerializer(category_list, many=True)
        return Response(serializer.data)