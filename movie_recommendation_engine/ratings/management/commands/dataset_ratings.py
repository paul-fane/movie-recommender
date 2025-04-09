from django.core.management.base import BaseCommand
from movie_recommendation_engine.users.models import BaseUser
from django.contrib.contenttypes.models import ContentType
from movie_recommendation_engine.ratings.tasks import task_update_movie_ratings
import os
import pandas as pd
from django.conf import settings

from movie_recommendation_engine.playlists.models import MovieProxy
from movie_recommendation_engine.ratings.models import Rating
import math
from decimal import Decimal

LINKS_SMALL_CSV = os.path.join(settings.DATA_DIR, "links_small.csv")
RATINGS_PATH = os.path.join(settings.DATA_DIR, "ratings_small.csv")



class Command(BaseCommand):
    help = "Adapted from nbs/Load Real Ratings to Fake Users.ipynb"
    
    def handle(self, *args, **options):
        if not LINKS_SMALL_CSV:
            print(f"{LINKS_SMALL_CSV} does not exist")
            return 
        if not RATINGS_PATH:
            print(f"{RATINGS_PATH} does not exist")
            return 
        df = pd.read_csv(RATINGS_PATH)
        df['value'] = df['rating'].apply(lambda x: math.ceil(Decimal(x)))
        df['user_id'] = df['userId']
        df['object_id'] = df['movieId']

        current_users = BaseUser.objects.all().values_list('id', flat=True)
        rating_users = df['userId'].tolist()
        missing_user_ids = set(rating_users) - set(current_users)
        for uid in missing_user_ids:
            BaseUser.objects.create(
                id=uid,
                email=f"dataset-user-{uid}@gmail.com"
            )
        cols = ['user_id', 'value', 'object_id']
        transformed_df = df.copy()[cols]
        rating_records = transformed_df.to_dict('records')
        from movie_recommendation_engine.ratings.models import Rating
        qs = Rating.objects.all()
        qs.delete()
       
        #ctype = ContentType.objects.get(app_label='movies', model='movie')
        ctype = ContentType.objects.get(app_label='playlists', model='movieproxy')
        new_ratings = []
        for r in rating_records:
            r['content_type'] = ctype
            new_ratings.append(
                Rating(**r)
            )
        Rating.objects.bulk_create(new_ratings, ignore_conflicts=True, batch_size=1000)
    
        task_update_movie_ratings()