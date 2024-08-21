from flask import Flask, render_template, request, redirect, url_for
from datamanager.sqlite_data_manager import SQLiteDataManager
from models import User, Movie  # Ensure this import works properly
import requests

# Initialize Flask app and SQLite data manager
app = Flask(__name__)
data_manager = SQLiteDataManager('db/moviwebapp.db')

OMDB_API_KEY = "853b022f"


def _fetch_movie_data(title):
    """
    Fetches movie data from OMDb API.

    Args:
        title (str): The title of the movie to fetch.

    Returns:
        dict: Movie data as returned by OMDb API.
              None if movie is not found or an error occurs.
    """
    try:
        response = requests.get(f"http://www.omdbapi.com/?apikey="
                                f"{OMDB_API_KEY}&t={title}")
        if response.status_code == 200:
            data = response.json()
            if data['Response'] == 'True':
                return data
            else:
                print(f"Error: {data['Error']}")
        else:
            print("Error: Could not retrieve data from OMDb API.")
    except requests.RequestException as e:
        print(f"Error: {e}")
    return None


@app.route('/')
def home():
    """
    Home page route.
    """
    return render_template("base.html")


@app.route('/users')
def list_users():
    """
    Route to display a list of all users.
    """
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>')
def user_movies(user_id):
    """
    Route to display a list of a specific user's favorite movies.
    """
    user = data_manager.get_user(user_id)
    movies = data_manager.get_user_movies(user_id)
    return render_template('user_movies.html',
                           user=user, movies=movies)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """
    Route to add a new user to the app.
    """
    if request.method == 'POST':
        name = request.form['name']
        data_manager.add_user(User(name=name))
        return redirect(url_for('list_users'))
    return render_template('add_user.html')


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    """
    Route to add a new movie to a user's favorite movies list.
    """
    user = data_manager.get_user(user_id)

    if request.method == 'POST':
        title = request.form['title']
        movie_data = _fetch_movie_data(title)
        if movie_data:
            movie = Movie(
                name=movie_data['Title'],
                director=movie_data['Director'],
                year=movie_data['Year'],
                rating=movie_data['imdbRating'],
                user_id=user_id
            )
            data_manager.add_movie(movie, user_id)
            return redirect(url_for('user_movies', user_id=user_id))
    return render_template('add_movie.html', user=user)


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>',
           methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    """
    Route to update details of a specific movie.
    """
    user = data_manager.get_user(user_id)
    movie = data_manager.get_movie(movie_id)

    if request.method == 'POST':
        movie.name = request.form['name']
        movie.director = request.form['director']
        movie.year = request.form['year']
        movie.rating = request.form['rating']
        data_manager.update_movie(movie)
        return redirect(url_for('user_movies', user_id=user_id))
    return render_template('update_movie.html',
                           user=user, movie=movie)


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>')
def delete_movie(user_id, movie_id):
    """
    Route to delete a specific movie from a user's list.
    """
    data_manager.delete_movie(movie_id)
    return redirect(url_for('user_movies', user_id=user_id))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
