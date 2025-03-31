import uuid
import pathlib
from django.utils import timezone


def export_file_handler(instance, filename):
    today = timezone.now().strftime("%Y-%m-%d")
    fpath = pathlib.Path(filename)
    ext = fpath.suffix # .csv
    dtype = instance.type
    if hasattr(instance, 'id'):
        new_fname = f"{instance.id}{ext}"
    else:
        new_fname = f"{uuid.uuid4()}{ext}"
    return f"exports/{dtype}/{today}/{new_fname}"