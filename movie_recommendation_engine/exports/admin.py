from django.contrib import admin

# Register your models here.
from movie_recommendation_engine.exports.models import Export

class ExportAdmin(admin.ModelAdmin):
    list_display = ['type', 'timestamp', 'latest']
    list_filter = ['latest', 'type', 'timestamp', ]

admin.site.register(Export, ExportAdmin)