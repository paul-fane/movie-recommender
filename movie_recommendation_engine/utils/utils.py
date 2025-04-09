import os
import csv
import datetime
import ast
import re
from django.db import IntegrityError
from django.conf import settings
from movie_recommendation_engine.common.models import PublishStateOptions
from movie_recommendation_engine.playlists.models import  Playlist, MovieProxy
from movie_recommendation_engine.categories.models import Category
from movie_recommendation_engine.videos.models import Video
from movie_recommendation_engine.users.models import BaseUser
from faker import Faker


MOVIE_METADATA_CSV = os.path.join(settings.DATA_DIR, "movies_metadata.csv")
YT_MOVIE_TRAILER_CSV = os.path.join(settings.DATA_DIR, "ml-youtube.csv")


def get_fake_profiles(count=10):
    fake = Faker()
    user_data = []
    for _ in range(count):
        profile = fake.profile()
        data = {
            #"username": profile.get('username'),
            "email": profile.get('mail'),
            "is_active": True
        }
        # if 'name' in profile:
        #     fname, lname = profile.get('name').split(" ")[:2]
        #     data['first_name'] = fname
        #     data['last_name'] = lname
        user_data.append(data)
    return user_data

def generate_users(count=10):
    profiles = get_fake_profiles(count=count)
    new_users = []
    for profile in profiles:
        new_users.append(
            BaseUser(**profile)
        )
    user_bulk = BaseUser.objects.bulk_create(new_users, ignore_conflicts=True)
    print(f"New users: {len(user_bulk)}")
    print(f"Total users: {BaseUser.objects.count()}")

def validate_date_str(date_text):
    try:
        datetime.datetime.strptime(date_text, "%Y-%m-%d")
    except:
        return None
    return date_text

def load_movie_data(limit=1, verbose=True):
    with open(MOVIE_METADATA_CSV, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        dataset = []
        for i, row in enumerate(reader):
            _id = row.get("id")
            try:
                _id = int(_id)
            except:
                _id = None
            release_date = validate_date_str(row.get('release_date'))
            if not row.get('title'):
                continue # Skip if no title is found
            data = {
                "id": _id,
                "title": row.get('title'),
                "type": Playlist.PlaylistTypeChoices.MOVIE,
                "overview": row.get("overview"),
                "release_date": release_date,
                "state": PublishStateOptions.PUBLISH,
                "poster_path": row.get('poster_path'),
            }
            dataset.append(data)
            if i + 1 > limit:
                break
        return dataset


def save_movie_data(limit=1, verbose=True):
    with open(MOVIE_METADATA_CSV, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        dataset = []
        for i, row in enumerate(reader):
            _id = row.get("id")
            try:
                _id = int(_id)
            except:
                _id = None
            release_date = validate_date_str(row.get('release_date'))
            data = {
                "id": _id,
                "title": row.get('title'),
                "type": Playlist.PlaylistTypeChoices.MOVIE,
                "overview": row.get("overview"),
                "release_date": release_date,
                "state": PublishStateOptions.PUBLISH,
                "poster_path": row.get('poster_path'),
            }
            dataset.append(data)
            if i + 1 > limit:
                break
        movies_new = [MovieProxy(**x) for x in dataset]
        movies_bulk = MovieProxy.objects.bulk_create(movies_new, ignore_conflicts=True)
        print(f"New movies: {len(movies_bulk)}")
        print(f"Total movies: {MovieProxy.objects.count()}")



def add_category_to_movie():
    with open(MOVIE_METADATA_CSV, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            categorys = row.get('genres')
            title = row.get('title')
            movie = Playlist.objects.filter(title=title).first()
            if not movie:
                continue  # Skip if no matching movie is found
            categorys_json = ast.literal_eval(categorys)
            if movie:
                for category in categorys_json:
                    if category:
                        category, created = Category.objects.get_or_create(title=category['name'])
                        movie.category.add(category)
            
            
        # distinct_items = list(set(dataset))
        # for category in distinct_items:
        #     print(category)
        #     print('created')
        #     Category.objects.create(title=category)
        
 
                
                
       
def add_video_to_movie():
    with open(YT_MOVIE_TRAILER_CSV, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            youtube_id = row.get('youtubeId')
            title = row.get('title')

            # Remove year from title (e.g., "Movie Title (2023)" -> "Movie Title")
            title_cleaned = re.sub(r'\s*\(.*?\)', '', title)

            # Get the movie from the database
            movie = Playlist.objects.filter(title=title_cleaned).first()
            if not movie:
                continue  # Skip if no matching movie is found

            try:
                # Create video if it doesn't exist
                video, created = Video.objects.get_or_create(
                    video_id=youtube_id,
                    defaults={'title': title_cleaned, 'state': PublishStateOptions.PUBLISH}
                )

                # Assign video to movie and save it
                if movie.video != video:  # Avoid unnecessary saves
                    movie.video = video
                    movie.save()

            except IntegrityError:
                continue  
                