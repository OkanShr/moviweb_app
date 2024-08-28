from flask import Blueprint, render_template, request, redirect, url_for
from datamanager.sqlite_data_manager import SQLiteDataManager

movies_bp = Blueprint('movies_bp', __name__, template_folder='templates')

data_manager = SQLiteDataManager('db/moviwebapp.db')


@movies_bp.route('/users/<int:user_id>/update_movie/<int:movie_id>',
                 methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    user = data_manager.get_user(user_id)
    movie = data_manager.get_movie(movie_id)
    if request.method == 'POST':
        movie.name = request.form['name']
        movie.director = request.form['director']
        movie.year = request.form['year']
        movie.rating = request.form['rating']
        data_manager.update_movie(movie)
        return redirect(url_for('users_bp.user_movies', user_id=user_id))
    return render_template('update_movie.html', user=user, movie=movie)
