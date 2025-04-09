import random
import time
import datetime
import decimal 
from celery import shared_task
from django.db.models import Avg, Count
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from faker import Faker

from movie_recommendation_engine.playlists.models import MovieProxy, Playlist
from movie_recommendation_engine.ratings.models import Rating, RatingChoices
from movie_recommendation_engine.users.models import BaseUser

@shared_task(name='generate_fake_reviews')
def generate_fake_reviews(count=100, users=10, null_avg=False):
    user_s = BaseUser.objects.first() # 1
    user_e = BaseUser.objects.last()
    random_user_ids = random.sample(range(user_s.id, user_e.id), users)
    users = BaseUser.objects.filter(id__in=random_user_ids)
    movies = MovieProxy.objects.all().order_by("?")[:count]
    # movie_ctype = ContentType.objects.get_for_model(MovieProxy, for_concrete_model=False)
    if null_avg:
        movies = MovieProxy.objects.filter(rating_avg__isnull=True).order_by("?")[:count]
    n_ratings = movies.count()
    rating_choices = [x for x in RatingChoices.values if x is not None] # 1,2,3,4,5
    user_ratings = [random.choice(rating_choices) for _ in range(0, n_ratings)]
    
    new_ratings = []
    for movie in movies:
        rating_obj = Rating.objects.create(
            content_object=movie,
            # content_type=movie_ctype,
            # object_id=movie.id,
            value=user_ratings.pop(),
            user=random.choice(users),
            review_text=Faker().text(max_nb_chars=80),
        )
        new_ratings.append(rating_obj.id)
    return new_ratings



@shared_task(name='task_update_movie_ratings')
def task_update_movie_ratings(object_id=None):
    start_time = time.time()
    
    # for_concrete_model=False allows fetching the ContentType of a proxy model
    ctype = ContentType.objects.get_for_model(MovieProxy, for_concrete_model=False)
    rating_qs = Rating.objects.filter(content_type=ctype, active=True)
    
    if object_id is not None:
        rating_qs = rating_qs.filter(object_id=object_id)
        
    # Groups records by object_id
    # For each group (each distinct object_id), it calculates the average of the value field.
    # It also counts how many times each object_id appears in the queryset.
    agg_ratings = rating_qs.values('object_id').annotate(average=Avg('value'), count=Count('object_id')) # [{'object_id':1, 'avarage':4.5, 'count':2}, ...]
    
    for agg_rate in agg_ratings:
        object_id = agg_rate['object_id']
        rating_avg = agg_rate['average']
        rating_count = agg_rate['count']
        
        # Calculate the score based on the average rating and count
        score = decimal.Decimal(rating_avg * rating_count * 1.0)
        
        # Update the Movie with the new rating information
        qs = MovieProxy.objects.filter(id=object_id)
        qs.update(
            rating_avg=rating_avg,
            rating_count=rating_count,
            score=score,
            rating_last_updated=timezone.now()
        )
        
    # Calculate the total time taken for the task
    total_time = time.time() - start_time
    delta = datetime.timedelta(seconds=int(total_time))
    print(f"Rating update took {delta} ({total_time}s)")
    
    
@shared_task(name='task_update_playlists_ratings')
def task_update_playlists_ratings(object_id=None):
    start_time = time.time()
    
    # for_concrete_model=False allows fetching the ContentType of a proxy model
    rating_qs = Rating.objects.filter(active=True)
    
    if object_id is not None:
        rating_qs = rating_qs.filter(object_id=object_id)
        
    # Groups records by object_id
    # For each group (each distinct object_id), it calculates the average of the value field.
    # It also counts how many times each object_id appears in the queryset.
    agg_ratings = rating_qs.values('object_id').annotate(average=Avg('value'), count=Count('object_id')) # [{'object_id':1, 'avarage':4.5, 'count':2}, ...]
    
    for agg_rate in agg_ratings:
        object_id = agg_rate['object_id']
        rating_avg = agg_rate['average']
        rating_count = agg_rate['count']
        
        # Calculate the score based on the average rating and count
        score = decimal.Decimal(rating_avg * rating_count * 1.0)
        
        # Update the Playlist with the new rating information
        qs = Playlist.objects.filter(id=object_id)
        qs.update(
            rating_avg=rating_avg,
            rating_count=rating_count,
            score=score,
            rating_last_updated=timezone.now()
        )
        
    # Calculate the total time taken for the task
    total_time = time.time() - start_time
    delta = datetime.timedelta(seconds=int(total_time))
    print(f"Rating update took {delta} ({total_time}s)")