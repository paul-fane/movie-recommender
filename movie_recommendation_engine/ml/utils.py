from surprise import accuracy, Reader, Dataset, SVD
from surprise.model_selection import cross_validate

from movie_recommendation_engine.ratings.selectors import ratings_dataset
from movie_recommendation_engine.exports.services import export_model

# A complete machine-learning pipeline for training and managing a recommendation model using the Surprise library. 
# The process involves preparing a dataset, training a collaborative filtering model, evaluating its accuracy, and exporting it for later use.


def get_data_loader(dataset, columns=['userId', 'movieId', 'rating']):
    '''Prepares the exported dataset into a format suitable for training with Surprise.'''
    
    # having the import inside the function can help in case of errors
    import pandas as pd
    
    # Uses Pandas to load the dataset into a DataFrame.
    # DataFrame: A two-dimensional labeled data structure with columns that can hold different types of data
    # dropna() removes rows containing NaN (missing ratings)
    # inplace=True modifies the DataFrame directly, rather than returning a copy with the changes
    df = pd.DataFrame(dataset)
    df['rating'].dropna(inplace=True)
    
    # Determines the rating scale (min_rating to max_rating).
    max_rating, min_rating = df.rating.max(), df.rating.min()
    # Adding rating scale
    reader = Reader(rating_scale=(min_rating, max_rating))
    
    # Converts the DataFrame into a Surprise-compatible Dataset object, using "Dataset from surprise"
    # Return the dataframe whit 'userId', 'movieId', 'rating' colums, ready for model training.
    return Dataset.load_from_df(df[columns], reader)


def get_model_acc(trainset, model, use_rmse=True):
    '''Evaluates the model's accuracy after training.'''
    
    # Uses the test set derived from the training set
    testset = trainset.build_testset()
    predictions = model.test(testset)
    
    # Computes prediction accuracy using either RMSE or MAE (default is RMSE).
    # RMSE should be low as we are biased
    if not use_rmse:
        return accuracy.mae(predictions, verbose=True)
    
    # Returns the accuracy value
    acc = accuracy.rmse(predictions, verbose=True)
    return acc 

def train_surprise_model(n_epochs=20, verbose=True):
    ''' 
    Trains an SVD (Singular Value Decomposition) model with the dataset and evaluates its performance.
    Setting surprise
    '''
    # 1. Data Preparation:
    dataset = ratings_dataset() # format-> [{'userId': 1, 'movieId': 10, 'rating': 4.5}, ...]
    loaded_data = get_data_loader(dataset)
    
    # 2.Model Definition:
    #   -Declaring the algoritm, Initializes the SVD model
    #   -n_epochs: This parameter controls how many times the algorithm should go over 
    #   the entire dataset to update the latent factors.
    model = SVD(n_epochs=n_epochs, verbose=verbose) 
    
    
    # 3.Cross-Validation:
    #   Cross validate will compare the algoritm whit the data across RMSE function and MAE function
    #   Use to improve the training process
    cv_results = cross_validate(model, loaded_data, measures=['RMSE', "MAE"], cv=4, verbose=True)
    
    # 4.Full Dataset Training:
    #   It converts the entire dataset (both training and testing portions) into a Trainset object, 
    #   which is a format that Surprise's algorithms can work with. This allows you to train a 
    #   recommendation algorithm on all available data.
    trainset = loaded_data.build_full_trainset()
    model.fit(trainset) # Trains the model
    
    # 5.Accuracy Measurement:
    # Grab the testset and some prediction from that testset
    acc = get_model_acc(trainset, model, use_rmse=True)
    
    acc_label = int(100* acc)
    model_name = f"model-{acc_label}" # model-0.63
    
    # 6.Exporting the Model
    export_model(model, model_name, model_type='surprise', model_ext='pkl')
    