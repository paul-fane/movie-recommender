from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import DataError
from django.db.utils import IntegrityError
from movie_recommendation_engine.utils import utils as config_utils
from movie_recommendation_engine.playlists.models import MovieProxy
from movie_recommendation_engine.users.models import BaseUser


# py manage.py loader --users 100 --show-total => To create 100 users
# py manage.py loader --movies --show-total => To create movies

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("count", nargs='?', default=10, type=int)
        parser.add_argument("--movies", action='store_true', default=False)
        parser.add_argument("--users", action='store_true', default=False)
        parser.add_argument("--show-total", action='store_true', default=False)
    
    def handle(self, *args, **options):
        count = options.get('count')
        show_total = options.get('show_total')
        load_movies = options.get('movies')
        generate_users = options.get('users')
        if load_movies:
            movie_dataset = config_utils.load_movie_data(limit=count)
            for movie in movie_dataset:
                try:
                    MovieProxy.objects.create(**movie)
                except DataError:
                    print(f"Skipping invalid movie id: {movie["id"]}")
                    continue
                except IntegrityError:
                    print(f"Movie already exists {movie["id"]}")
                    continue
            
            # movies_new = [MovieProxy(**x) for x in movie_dataset]
            # # Ignore conflicts, in case of duplicate values
            # movies_bulk = MovieProxy.objects.bulk_create(movies_new, ignore_conflicts=True)
            # print(f"New movies: {len(movies_bulk)}")
            if show_total:
                print(f"Total movies: {MovieProxy.objects.count()}")
        if generate_users:
            profiles = config_utils.get_fake_profiles(count=count)
            new_users = []
            for profile in profiles:
                new_users.append(
                    BaseUser(**profile)
                )
            user_bulk = BaseUser.objects.bulk_create(new_users, ignore_conflicts=True)
            print(f"New users: {len(user_bulk)}")
            if show_total:
                print(f"Total users: {BaseUser.objects.count()}")