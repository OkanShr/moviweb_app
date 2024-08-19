from abc import ABC, abstractmethod


class DataManagerInterface(ABC):
    """
    Interface:
    Basic CRUD functions that we need
    """
    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        pass

    @abstractmethod
    def add_user(self, user):
        pass

    @abstractmethod
    def add_movie(self, movie, user_id):
        pass

    @abstractmethod
    def update_movie(self, movie):
        pass

    @abstractmethod
    def delete_movie(self, movie_id):
        pass
