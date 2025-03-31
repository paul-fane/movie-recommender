from celery import shared_task

from movie_recommendation_engine.exports.services import export_dataset
from movie_recommendation_engine.exports.models import ExportDataType
from movie_recommendation_engine.ratings.selectors import ratings_dataset
from movie_recommendation_engine.playlists.selectors import movies_dataset

@shared_task(name='export_rating_dataset')
def export_rating_dataset_task():
    dataset = ratings_dataset()
    export_dataset(dataset=dataset, fname='ratings.csv', type=ExportDataType.RATINGS)

@shared_task(name='export_movies_dataset')
def export_movies_dataset_task():
    dataset = movies_dataset()
    export_dataset(dataset=dataset, fname='movies.csv', type=ExportDataType.MOVIES)