from flask import Blueprint, render_template, request, redirect, url_for
from datamanager.sqlite_data_manager import SQLiteDataManager
from models import Review

reviews_bp = Blueprint('reviews_bp', __name__,
                       template_folder='templates')

data_manager = SQLiteDataManager('db/moviwebapp.db')


@reviews_bp.route('/movies/<int:movie_id>/reviews',
                  methods=['GET', 'POST'])
def movie_reviews(movie_id):
    movie = data_manager.get_movie(movie_id)
    reviews = data_manager.get_movie_reviews(movie_id)
    if request.method == 'POST':
        review_text = request.form['review_text']
        rating = request.form['rating']
        review = Review(
            user_id=request.form['user_id'],
            movie_id=movie_id,
            review_text=review_text,
            rating=rating
        )
        data_manager.add_review(review)
        return redirect(url_for('reviews_bp.movie_reviews',
                                movie_id=movie_id))
    return render_template('movie_reviews.html',
                           movie=movie, reviews=reviews)


@reviews_bp.route('/reviews/<int:review_id>/edit', methods=['GET', 'POST'])
def edit_review(review_id):
    review = data_manager.get_review(review_id)
    if request.method == 'POST':
        review.review_text = request.form['review_text']
        review.rating = request.form['rating']
        data_manager.update_review(review)
        return redirect(
            url_for('reviews_bp.movie_reviews',
                    movie_id=review.movie_id))
    return render_template('edit_review.html', review=review)


@reviews_bp.route('/reviews/<int:review_id>/delete', methods=['POST'])
def delete_review(review_id):
    review = data_manager.get_review(review_id)
    data_manager.delete_review(review_id)
    return redirect(
        url_for('reviews_bp.movie_reviews', movie_id=review.movie_id))
