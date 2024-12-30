# Movie Recommendation System

A Django-based web application that uses Machine Learning to provide personalized movie recommendations. This project is designed to deliver relevant movie suggestions based on user preferences, search history, and movie similarity matrices.

---

## Features

- **Movie Recommendation**: Suggest movies using a content-based recommendation algorithm.
- **Search History Integration**: Refine recommendations based on user search history.
- **TMDb API Integration**: Fetch movie details, posters, and release years.
- **Detailed Movie Information**: Display comprehensive details about a recommended movie.
- **Dynamic Loading**: Show 20 movies initially and load more with a 'Load More' button.
- **Filtered Recommendations**: Recommend movies at least 10 years old relative to the searched movie.

---

## Technologies Used

- **Backend**: Django, Python
- **Frontend**: HTML, CSS, JavaScript (Bootstrap for UI)
- **Database**: SQLite (default, configurable to other databases)
- **API**: TMDb API for movie data and poster fetching
- **Machine Learning**: Content-based filtering algorithm

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/your-repository-name.git
   cd your-repository-name
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the server:**
   ```bash
   python manage.py runserver
   ```

6. **Access the application:**
   Open your browser and navigate to `http://127.0.0.1:8000/`.

---

## Usage

1. **Search for Movies:** Enter a movie name to get personalized recommendations.
2. **Explore Details:** Click on any recommended movie to view its details, including the poster and release year.
3. **Load More:** Use the 'Load More' button to explore additional recommendations.

---

## Project Structure

- **movie_recommender/**: Main project folder.
- **templates/**: HTML templates for the web application.
- **static/**: CSS, JavaScript, and other static files.
- **recommendation/**: Django app for handling movie recommendation logic.
- **requirements.txt**: List of dependencies.

---

## API Key Setup

1. Obtain an API key from [TMDb](https://www.themoviedb.org/documentation/api).
2. Add the API key to your environment variables or directly in the settings file (not recommended for production).

---

## Future Enhancements

- Add user authentication for personalized recommendations.
- Implement collaborative filtering for better suggestions.
- Support multilingual movie recommendations.
- Improve UI/UX for seamless user interaction.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Contributions

Contributions are welcome! Feel free to open issues or submit pull requests to improve this project.

---

## Acknowledgments

- **TMDb API**: For providing movie data.
- Django documentation and community for guidance.

---

## Contact

For questions or suggestions, please email: [raj.muliya0@gmail.com](mailto:raj.muliya0@gmail.com)

