import pickle
from movie_recommendation_engine.exports.models import Export, ExportDataType

def load_model(model_type=ExportDataType.SURPRISE):
    '''Loads the latest exported model for predictions from the Export model.'''
    
    # Retrieve the latest Export object for the given model type
    export_instance = Export.objects.filter(type=model_type, latest=True).first()

    if not export_instance or not export_instance.file:
        raise ValueError(f"No model file found for type '{model_type}'.")

    # Open and load the pickled model
    with export_instance.file.open('rb') as f:
        model_data = pickle.load(f)  # Load the model from the file
        model = model_data.get('model')

    if not model:
        raise ValueError("Failed to load the model.")

    return model  # Return the deserialized model object