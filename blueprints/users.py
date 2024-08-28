from flask import Blueprint, render_template, request, redirect, url_for
from datamanager.sqlite_data_manager import SQLiteDataManager
from models import User, Movie, Director
from static.utils import _fetch_movie_data


users_bp = Blueprint('users_bp', __name__, template_folder='templates')

data_manager = SQLiteDataManager('db/moviwebapp.db')


@users_bp.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@users_bp.route('/users/<int:user_id>')
def user_movies(user_id):
    user = data_manager.get_user(user_id)
    movies = data_manager.get_user_movies(user_id)
    return render_template('user_movies.html', user=user,
                           movies=movies)


@users_bp.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        data_manager.add_user(User(name=name, lastname=lastname))
        return redirect(url_for('users_bp.list_users'))
    return render_template('add_user.html')


@users_bp.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    user = data_manager.get_user(user_id)

    if not user:
        return f"User with ID {user_id} not found", 404

    if request.method == 'POST':
        title = request.form['title']
        movie_data = _fetch_movie_data(title)

        if movie_data:
            director_name = movie_data.get('Director')
            if not director_name:
                return "Director not found", 404

            director = data_manager.get_director_by_name(director_name)
            if not director:
                director = Director(name=director_name)
                data_manager.add_director(director)

            movie = Movie(
                name=movie_data.get('Title'),
                director_id=director.id,
                year=movie_data.get('Year'),
                rating=float(movie_data.get('imdbRating')),
                poster=movie_data.get('Poster'),
                user_id=user_id
            )

            print(movie)  # Debug output
            movie_id = data_manager.add_movie(user_id, movie)
            if movie_id:
                return redirect(url_for('users_bp.user_movies', user_id=user_id))
            else:
                return "Failed to add movie", 500
        else:
            return "Movie not found", 404

    return render_template('add_movie.html', user=user)


@users_bp.route('/users/<int:user_id>/delete_movie/<int:movie_id>',
                methods=['POST'])
def delete_movie(user_id, movie_id):
    data_manager.delete_movie(movie_id)
    return redirect(url_for('users_bp.user_movies', user_id=user_id))
