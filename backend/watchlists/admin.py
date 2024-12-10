from django.contrib import admin

# Register your models here.
from .models import Watchlist



class WatchlistAdmin(admin.ModelAdmin):
    list_display = ['content_object', 'user']
    search_fields = ['user__username']
    #search_fields = ['object_id']
    raw_id_fields = ['user']
    readonly_fields = ['content_object']

admin.site.register(Watchlist, WatchlistAdmin)