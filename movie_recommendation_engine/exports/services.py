import csv
import tempfile
import pickle
from django.core.files.base import File

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
        # File(temp_f) wraps the temporary file so Django's storage system can handle it.
        obj.file.save(fname, File(temp_f))

        
        
def export_model(model, model_name='model', model_type=ExportDataType.SURPRISE, model_ext='pkl'):
    '''Saves the trained model using the Export model.'''
    
    # Stores the model in a temporary file.
    # pickle library to serialize the model into a binary file.
    with tempfile.NamedTemporaryFile(mode='rb+') as temp_f:
        pickle.dump({"model": model}, temp_f)
        temp_f.seek(0)  # Reset file pointer before reading it again

        # Create an Export instance before saving the file
        export_instance = Export.objects.create(type=model_type)
        
        # Save the file using Export's file field
        export_instance.file.save(f"{model_name}.{model_ext}", File(temp_f))