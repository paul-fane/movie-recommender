from django.core.management.base import BaseCommand

from movie_recommendation_engine.ratings.models import Rating
from movie_recommendation_engine.ratings.tasks import generate_fake_reviews

# py manage.py fake_ratings 100 --users 500 --show-total

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("count", nargs='?', default=10, type=int)
        parser.add_argument("--users", default=1000, type=int)
        parser.add_argument("--show-total", action='store_true', default=False)
    
    def handle(self, *args, **options):
        count = options.get('count')
        show_total = options.get('show_total')
        user_count = options.get('users')
        # print(count, show_total, user_count)
        new_ratings = generate_fake_reviews(count=count, users=user_count)
        print(f"New ratings: {len(new_ratings)}")
        if show_total:
            qs = Rating.objects.all()
            print(f"Total ratings: {qs.count()}")