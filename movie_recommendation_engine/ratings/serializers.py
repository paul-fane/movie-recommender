from rest_framework import serializers
from movie_recommendation_engine.ratings.models import Rating

class RateSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    
    class Meta:
        model = Rating
        fields = ['id','username', 'value', 'review_text', 'timestamp']
        
    def get_username(self, obj):
        return obj.user.username
    

class RatePlaylistSerializer(serializers.ModelSerializer):
    playlist = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    
    class Meta:
        model = Rating
        fields = ['id','username','playlist', 'value', 'review_text', 'timestamp']
        
    def get_username(self, obj):
        return obj.user.username
    
    def get_playlist(self, obj):
        # Retrieve the related object using the GenericForeignKey
        if obj.content_object:
            # Return a representation of the object (you can customize this)
            return {
                "id": obj.content_object.id,
                "title": getattr(obj.content_object, 'title', str(obj.content_object)),
                "type": getattr(obj.content_object, 'type', str(obj.content_object)),
                "slug": getattr(obj.content_object, 'slug', str(obj.content_object)) 
            }
            #return getattr(obj.content_object, 'title', str(obj.content_object)) 
        return None