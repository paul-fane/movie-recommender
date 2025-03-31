import pickle
from movie_recommendation_engine.exports.models import Export, ExportDataType

def load_model(model_type=ExportDataType.SURPRISE):
    '''Loads the latest exported model for predictions from the Export model.'''
    
    # Retrieve the latest Export object for the given model type
    try:
        export_instance = Export.objects.filter(type=model_type, latest=True)
    except Export.DoesNotExist:
        raise ValueError(f"No model found for type '{model_type}'.")

    # Open the file from Django storage
    model = None
    if export_instance.file:
        with export_instance.file.open('rb') as f:
            model_data = pickle.load(f)  # Load the model from the file
            model = model_data.get('model')

    if not model:
        raise ValueError("Failed to load the model.")

    return model  # Return the deserialized model object