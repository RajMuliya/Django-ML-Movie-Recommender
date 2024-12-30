import os
import pickle
import pandas as pd
import requests
from django.shortcuts import render
import random
import requests
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User  # Import the User model
from .forms import CustomLoginForm, RegistrationForm

def auth_view(request):
    login_form = CustomLoginForm()
    signup_form = RegistrationForm()

    if request.method == 'POST':
        if 'login' in request.POST:
            # Handle login form submission
            login_form = CustomLoginForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                messages.success(request, "Logged in successfully!")
                return redirect('home')  # Replace 'home' with your actual homepage URL name
            else:
                messages.error(request, "Login failed. Please check your credentials and try again.")

        elif 'signup' in request.POST:
            # Handle signup form submission
            signup_form = RegistrationForm(request.POST)
            if signup_form.is_valid():
                # Extract cleaned data
                username = signup_form.cleaned_data.get('username')
                email = signup_form.cleaned_data.get('email')
                password = signup_form.cleaned_data.get('password1')
                
                # Create new user
                user = User.objects.create_user(username=username, email=email, password=password)
                messages.success(request, "Your account has been created successfully! You can now log in.")
                return redirect('login')  # Replace 'login' with the name of your login page
            else:
                messages.error(request, "Signup failed. Please correct the errors and try again.")

    # Render the template with both forms
    return render(request, 'registration/login.html', {
        'login_form': login_form,
        'signup_form': signup_form,
    })






# Function to fetch movie image (poster) from IMDb
def fetch_poster(imdb_id):
    api_key = '2bb8c29b'  # Replace with your OMDb API key
    url = f'http://www.omdbapi.com/?i={imdb_id}&apikey={api_key}'
    
    response = requests.get(url)
    data = response.json()
        
    # Check if the response contains a valid poster
    if 'Poster' in data and data['Poster'] != 'N/A':
        return data['Poster']  # Return the poster URL
    else:
        return 'static/placeholder1.jpg'
    
    



# Function to load multiple models
def load_data():
    # Define the paths to your .pkl files
    base_dir = os.path.dirname(__file__)
    movie_list_path = os.path.join(base_dir, 'my_models', 'movie_list.pkl')
    similarity_path = os.path.join(base_dir, 'my_models', 'similarity.pkl')

    # Load the movie list and similarity matrix
    with open(movie_list_path, 'rb') as f:
        movies = pickle.load(f)

    with open(similarity_path, 'rb') as f:
        similarity = pickle.load(f)

    return movies, similarity

movies, similarity = load_data()


# Function to recommend movies
def recommend(movie, movies, similarity):
    index = movies[movies['movie_name'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movie_ids = []  # added
    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[0:11]:  # Get the top 5 recommendations
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_ids.append(movie_id)  #added
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].movie_name)

    return recommended_movie_ids, recommended_movie_names, recommended_movie_posters #added


# View for the movie recommendation system
@login_required(login_url='login')
def index(request):
    # Initialize search history in the session
    if 'search_history' not in request.session:
        request.session['search_history'] = []

    search_history = request.session['search_history']
    recommended_movies = []

    # If search history exists, recommend movies based on history
    if search_history:
        for movie in search_history:
            recommended_movie_ids,recommended_movie_names, recommended_movie_posters = recommend(movie, movies, similarity)
            recommendations = zip(recommended_movie_ids,recommended_movie_names, recommended_movie_posters)

            # Append recommendations to the final list (ensure no duplicates)
            for movie_id,movie_name, poster_url in recommendations:
                if movie_id and movie_name not in [m['name'] for m in recommended_movies]:
                    recommended_movies.append({
                        'id': movie_id,
                        'name': movie_name,
                        'poster_url': poster_url if poster_url else 'static/placeholder1.jpg'
                    })
    
    # If no search history exists, show random movies as fallback
    # elif not recommended_movies:
    #     random_movies = movies[['movie_name', 'movie_id']].sample(22)  # Extract movie names and IMDb IDs
    #     # random_movies = movie_names.sample(20)  # Randomly sample 20 movies
        
    #     # Prepare a list of dictionaries containing movie name and poster URL
    #     for index, row in random_movies.iterrows():
    #         movie_name = row['movie_name']
    #         imdb_id = row['movie_id']
            
    #         # Fetch the poster URL using the provided function
    #         poster_url = fetch_poster(imdb_id)
            
    #         recommended_movies.append({
    #             'name': movie_name,
    #             'poster_url': poster_url if poster_url else 'static/placeholder1.jpg'
    #         })

    # Shuffle the final list of recommended movies (whether from history or fallback)
    random.shuffle(recommended_movies)
    
    # Pass the list of movies with posters to the template
    context = {
        'random_movies': recommended_movies
    }
    
    return render(request, 'index.html', context)

    
# @login_required  # Ensure that only logged-in users can access this view
def clear_session(request):
    request.session.flush()  # Clears the entire session
    return redirect('home')



def search_movies(request):
    movie_list = movies['movie_name'].values
    selected_movie = None
    recommended_movies = []


    # Initialize search history in the session
    if 'search_history' not in request.session:
        request.session['search_history'] = []

    # Handle form submission
    if request.method == 'POST':
        selected_movie = request.POST.get('selected_movie')  # Get selected movie from the form

        if selected_movie:
            # Store the searched movie in the session
            search_history = request.session['search_history']
            if selected_movie not in search_history:
                search_history.append(selected_movie)
            request.session['search_history'] = search_history  # Update session with search history
     
            recommended_movie_ids,recommended_movie_names, recommended_movie_posters = recommend(selected_movie, movies, similarity)
            recommended_movies = zip(recommended_movie_ids,recommended_movie_names, recommended_movie_posters)

    context = {
        'movie_list': movie_list,
        'selected_movie': selected_movie,
        'recommended_movies': recommended_movies
    }
    return render(request, "search_movie.html", context)


def movie_detail(request, movie_id):

    OMDB_API_KEY = 'e0e493db'
    
    # Make a request to the OMDb API
    url = f"http://www.omdbapi.com/?i={movie_id}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    movie_data = response.json()
    
    if movie_data.get('Response') == 'True':  # Check if movie is found
        movie_details = {
            'title': movie_data.get('Title'),
            'year': movie_data.get('Year'),
            'genre': movie_data.get('Genre'),
            'plot': movie_data.get('Plot'),
            'poster': movie_data.get('Poster'),
            'director': movie_data.get('Director'),
            'actors': movie_data.get('Actors'),
            'writers': movie_data.get('Writer'),
            'production': movie_data.get('Production'),
            'released': movie_data.get('Released'),
            'runtime': movie_data.get('Runtime'),
            'language': movie_data.get('Language'),
            'country': movie_data.get('Country'),
            'awards': movie_data.get('Awards'),
            'imdb_rating': movie_data.get('imdbRating'),
            'box_office': movie_data.get('BoxOffice'),
            'cast': movie_data.get('Actors'),
            'writers': movie_data.get('Writer')
        }
    else:
        # Handle cases where movie details are not found
        movie_details = {
            'id': movie_id,
            'error': 'Movie details not found.'
        }
    
    first_actor = ""
    second_actor = ""
    if movie_data.get('Response') == 'True' and 'Actors' in movie_data:
        actors = movie_data.get('Actors').split(',')
        first_actor=actors[0]
        second_actor = actors[1]

    
    context = {
        'movie_details': movie_details,
        'first_actor' : first_actor,
        'second_actor' : second_actor,
    }
    return render(request, 'movie_detail.html', context)
  

