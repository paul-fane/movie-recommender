from config.env import env


# https://docs.celeryproject.org/en/stable/userguide/configuration.html


CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'

CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="redis://redis:6379/0")
CELERY_RESULT_BACKEND = "django-db"

CELERY_TIMEZONE = "UTC"
