from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


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
    movies = relationship('Movie', backref='user',
                          cascade='all, delete-orphan')

    def __repr__(self):
        return f"User(id={self.id}, name={self.name})"


class Movie(Base):
    """
    Movie model representing a movie in the database.

    Attributes:
        id (int): Unique identifier for the movie.
        name (str): Name of the movie.
        director (str): Director of the movie.
        year (int): Year of release.
        rating (float): Rating of the movie.
        user_id (int): ID of the user who added the movie.
    """
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    director = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return (f"Movie(id={self.id}, name={self.name}, "
                f"director={self.director}, year={self.year}, "
                f"rating={self.rating})")
