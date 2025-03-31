from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.django.base")

app = Celery("movie_recommendation_engine")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "run_playlists_rating_avg": {
      'task': 'task_update_playlists_ratings',
      'schedule' : 60 * 30,  
    },
    "run_movie_rating_avg_every_30": {
        'task': 'task_update_movie_ratings',
        'schedule': 60 * 30, # 30 min,
    },
    "daily_movie_idx_refresh": {
        "task": "movie_recommendation_engine.playlists.tasks.update_movie_position_embedding_idx",
        "schedule":  crontab(hour=1, minute=0)
    },
    "daily_rating_dataset_export": {
        "task": "export_rating_dataset",
        "schedule": crontab(hour=1, minute=30)
    },
    "daily_rating_dataset_export": {
        "task": "export_movies_dataset",
        "schedule": crontab(hour=2, minute=15)
    },
    "daily_train_surprise_model": {
        "task": "movie_recommendation_engine.ml.tasks.train_surprise_model_task",
        "schedule": crontab(hour=3, minute=0)
    },
    "daily_model_inference": {
        "task": "movie_recommendation_engine.ml.tasks.batch_users_prediction_task",
        "schedule": crontab(hour=4, minute=30),
        "kwargs": {"max_pages": 5000, "offset": 200}
    },
    
}