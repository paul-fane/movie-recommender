from django.contrib import admin

# Register your models here.
from movie_recommendation_engine.categories.models import Category

admin.site.register(Category)