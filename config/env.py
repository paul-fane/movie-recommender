import environ
from django.core.exceptions import ImproperlyConfigured

env = environ.Env()

BASE_DIR = environ.Path(__file__) - 2
APPS_DIR = BASE_DIR.path("movie_recommendation_engine")