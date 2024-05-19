# TODO implement the class
from film import Film


class CollectionManager:
    def __init__(self):
        self.collection = []
        self.watched = []

    def add_film(self, film: Film):
        self.collection.append(film)

    def remove_film(self, film: Film):
        self.collection.remove(film)

    def get_films(self):
        return self.collection

    def get_watched(self):
        return self.watched

    def search_films(self, **kwargs):
        result = []
        for film in self.collection:
            if all(getattr(film, key) == value for key, value in kwargs.items()):
                result.append(film)
        return result

    def __str__(self):
        return '\n'.join([str(film) for film in self.collection])

    def watch_film(self, film: Film, date: str):
        self.watched.append(film)
        film.get_watch_dates().append(date)
        film.set_status("watched")

    def print_watched(self):
        return '\n'.join([str(film) + ", watched on: " + ", ".join(film.get_watch_dates()) for film in self.watched])