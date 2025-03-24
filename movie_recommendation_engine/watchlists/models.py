from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = settings.AUTH_USER_MODEL # "auth.User"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    timestamp = models.DateTimeField(auto_now_add=True)
    watched = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'object_id')  # A user can only add a specific item to their watchlist once
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['object_id']),
        ]

    # def __str__(self):
    #     return f'{self.user.username} - {self.object_id.title}'

