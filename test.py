from datamanager.sqlite_data_manager import SQLiteDataManager
from models import User, Movie

if __name__ == '__main__':
    """Main entry point for testing the SQLiteDataManager functionality."""

    dm = SQLiteDataManager('db/movies.db')

    # Add a new user
    user_id = dm.add_user(User(name='Alice'))

    # Add a movie for the user
    movie_id = dm.add_movie(
        Movie(name='Inception', director='Christopher Nolan', year=2010,
              rating=8.8), user_id)

    # Get all users
    users = dm.get_all_users()
    print(users)

    # Get movies for a specific user
    movies = dm.get_user_movies(user_id)
    print(movies)

    # Update a movie
    dm.update_movie(
        Movie(id=movie_id, name='Inception', director='Christopher Nolan',
              year=2010, rating=9.0))

    # Delete a movie
    dm.delete_movie(movie_id)

    # Check if the movie is deleted
    movies = dm.get_user_movies(user_id)
    print(movies)
