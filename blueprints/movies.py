from flask import Blueprint, render_template, request, redirect, url_for
from datamanager.sqlite_data_manager import SQLiteDataManager
from models import Director

movies_bp = Blueprint('movies_bp', __name__, template_folder='templates')

data_manager = SQLiteDataManager('db/moviwebapp.db')


@movies_bp.route('/users/<int:user_id>/update_movie/<int:movie_id>',
                 methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    user = data_manager.get_user(user_id)
    if not user:
        return f"User with ID {user_id} not found", 404

    movie = data_manager.get_movie(movie_id)
    if not movie:
        return f"Movie with ID {movie_id} not found", 404

    if request.method == 'POST':
        title = request.form.get('title')
        director_name = request.form.get('director')
        year = request.form.get('year')
        rating = request.form.get('rating')
        poster = request.form.get('poster')
        plot = request.form.get('plot')

        # Fetch or create director
        if director_name:
            director = data_manager.get_director_by_name(director_name)
            if not director:
                director = Director(name=director_name)
                data_manager.add_director(director)
            movie.director_id = director.id

        # Update movie details
        movie.title = title
        movie.year = year or movie.year
        movie.rating = float(rating) if rating else movie.rating
        movie.poster = poster or movie.poster
        movie.plot = plot or movie.plot

        # Update movie in data manager
        if data_manager.update_movie(movie):
            return redirect(url_for('users_bp.user_movies', user_id=user_id))
        else:
            return "Failed to update movie", 500

    return render_template('update_movie.html', user=user, movie=movie)
