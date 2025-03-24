from django.contrib import admin

from movie_recommendation_engine.ratings.models import Rating 

class RatingAdmin(admin.ModelAdmin):
    list_display = ['content_object', 'user', 'value', 'active']
    search_fields = ['user__username']
    #search_fields = ['object_id']
    raw_id_fields = ['user']
    readonly_fields = ['content_object']

admin.site.register(Rating, RatingAdmin)