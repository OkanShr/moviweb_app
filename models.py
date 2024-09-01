from sqlalchemy import Column, Text, Integer, String, ForeignKey, Float, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

movie_genre_table = Table('movie_genre', Base.metadata,
                          Column('movie_id', Integer,
                                 ForeignKey('movies.id'),
                                 primary_key=True),
                          Column('genre_id', Integer,
                                 ForeignKey('genres.id'),
                                 primary_key=True)
                          )


class Genre(Base):
    """
    Genre model representing a genre of movies in the database.

    Attributes:
        id (int): Unique identifier for the genre.
        name (str): Name of the genre.
    """
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    movies = relationship('Movie', secondary=movie_genre_table,
                          back_populates='genres')

    def __repr__(self):
        return f"Genre(id={self.id}, name={self.name})"


class User(Base):
    """
    User model representing a user in the database.

    Attributes:
        id (int): Unique identifier for the user.
        name (str): Name of the user.
        movies (list): List of movies associated with the user.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    movies = relationship('Movie', backref='user',
                          cascade='all, delete-orphan')

    def __repr__(self):
        return f"User(id={self.id}, name={self.name})"


class Movie(Base):
    """
    Movie model representing a movie in the database.

    Attributes:
        id (int): Unique identifier for the movie.
        title (str): Name of the movie.
        director (str): Director of the movie.
        year (int): Year of release.
        rating (float): Rating of the movie.
        user_id (int): ID of the user who added the movie.
    """
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    director_id = Column(Integer, ForeignKey('directors.id'), nullable=False)
    year = Column(String, nullable=False)
    rating = Column(String, nullable=False)
    poster = Column(String)
    plot = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    director = relationship('Director', back_populates='movies')
    genres = relationship('Genre', secondary=movie_genre_table,
                          back_populates='movies')

    def __repr__(self):
        director_name = self.director.name if self.director else "Unknown"
        return (f"Movie(id={self.id}, name={self.title}, "
                f"director={director_name}, year={self.year}, "
                f"rating={self.rating})")


class Review(Base):
    """
    Review model representing a user review of a movie.

    Attributes:
        id (int): Unique identifier for the review.
        user_id (int): ID of the user who wrote the review.
        movie_id (int): ID of the movie being reviewed.
        review_text (str): Text of the review.
        rating (float): Rating given by the user.
    """
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False)
    review_text = Column(Text, nullable=False)
    rating = Column(Float, nullable=False)

    user = relationship('User', backref='reviews')
    movie = relationship('Movie', backref='reviews')

    def __repr__(self):
        return (f"Review(id={self.id}, user_id={self.user_id}, "
                f"movie_id={self.movie_id}, rating={self.rating})")


class Director(Base):
    """
    Director model representing a movie director in the database.

    Attributes:
        id (int): Unique identifier for the director.
        name (str): Name of the director.
    """
    __tablename__ = 'directors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    movies = relationship('Movie',
                          back_populates='director')  # Relationship to Movie

    def __repr__(self):
        return f"Director(id={self.id}, name={self.name})"
