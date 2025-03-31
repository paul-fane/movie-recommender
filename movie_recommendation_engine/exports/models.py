import uuid
import pathlib
from django.db import models

from movie_recommendation_engine.exports import storages as exports_storages
from movie_recommendation_engine.exports.utils import export_file_handler


class ExportDataType(models.TextChoices):
    RATINGS = 'ratings', 'Ratings'
    MOVIES = 'movies', 'Movies'
    SURPRISE = 'surprise', 'Surprise'

class Export(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    file = models.FileField(upload_to=export_file_handler, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20, choices=ExportDataType.choices, default=ExportDataType.RATINGS)
    latest = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Aftere saving the file in the "exports/{dtype}/{today}/{new_fname}" path
        # Seve the current instance file also as the latest file in the "exports/{self.type}/latest{ext}" path
        # Overwriteing the previous latest file
        # Change the latest field to False for the previous latest file 
        if self.latest and self.file:
            file = self.file
            ext = pathlib.Path(file.name).suffix
            path = f"exports/{self.type}/latest{ext}"
            exports_storages.save(path, file, overwrite=True)
            qs = Export.objects.filter(type=self.type).exclude(pk=self.pk)
            qs.update(latest=False)