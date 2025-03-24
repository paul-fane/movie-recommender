from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PublishStateOptions(models.TextChoices):
    # CONSTANT = DB_VALUE, USER_DISPLAY_VA
    PUBLISH = 'PU', 'Publish'
    DRAFT = 'DR', 'Draft'
    UNLISTED = 'UN', 'Unlisted'
    PRIVATE = 'PR', 'Private'