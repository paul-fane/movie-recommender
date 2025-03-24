import csv
import tempfile

from django.core.files.base import File
from django.db.models import F
from django.contrib.contenttypes.models import ContentType


from movie_recommendation_engine.playlists.models import MovieProxy
from movie_recommendation_engine.ratings.models import Rating

from movie_recommendation_engine.exports.models import Export, ExportDataType

def export_dataset(dataset, fname='dataset.csv', type=ExportDataType.RATINGS):
    with tempfile.NamedTemporaryFile(mode='r+', errors='ignore') as temp_f:
        try:
            keys = dataset[0].keys()
        except:
            return
        dict_writer = csv.DictWriter(temp_f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(dataset)
        temp_f.seek(0) # go to the top of the file
        # write Export model
        obj = Export.objects.create(type=type)
        obj.file.save(fname, File(temp_f))


def generate_rating_dataset(app_label='playlists', model='MovieProxy', to_csv=True):
    #ctype = ContentType.objects.get(app_label=app_label, model=model)
    #ctype = ContentType.objects.get_for_model(model, for_concrete_model=False)
    ctype = ContentType.objects.get_for_model('MovieProxy', for_concrete_model=False)
    # print(ctype)
    qs = Rating.objects.filter(active=True, content_type=ctype)
    qs = qs.annotate(userId=F('user_id'), movieId=F("object_id"), rating=F("value"))
    dataset = qs.values('userId', 'movieId', 'rating')
    if to_csv:
        export_dataset(dataset=dataset, fname='rating.csv', type=ExportDataType.RATINGS)
    return dataset

def generate_movies_dataset(to_csv=True):
    qs = MovieProxy.objects.all()
    qs = qs.annotate(movieId=F('id'), movieIdx=F("idx"))
    dataset = qs.values('movieIdx', 'movieId', 'title', 'release_date', 'rating_count', 'rating_avg')
    if to_csv:
        export_dataset(dataset=dataset, fname='movies.csv', type=ExportDataType.MOVIES)
    return dataset