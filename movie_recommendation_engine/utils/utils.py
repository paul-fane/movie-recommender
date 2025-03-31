import os
import csv
import datetime
from pprint import pprint
from django.conf import settings

from movie_recommendation_engine.common.models import PublishStateOptions
from movie_recommendation_engine.playlists.models import  Playlist
from movie_recommendation_engine.categories.models import Category
from movie_recommendation_engine.videos.models import Video
from faker import Faker


MOVIE_METADATA_CSV = os.path.join(settings.DATA_DIR, "movies_metadata.csv")
YT_MOVIE_TRAILER_CSV = os.path.join(settings.DATA_DIR, "ml-youtube.csv")

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
            data = {
                "id": _id,
                "title": row.get('title'),
                "type": Playlist.PlaylistTypeChoices.MOVIE,
                "overview": row.get("overview"),
                "release_date": release_date,
                "state": PublishStateOptions.PUBLISH
            }
            dataset.append(data)
            if i + 1 > limit:
                break
        return dataset


def get_fake_profiles(count=10):
    fake = Faker()
    user_data = []
    for _ in range(count):
        profile = fake.profile()
        data = {
            "username": profile.get('username'),
            "email": profile.get('mail'),
            "is_active": True
        }
        if 'name' in profile:
            fname, lname = profile.get('name').split(" ")[:2]
            data['first_name'] = fname
            data['last_name'] = lname
        user_data.append(data)
    return user_data


import ast
def add_category_to_movie(limit=1):
    with open(MOVIE_METADATA_CSV, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        dataset = []
        for i, row in enumerate(reader):
            categorys = row.get('genres')
            title = row.get('title')
            movie = Playlist.objects.filter(title=title)
            categorys_json = ast.literal_eval(categorys)
            if movie:
                for category in categorys_json:
                    if category:
                        category = Category.objects.get(title=category['name'])
                        movie[0].category.add(category)
            
            # if i + 1 > limit:
            #     break
            
        # distinct_items = list(set(dataset))
        # for category in distinct_items:
        #     print(category)
        #     print('created')
        #     Category.objects.create(title=category)
        
        
def add_image_path_to_movie():
    with open(MOVIE_METADATA_CSV, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        dataset = []
        for i, row in enumerate(reader):
            poster_path = row.get('poster_path')
            title = row.get('title')
            movie = Playlist.objects.filter(title=title)
            if movie:
                movie[0].poster_path = poster_path
                movie[0].save()
                
                
import re
from django.db import IntegrityError
def add_video_to_movie():
    with open(YT_MOVIE_TRAILER_CSV, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        dataset = []
        for i, row in enumerate(reader):
            youtubeId = row.get('youtubeId')
            title = row.get('title')
            title_result = re.sub(r'\s*\(.*?\)', '', title) # Title without Year
            movie = Playlist.objects.filter(title=title_result)
            # print(youtubeId, title, title_result)
            # if movie:
            #     print("Movie")
            #     print(movie[0])
            if movie:
                try:
                    video = Video.objects.create(title=title_result, video_id=youtubeId, state=PublishStateOptions.PUBLISH)
                    movie[0].video = video
                    movie[0].save()
                except IntegrityError:
                    continue