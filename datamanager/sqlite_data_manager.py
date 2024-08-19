from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Movie, Base
from datamanager.data_manager_interface import DataManagerInterface


class SQLiteDataManager(DataManagerInterface):
    """
    SQLiteDataManager is an implementation of DataManagerInterface
    that uses SQLAlchemy to manage CRUD operations with a SQLite database.
    """

    def __init__(self, db_file_name):
        """
        Initialize the SQLiteDataManager with the specified
        SQLite database file.

        :param db_file_name: Name of the SQLite database file.
        """
        engine = create_engine(f'sqlite:///{db_file_name}')
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)

    def get_all_users(self):
        """
        Retrieve all users from the database.

        :return: A list of User objects.
        """
        session = self.Session()
        users = session.query(User).all()
        session.close()
        return users

    def get_user_movies(self, user_id):
        """
        Retrieve all movies associated with a specific user.

        :param user_id: ID of the user whose movies are to be retrieved.
        :return: A list of Movie objects.
        """
        session = self.Session()
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            movies = user.movies
        else:
            movies = []
        session.close()
        return movies

    def add_user(self, user):
        """
        Add a new user to the database.

        :param user: User object to be added.
        :return: The ID of the newly created user.
        """
        session = self.Session()
        new_user = User(name=user.name)
        session.add(new_user)
        session.commit()
        new_user_id = new_user.id
        session.close()
        return new_user_id

    def add_movie(self, movie, user_id):
        """
        Add a new movie to a specific user's movie list.

        :param movie: Movie object to be added.
        :param user_id: ID of the user to whom the movie is to be added.
        :return: The ID of the newly created movie.
        """
        session = self.Session()
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            new_movie = Movie(
                name=movie.name,
                director=movie.director,
                year=movie.year,
                rating=movie.rating,
                user_id=user_id
            )
            session.add(new_movie)
            session.commit()
            movie_id = new_movie.id
        else:
            movie_id = None
        session.close()
        return movie_id

    def update_movie(self, movie):
        """
        Update the details of a specific movie in the database.

        :param movie: Movie object containing updated details.
        """
        session = self.Session()
        existing_movie = session.query(Movie).filter_by(id=movie.id).first()
        if existing_movie:
            existing_movie.name = movie.name
            existing_movie.director = movie.director
            existing_movie.year = movie.year
            existing_movie.rating = movie.rating
            session.commit()
        session.close()

    def delete_movie(self, movie_id):
        """
        Delete a specific movie from the database.

        :param movie_id: ID of the movie to be deleted.
        """
        session = self.Session()
        movie = session.query(Movie).filter_by(id=movie_id).first()
        if movie:
            session.delete(movie)
            session.commit()
        session.close()
