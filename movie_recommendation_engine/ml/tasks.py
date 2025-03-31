from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from celery import shared_task
from movie_recommendation_engine.playlists.models import MovieProxy
from movie_recommendation_engine.users.selectors import get_recent_users 
from movie_recommendation_engine.ml import utils as ml_utils
from movie_recommendation_engine.exports.selectors import load_model
from movie_recommendation_engine.suggestions.services import generate_suggestions

@shared_task
def train_surprise_model_task(n_epochs=20):
    ml_utils.train_surprise_model(n_epochs=n_epochs)


@shared_task
def batch_users_prediction_task(users_ids=None, start_page=0, offset=50, max_pages=1000):
    """
    The function generates and stores movie recommendations for a batch of users by:
        1.Fetching movies and user profiles.
        2.Predicting ratings for movies for each user using a trained model.
        3.Storing or updating recommendations in the database.

    Args:
        users_ids (list, optional): A list of user IDs for whom recommendations are being generated. Defaults to None.
        start_page (int, optional): Starting index for fetching movies in paginated queries. Defaults to 0.
        offset (int, optional): Number of movies fetched per batch. Defaults to 50.
        max_pages (int, optional): The upper limit for pagination. Defaults to 1000.
    """
    # Load a pre-trained model for collaborative filtering (SVD model from a library like Surprise).
    # SVD (Singular Value Decomposition) is used for matrix factorization in collaborative filtering.
    # The model predicts a user’s rating for a movie based on patterns in training data.
    
    # The model fit the trainset=>(data.buid_full_trainset())
    # The model get the accuracy using rmse algorithm passing the predictions => model.test(trainset.build_testset())
    model = load_model() # load the lattest mode
    
    
    # Fetching Movies and Users
    end_page = start_page + offset
    
    generate_suggestions(model, users_ids, start_page, end_page)
    
                
    # Continues to the next batch of movies if the maximum number of pages (max_pages) hasn't been reached.
    if end_page < max_pages:
        return batch_users_prediction_task(start_page=end_page-1)