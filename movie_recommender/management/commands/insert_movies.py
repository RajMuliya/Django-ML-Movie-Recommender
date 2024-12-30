from django.core.management.base import BaseCommand
import pandas as pd
from movie_recommender.models import movie_list

class Command(BaseCommand):
    help = 'Load movies from a .pkl file and insert into the database'

    def handle(self, *args, **options):
        # Load movie names from a .pkl file (replace with your actual file path)
        movies_df = pd.read_pickle('E:/ML Project/Recommend_django/movie_recommendation_system/movie_recommender/my_models/movie_list.pkl')  # Adjust the path as necessary
        
        # Assuming the column name in your DataFrame is 'movie_name'
        movies_to_insert = movies_df['movie_name'].values  # Get the 'movie_name' column as a NumPy array

        # Insert each movie into the database
        for movie_name in movies_to_insert:
            movie_list.objects.get_or_create(movies=movie_name)  # Use 'movies' here instead of 'name'

        self.stdout.write(self.style.SUCCESS('Successfully inserted movies into the database.'))
