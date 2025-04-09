# **🎬 Movie & TV Show Recommender Platform**

A full-stack, web-based platform for discovering, rating, and reviewing movies, TV shows, and playlists. Built with **collaborative filtering** to deliver personalized recommendations based on user ratings.

---

## **🚀 Features**

### **👤 User Experience**
- **Rate and Review**: Share your opinions on movies, shows, and playlists.
- **Watchlist**: Keep track of what you want to watch.
- **User Profiles**: View your activity on your own profile or compare it with others by visiting their profiles.

### **🎯 Smart Recommendations**
- **Collaborative Filtering**: Uses the Surprise library to power personalized suggestions.
- **Dynamic Updates**: For every 5 new ratings provided by a user, fresh new recommendations are generated.
- **Scheduled Predictions**: Background tasks provide recommendations for new or active users.

### **🔍 Discover Content**
- **Search & Filte**: Explore movies, series, playlists, and community reviews.
- **Compare Ratings**: Visualize rating comparisons with other users.

### **🔄 Daily Tasks**
- Recalculate average ratings for all content.
- Train the recommendation model.
- Predict and update suggestions
- Other.

---

## **🧰 Tech Stack**

### **🔧 Backend**
- **Django** + **Django REST Framework**
- **Celery** + **Redis** for async/scheduled tasks
- **Postgres** for relational data

### **💻 Frontend**
- **React** SPA for a smooth user interface

### **🤖 Machine Learning**
- **Surprise Library** (SVD collaborative filtering)
- **Jupyter Notebooks** for prototyping


### **📦 Containerization**
- **Docker** + **Docker Compose** for easy setup

---

## **⚙️ Installation**

### 1. Prerequisites
- **Docker** & **Docker Compose**


### 2. Clone the Repo
```bash
   git clone https://github.com/paul-fane/movie-recommender.git
   cd movie-recommender
```
   
### 3. Docker Setup:  
```bash
   docker compose build
```

### 4. Apply Migrations & Create Admin 
```bash
   docker compose run --rm django python manage.py makemigrations
   docker compose run --rm django python manage.py migrate
   docker compose run --rm django python manage.py createsuperuser
```

### 5. Run Containers 
```bash
   docker compose up
```

**📂 To experience and test the platform with real-world data, you can take the following stepts to load a dataset containing:**
- 🎬 ~45,000 movies
- 👥 ~1,000 users
- ⭐ ~100,000 user ratings

This will make the recommendation system more realistic and interactive.


### 6. Download the Movies Dataset: 
   - Visit https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset
   - Login or SignUp
   - Download the movies dataset
   - Expand archive.zip (the downloaded file)
   - Copy contents into ```./data``` folder so that you have:

```bash
   # in .(root project)/data 
    credits.csv             links.csv               movies_metadata.csv     ratings_small.csv
    keywords.csv            links_small.csv         ratings.csv
```
- We only need ```links_small.csv```, ```ratings_small.csv```, and ```movies_metadata.csv```

### 7. Load Data Into the System
```bash
   # Open a new terminal

   # Load movies (45,000+ entries)
   docker compose exec django python manage.py loader 100_000 --movies

   # Generate fake users
   docker compose exec django python manage.py loader --users 1000

   # Load ratings
   docker compose exec django python manage.py dataset_ratings

   # Fix incorrect movie IDs and associate ratings
   # This command cand take a few minutes (~2-3)
   docker compose exec django python manage.py update_movie_ids_and_ratings
```


### 8. Train the Recommendation Model
   - This command will generate a file inside ```.(root-project)/media/exports/surprise/yyyy-mm-dd/filename.pkl```
```bash
   docker compose exec django python manage.py train --epochs 20
```

### 9. Access the application
   - Frontend: http://localhost:3000
   - Backend-api: http://localhost:8000
   - Admin: http://localhost:8000/admin

### 10. Rate some movies:
   -  Each 5 rating, a task will be triggered and will generate new suggestions only for you.


### 11. Generate Recommendations
```bash
   # Generate 10 suggestions for all new and active users
   docker compose exec django python manage.py recommend --max_pages 10
   
   or 

   # For specific user IDs
   docker compose exec django python manage.py recommend --max_pages 10 --users [1,5,23]
```

### 12. Update Average Ratings
   - A task will also update it every 30 minutes
```bash
   docker compose exec django python manage.py calculate_ratings
```

### 13. (Optional) Add Movie Metadata
   - **Add Categories to each movie**
```bash
   # Open the shell
   docker compose exec django python manage.py shell

   # In Django shell
   from movie_recommendation_engine.utils.utils import add_category_to_movie
   add_category_to_movie() # (takes ~10-15 minutes)

   # Exit the shell
   exit()
```
   - **Add Video (YouTube Trailer IDs) to movie**
      - Download [MovieLens 20M YouTube Trailers Dataset](https://grouplens.org/datasets/movielens/20m-youtube/)
      - Add it to ```.(root)/data/ml-youtube.csv```.
      - Some trailer for some movie is not available.

```bash
   # Open the shell
   docker compose exec django python manage.py shell

   # In Django shell
   from movie_recommendation_engine.utils.utils import add_video_to_movie
   add_video_to_movie() # (takes ~10 minutes)

   # Exit the shell
   exit()
```




## **🧠 Machine Learning Workflow**
A complete machine-learning pipeline for training and managing a recommendation model using the Surprise library. 
The process involves preparing a dataset, training a collaborative filtering model, evaluating its accuracy, and exporting it for later use. 

1. **Prepare Dataset**: Export ratings with ```export_ratings_dataset()```
2. **Data Loader**: Convert to Surprise format ```using get_data_loader()```
3. **Train Model**: Fit an SVD model via ```train_surprise_model()```
4. **Evaluate Performance**: Metrics like RMSE and MAE validate the model's accuracy.
5. **Export**: Serialize and save the model using ```export_model()```
6. **Load**: Load the most recent model with ```load_model()``` when needed.



## **🔌 API Endpoints**

### **🔐 Auth**
| Method | Endpoint             | Description                     |
|--------|----------------------|---------------------------------|
| POST   | `/api/auth/token/`          | Obtain token             |
| POST   | `/api/auth/token/refresh/`  | Refresh token            |

### **👤 User**
| Method | Endpoint            | Description                     |
|--------|----------------------|---------------------------------|
| GET    | `/api/users/`                        | User List                   |
| POST   | `/api/users/create/`                 | User Create                 |
| GET    | `/api/users/<int:user_id>/`          | User Detail                 | 
| POST   | `/api/users/<int:user_id>/update/`   | User Update                 |
| GET    | `/api/users/me/`                     | User Me                     |

### **📺 Content**
| Method | Endpoint                        | Description                          |
|--------|---------------------------------|--------------------------------------|
| GET    | `/api/dashboard/list/`                        | Browse playlists            |
| GET    | `/api/playlists/movie-detail/<str:slug>/`     | Movie-detail                |
| GET    | `/api/playlists/playlist-detail/<str:slug>/`  | Playlist-detail             |
| GET    | `/api/playlists/tvshow-detail/<str:slug>/`    | TVShow-detail               |
| GET    | `/api/playlists/season-detail/<str:slug>/`    | Season-detail               |


### **⭐ Ratings**
| Method | Endpoint                        | Description                          |
|--------|---------------------------------|--------------------------------------|
| POST   | `/api/ratings/create/`                           | Create                 |
| GET    | `/api/ratings/user-list/<str:user_username>/`    | Ratings List (User)    |
| GET    | `/api/ratings/list/<int:playlist_id>/`           | Ratings List (Playlist)|
| GET    | `/api/ratings/compar-list/<str:user_username>/`  | Ratings Compare        |

### **🤖 Recommendations**
| Method | Endpoint                        | Description                          |
|--------|---------------------------------|--------------------------------------|
| GET    | `/api/suggestions/list/`        | Suggestions List                     |

### **📌 Watchlists**
| Method | Endpoint                        | Description                          |
|--------|---------------------------------|--------------------------------------|
| GET    | `/api/watchlists/list/`           | Watchlists List                    |
| POST   | `/api/watchlists/create/`         | Watchlists Create                  |
| DELETE | `/api/watchlists/delete/<int:pk>/`| Watchlists Delete                  |

### **👥 Profiles**
| Method | Endpoint                        | Description                          |
|--------|---------------------------------|--------------------------------------|
| GET    | `/api/profile/<str:user_username>/`| User profile                      |


## **📂 Project Structure**
```
movie_recommendation_engine/     # The root
├── config/                      # Settings
├── data/                        # Download required!
│   ├── links_small.csv 
│   ├── movies_metadata.csv
│   └── ratings_small.csv
├── docker/
├── frontend/                    # React app 
├── media/                       # Generated when export files
│   └── exports/
├── movie_recommendation_engine/ # Django apps
├── nbs/                         # Jupyter notebooks
├── postgres_data/
├── requirements/
├── .env
├── .gitignore
├── .pre-commit-config.yaml
├── docker-compose.yml           # Container setup 
├── manage.py
├── mypy.ini
├── README.md
└── requirements.txt  
```

## **💬 Final Notes**
- **🧱 Scalable Architecture**: The system follows the **Django Styleguide by HackSoft**, ensuring clean, maintainable, and scalable backend code.


## **📜 License**
- MIT License.