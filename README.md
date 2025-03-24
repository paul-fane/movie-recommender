# **Movie & TV Show Recommender Platform**

A web-based platform for rating and reviewing movies, TV shows, and playlists. This project leverages **collaborative filtering** to generate personalized recommendations for users based on their ratings.

---

## **Features**

### **User Interaction**
- **Rate and Review**: Leave ratings and reviews for movies, TV shows, and playlists.
- **Watchlist**: Add items to a personal watchlist for future viewing.
- **Custom Playlists**: Create and manage playlists of movies and series.
- **User Profiles**: View and compare your ratings with those of other users.

### **Recommendations**
- **Collaborative Filtering**: A recommendation engine generates new suggestions for users based on their ratings.
- **Dynamic Updates**: For every 5 new ratings provided by a user, fresh recommendations are generated.
- **Automated Suggestions**: Scheduled tasks provide recommendations for new and active users.

### **Content Discovery**
- **Browse Content**: Search and filter reviews, movies, series, and playlists.
- **Compare Ratings**: Visualize rating comparisons with other users.

### **Daily Tasks**
- Update average ratings for all content.
- Train the **Surprise** recommendation model.
- Predict new suggestions using the trained model.
- Other.

---

## **Tech Stack**

### **Backend**
- **Django**: Backend framework for logic and data management.
- **Django REST Framework (DRF)**: API development.
- **Celery**: Background and scheduled task management.
- **Redis**: Message broker for Celery tasks.

### **Frontend**
- **React**: Interactive single-page application (SPA).

### **Machine Learning**
- **Jupyter Notebooks**: Model prototyping and training.
- **Surprise Library**: Collaborative filtering recommendation engine.

### **Containerization**
- **Docker**: Isolated and containerized environment setup.

---

## **Installation**

### **Prerequisites**
1. **Docker** and **Docker Compose**, the easiest way to run all containers.
2. (Another option) Install **Python**, **Node.js** and dependencies for local setup.

### **Setup**


1. Clone the repository:
```bash
   git clone https://github.com/paul-fane/movie-recommender.git
   cd movie-recommender
```
   
#### **Using Docker:**
2. Build and start the containers:  
```bash
   docker-compose up --build
```

3. Access the application:
    - Frontend: http://localhost:3000
    - Backend: http://localhost:8000

#### **Local setup:** 
Limited features due to the need to run redis and celery! Much easier with Docker.
Steps to follow to run the Django backend and React frontend:

2. Create virtual environment and activate it.:
```bash
    cd path/to/movie-recommender/backend
    python -m venv venv
    source venv/bin/activate
```
Use .\venv\Scripts\activate if on windows

3. Install requirements:  
```bash
    (venv) python -m pip install pip --upgrade
    (venv) python -m pip install -r requirements/requirements.txt
    (venv) python -m pip install -r requirements/requirements.ml.txt
```

3. There is no need to run migrations and migrate data because the database is 
included in the github file to allow other users to test the application. 
In the database there are tens of thousands of movies and many reviews that have
 been randomly generated. Create superuser to be able to see the admin section:  
```bash
    (venv) python manage.py createsuperuser
```

4. Run the backend server: 
```bash
   (venv) python manage.py runserver
```

5. In order to run the React frontend, open a new terminal.
```bash
    cd path/to/movie-recommender/frontend
```

6. Install the frontend packages: 
```bash
   npm i
```

6. Run the frontend: 
```bash
   npm run dev
```

7. Access the application:
    - Frontend: http://localhost:3000
    - Backend: http://localhost:8000

[The Movies Dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset) and 
[MovieLens 20M YouTube Trailers Dataset](https://grouplens.org/datasets/movielens/20m-youtube/) were used for this project.

## **Usage**

### **Frontend**

    - Accessible via the React-based user interface.
    - Perform actions like rating, reviewing, managing watchlists, searching, filtering and exploring recommendations.

### **Backend**
    - Provides RESTful API endpoints.

### **Scheduled Tasks**
    - Celery automates tasks like updating ratings, training the model, generating suggestions, other.



## **Machine Learning Workflow**
A complete machine-learning pipeline for training and managing a recommendation model using the Surprise library. 
The process involves preparing a dataset, training a collaborative filtering model, evaluating its accuracy, and exporting it for later use. 

### **Exporting Data**
 - export_ratings_dataset() retrieves and formats the dataset.
### **Prepare Dataset:**  
 - get_data_loader() converts the dataset into a Surprise-compatible format.
### **Train the Model:**
 - train_surprise_model() initializes the SVD model.
### **Evaluate Performance:**
 - Metrics like RMSE and MAE validate the model's accuracy.
### **Save Model:**
 - export_model() The trained model is serialized and saved in ml/models/ for future use.
### **Load Model:**
 - load_model() loads the latest saved model when needed.


## **API Endpoints**

### **User Authentication**
| Method | Endpoint            | Description                     |
|--------|----------------------|---------------------------------|
| POST   | `/api/token/`          | Obtain token.                 |
| POST   | `/api/token/refresh/`  | Refresh token.                |
| POST   | `/api/register/`       | Register a new user.          | 

### **Playlists and  Dashnoard**
| Method | Endpoint                        | Description                          |
|--------|---------------------------------|--------------------------------------|
| GET    | `/api/dashnoard/list/`          | List(search and filter) all playlists. |
| GET    | `/api/playlists/movie-detail/<str:slug>/`  | Movie-detail                |
| GET    | `/api/playlists/playlist-detail/<str:slug>/`| Playlist-detail            |
| GET    | `/api/playlists/tvshow-detail/<str:slug>/` | TVShow-detail               |
| GET    | `/api/playlists/season-detail/<str:slug>/` | Season-detail               |


### **Ratings and Comparisons**
| Method | Endpoint                        | Description                          |
|--------|---------------------------------|--------------------------------------|
| POST   | `/api/ratings/create/`                | Submit a rating for an item.        |
| GET    | `/api/ratings/user-list/<str:user_username>/`| Get all ratings by a specific user. |
| GET    | `/api/ratings/list/<int:playlist_id>/` | List all ratings by a specific playlist. |
| GET    | `/api/ratings/compar-list/<str:user_username>/`| Compare ratings with another user.|

### **Recommendations**
| Method | Endpoint                        | Description                          |
|--------|---------------------------------|--------------------------------------|
| GET    | `/api/suggestions/list/`        | Retrieve suggestions.                |

### **Watchlists**
| Method | Endpoint                        | Description                          |
|--------|---------------------------------|--------------------------------------|
| GET    | `/api/watchlists/list/`           | List all watchlists.               |
| POST   | `/api/watchlists/create/`         | Add playlist to watchlist.         |
| DELETE | `/api/watchlists/delete/<int:pk>/`| Remove a playlist from watchlist.  |

### **Profiles**
| Method | Endpoint                        | Description                          |
|--------|---------------------------------|--------------------------------------|
| GET    | `/api/profile/<str:user_username>/`| Retrieve a user's profile.       |
