from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from models import User, Movie, Base, Review, Director
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

    def get_user(self, user_id):
        """
        Retrieve a single user by ID.

        :param user_id: ID of the user to retrieve.
        :return: User object or None if not found.
        """
        session = self.Session()
        user = session.query(User).filter_by(id=user_id).first()
        session.close()
        return user

    def get_user_movies(self, user_id):
        """
        Retrieve all movies associated with a specific user with eager
        loading for related Director objects.

        :param user_id: ID of the user whose movies are to be retrieved.
        :return: A list of Movie objects with their associated Director
        objects.
        """
        session = self.Session()
        try:
            user = session.query(User).filter_by(id=user_id).first()
            if user:
                # Eager load the related Director objects
                movies = session.query(Movie).options(
                    joinedload(Movie.director)).filter_by(
                    user_id=user_id).all()
            else:
                movies = []
        finally:
            session.close()
        return movies

    def add_user(self, user):
        """
        Add a new user to the database.

        :param user: User object to be added.
        :return: The ID of the newly created user.
        """
        session = self.Session()
        new_user = User(name=user.name, lastname=user.lastname)
        session.add(new_user)
        session.commit()
        new_user_id = new_user.id
        session.close()
        return new_user_id

    def add_movie(self, user_id, movie):
        session = self.Session()
        try:
            # Check if the user exists
            user = session.query(User).filter_by(id=user_id).first()
            if not user:
                raise ValueError("User not found")

            # Extract the director_id from the movie object
            director_id = movie.director_id

            if not director_id:
                raise ValueError("Director information is missing")

            # Create new movie
            new_movie = Movie(
                name=movie.name,
                director_id=director_id,
                year=movie.year,
                rating=movie.rating,
                user_id=user_id,
                poster=movie.poster
            )
            session.add(new_movie)
            session.commit()  # Commit to save the movie
            return new_movie.id
        except ValueError as ve:
            print(f"ValueError: {ve}")
            session.rollback()
            return None
        except Exception as e:
            print(f"Error adding movie: {e}")
            session.rollback()
            return None
        finally:
            session.close()

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

    def get_movie(self, movie_id):
        """
        Retrieve a single movie by ID.

        :param movie_id: ID of the movie to retrieve.
        :return: Movie object or None if not found.
        """
        session = self.Session()
        movie = session.query(Movie).filter_by(id=movie_id).first()
        session.close()
        return movie

    # --- Director CRUD Operations ---

    def add_director(self, director):
        """
        Add a new director to the database.
        :param director: Director object to be added.
        :return: The ID of the newly created director.
        """
        session = self.Session()
        session.add(director)
        session.commit()
        director_id = director.id
        session.close()
        return director_id

    def get_director(self, director_id):
        """
        Retrieve a director by their ID.
        :param director_id: ID of the director to retrieve.
        :return: Director object.
        """
        session = self.Session()
        director = session.query(Director).filter_by(id=director_id).first()
        session.close()
        return director

    def get_director_by_name(self, name):
        session = self.Session()
        try:
            director = session.query(Director).filter_by(name=name).first()
            return director
        finally:
            session.close()

    def get_all_directors(self):
        """
        Retrieve all directors from the database.
        :return: A list of Director objects.
        """
        session = self.Session()
        directors = session.query(Director).all()
        session.close()
        return directors

    def update_director(self, director):
        """
        Update an existing director in the database.
        :param director: Director object with updated data.
        """
        session = self.Session()
        existing_director = session.query(Director).filter_by(
            id=director.id).first()
        if existing_director:
            existing_director.name = director.name
            existing_director.birth_date = director.birth_date
            session.commit()
        session.close()

    def delete_director(self, director_id):
        """
        Delete a director by their ID.
        :param director_id: ID of the director to delete.
        """
        session = self.Session()
        director = session.query(Director).filter_by(id=director_id).first()
        if director:
            session.delete(director)
            session.commit()
        session.close()

    # --- Review CRUD Operations ---

    def add_review(self, review):
        """
        Add a new review to the database.
        :param review: Review object to be added.
        :return: The ID of the newly created review.
        """
        session = self.Session()
        session.add(review)
        session.commit()
        review_id = review.id
        session.close()
        return review_id

    def get_review(self, review_id):
        """
        Retrieve a review by its ID.
        :param review_id: ID of the review to retrieve.
        :return: Review object.
        """
        session = self.Session()
        review = session.query(Review).filter_by(id=review_id).first()
        session.close()
        return review

    def get_movie_reviews(self, movie_id):
        """
        Retrieve all reviews for a specific movie.
        :param movie_id: ID of the movie whose reviews are to be retrieved.
        :return: A list of Review objects.
        """
        session = self.Session()
        reviews = session.query(Review).filter_by(movie_id=movie_id).all()
        session.close()
        return reviews

    def update_review(self, review):
        """
        Update an existing review in the database.
        :param review: Review object with updated data.
        """
        session = self.Session()
        existing_review = session.query(Review).filter_by(id=review.id).first()
        if existing_review:
            existing_review.review_text = review.review_text
            existing_review.rating = review.rating
            session.commit()
        session.close()

    def delete_review(self, review_id):
        """
        Delete a review by its ID.
        :param review_id: ID of the review to delete.
        """
        session = self.Session()
        review = session.query(Review).filter_by(id=review_id).first()
        if review:
            session.delete(review)
            session.commit()
        session.close()