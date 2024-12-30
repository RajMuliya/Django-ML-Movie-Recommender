# # context_processors.py
# from .models import movie_list
# import pickle
# import os
# import pandas as pd

# # from .models import SearchHistory


# def movie_func(request):
#     base_dir = os.path.dirname(__file__)
#     movie_list_path = os.path.join(base_dir, 'my_models', 'movie_list.pkl')

#     with open(movie_list_path, 'rb') as f:
#         movies = pickle.load(f)

#     # Check if the database is empty before inserting
#     if not movie_list.objects.exists():  # Check if any movies exist in the DB
#         # Load movie names from a .pkl file (replace with your actual file path)
#         movies_df = pd.read_pickle(movies)  # Adjust the path as necessary
        
#         # Assuming the column name in your DataFrame is 'movie_name'
#         movies_to_insert = movies_df['movie_name'].values  # Get the 'movie_name' column as a NumPy array

#         # Insert each movie into the database
#         for movie_name in movies_to_insert:
#             movie_list.objects.get_or_create(name=movie_name)  # Insert movie if it doesn't already exist

#     list = movie_list.objects.all()
#     return {'list': list}

from .models import movie_list
import pickle
import os
import pandas as pd

def movie_func(request):
    base_dir = os.path.dirname(__file__)
    movie_list_path = os.path.join(base_dir, 'my_models', 'movie_list.pkl')

    # Load only the `movie_name` column from the .pkl file
    with open(movie_list_path, 'rb') as f:
        movies_df = pickle.load(f)  # Assume movies_df is a DataFrame

    # Check if the database is empty before inserting
    if not movie_list.objects.exists():
        # Extract only the `movie_name` column
        movies_to_insert = movies_df['movie_name'].values  # Get 'movie_name' as an array

        # Insert each movie into the database
        for movie_name in movies_to_insert:
            movie_list.objects.get_or_create(movies=movie_name)  # Insert movie if it doesn't already exist

    list = movie_list.objects.all()
    return {'list': list}


