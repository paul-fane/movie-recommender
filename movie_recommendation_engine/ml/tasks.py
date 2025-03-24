from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from celery import shared_task
from movie_recommendation_engine.playlists.models import MovieProxy
from movie_recommendation_engine.users import utils as users_utils
from movie_recommendation_engine.ml import utils as ml_utils

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
    model = ml_utils.load_model()
    
    Suggestion = apps.get_model('suggestions', 'Suggestion')
    ctype = ContentType.objects.get_for_model(MovieProxy, for_concrete_model=False)
    
    
    # Fetching Movies and Users
    end_page = start_page + offset
    # If users_ids is not provided, the function fetches recent users
    if users_ids is None:
        users_ids = users_utils.get_recent_users()
        
    # Retrieves popular movie IDs in the range [start_page:end_page].
    # The "start_page" is the number of alredy existing suggestions for those movies
    movie_ids = MovieProxy.objects.all().popular().values_list('id', flat=True)[start_page:end_page]
    
    # Fetches movies that have already been suggested to the users to avoid duplicate recommendations.
    recently_suggested = Suggestion.objects.get_recently_suggested(movie_ids, users_ids)
    new_suggestion = []
    if not movie_ids.exists():
        return 
    
    # The function iterates over the movies and users
    # Skips users who already have suggestions for the movie or if the user/movie data is invalid.
    for movie_id in movie_ids:
        users_done = recently_suggested.get(f"{movie_id}") or []
        for u in users_ids:
            if u in users_done:
                # print(movie_id, 'is done for', u, 'user')
                continue
            if u is None:
                continue
            if movie_id is None:
                continue
            # The model predicts the estimated rating (pred) for a user (uid) and a movie (iid).
            # est is the predicted rating value.
            pred = model.predict(uid=u, iid=movie_id).est
            data = {
                'user_id': u,
                'object_id': movie_id,
                'value': pred,
                'content_type': ctype
            }
            try:
                obj, _ = Suggestion.objects.get_or_create(user_id=u, object_id=movie_id, content_type=ctype)
            except Suggestion.MultipleObjectsReturned:
                # If duplicate Suggestion objects are found, they are deleted
                qs = Suggestion.objects.filter(user_id=u, object_id=movie_id, content_type=ctype)
                obj = qs.first()
                to_delete = qs.exclude(id=obj.id)
                to_delete.delete()
            # Updates the predicted rating if it has changed
            if obj.value != pred:
                obj.value = pred
                obj.save()
                
    # Continues to the next batch of movies if the maximum number of pages (max_pages) hasn't been reached.
    if end_page < max_pages:
        return batch_users_prediction_task(start_page=end_page-1)