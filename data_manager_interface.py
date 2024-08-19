from abc import ABC, abstractmethod


class DataManagerInterface(ABC):
    """Abstract base class defining the interface
    for data management operations."""

    @abstractmethod
    def get_all_users(self):
        """Retrieve all users from the database."""
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        """Retrieve all movies associated with a specific user."""
        pass

    @abstractmethod
    def add_user(self, user):
        """Add a new user to the database."""
        pass

    @abstractmethod
    def add_movie(self, movie, user_id):
        """Add a new movie to a specific user's movie list."""
        pass

    @abstractmethod
    def update_movie(self, movie):
        """Update the details of a specific movie in the database."""
        pass

    @abstractmethod
    def delete_movie(self, movie_id):
        """Delete a specific movie from the database."""
        pass
