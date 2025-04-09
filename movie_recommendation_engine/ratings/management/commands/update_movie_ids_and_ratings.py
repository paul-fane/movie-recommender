from django.core.management.base import BaseCommand
from movie_recommendation_engine.ratings.tasks import task_update_movie_ratings
from django.db import DataError
from django.forms.models import model_to_dict
import pandas as pd
from django.conf import settings
from movie_recommendation_engine.playlists.models import MovieProxy
from movie_recommendation_engine.ratings.models import Rating
import os

LINKS_SMALL_CSV = os.path.join(settings.DATA_DIR, "links_small.csv")
MOVIES_CSV = os.path.join(settings.DATA_DIR, "movies_metadata.csv")


def enrich_imdb_col(val):
    val = str(val)
    if len(val) == 7:
        val = f"tt{val}"
        return val
    if len(val) == 6:
        val = f"tt0{val}"
        return val
    if len(val) == 5:
        val = f"tt00{val}"
        return val
    return val



class Command(BaseCommand):
    help = "Adapted from nbs/Update Movie IDs and Ratings.ipynb"
    
    def handle(self, *args, **options):
        if not LINKS_SMALL_CSV:
            print(f"{LINKS_SMALL_CSV} does not exist")
            return 
        if not MOVIES_CSV:
            print(f"{MOVIES_CSV} does not exist")
            return 
        
        
        qs = Rating.objects.all()
        missing_movie_ids = []
        for instance in qs:
            if instance.content_object is None:
                missing_movie_ids.append(instance.object_id)

                
        _total = len(missing_movie_ids)
        total_missing = list(set(missing_movie_ids))
        print(len(total_missing), _total, qs.count())
        
        links_df = pd.read_csv(LINKS_SMALL_CSV)
        
        ms_df = links_df.copy()[links_df.movieId.isin(total_missing)]
        
        #ms_df.shape[0] == len(total_missing)
        
        ms_df['tt'] = ms_df['imdbId'].apply(enrich_imdb_col)
        
        
        
        movies_cols = ['title', 'overview', 'release_date', 'imdb_id']
        movies_df = pd.read_csv(MOVIES_CSV, usecols=movies_cols)
        
        missing_movies_df = ms_df.merge(movies_df, left_on='tt', right_on='imdb_id')
        
        missing_movies_df['id'] = missing_movies_df['movieId']
        missing_movies_df['id_alt'] = missing_movies_df['tmdbId'].apply(lambda x: str(int(x)))
        
        final_df = missing_movies_df.copy()[['id', 'id_alt', 'title']]
        final_df['id_alt'] = final_df['id_alt'].astype(str)
        
        alt_id_list = final_df['id_alt'].to_list()
        
        movies_qs = MovieProxy.objects.filter(id__in=alt_id_list)
        for obj in movies_qs:
            data = final_df.copy()[final_df['id_alt'] == str(obj.id)]
            if data.shape[0] == 1:
                og_model_data = model_to_dict(obj)
                update_data = data.to_dict('records')[0]
                if obj.title == update_data.get('title'): 
                    #print(og_model_data)
                    og_model_data['id'] = update_data['id']
                    new_model_data = {**og_model_data}
                    try:
                        obj.id =new_model_data["id"]
                        obj.save()
                    except DataError:
                        print(f"Skipping invalid row: {new_model_data["id"]}")
                        continue
        task_update_movie_ratings()
        