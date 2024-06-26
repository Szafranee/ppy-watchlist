from datetime import datetime, date

from film import Film


class CollectionManager:
    def __init__(self):
        self.film_collection = []
        self.watched_films = set()

    def add_film(self, film: Film):
        self.film_collection.append(film)
        self.film_collection.sort(key=lambda x: x.get_title())  # Keeps the collection sorted by title

    def remove_film(self, film: Film):
        self.film_collection.remove(film)

    def get_films(self):
        return self.film_collection

    def get_watched(self):
        return self.watched_films

    def add_to_watched(self):
        for film in self.film_collection:
            if film.get_status() == "watched":
                self.watched_films.add(film)

    def search_films(self, **kwargs):
        result = []
        for film in self.film_collection:
            if all(getattr(film, 'get_' + key)() == value for key, value in kwargs.items()):
                result.append(film)

        return result

    def __str__(self):
        response = ""
        for number, film in enumerate(self.film_collection, 1):
            response += str(number) + ". " + str(film) + "\n"
        return response

    def __repr__(self):
        return '\n'.join([repr(film) for film in self.film_collection])

    def watch_film(self, film: Film, watch_date: date):
        self.watched_films.add(film)
        if film.get_status() == "not watched":
            film.change_status()
        film.get_watch_dates().append(watch_date)

    def print_watched(self):
        response = ""
        for film in self.watched_films:
            response += str(film) + "\n"
        return response

    def generate_stats(self, films):
        films_stats = {}

        genre_stats = self.count_by_genres(films)
        films_stats["genres_stats"] = genre_stats

        avg_rating = self.calculate_avg_rating(films)
        films_stats["avg_rating"] = avg_rating

        watch_stats = self.calculate_watch_stats(films)
        films_stats["watch_stats"] = watch_stats

        rated_film_by_genre = self.count_rated_film_by_genre(films)
        films_stats["rated_film_by_genre"] = rated_film_by_genre

        return films_stats

    def count_by_genres(self, films):
        """
        Count the number of films in each genre
        :param films: list of films
        :return: dictionary with genres stats
        """
        genres_stats = {}
        for film in self.film_collection:
            genres = film.get_genre()
            if type(genres) is str:
                genres = [genres]
            for genre in genres:
                if genre in genres_stats:
                    genres_stats[genre] += 1
                else:
                    genres_stats[genre] = 1
        return genres_stats

    def calculate_avg_rating(self, films):
        total = 0
        num_of_rated_films = len([film for film in films if film.get_rating() != "Not rated yet"])

        for film in self.film_collection:
            if film.get_rating() == "Not rated yet":
                continue
            total += film.get_rating()
        return total / num_of_rated_films if num_of_rated_films != 0 else "No rated films yet"

    def calculate_watch_stats(self, films):
        """
        Calculate the total number of watches and total time spent watching the films
        :param films: list of films
        :return: dictionary with watch stats
        """
        if films == list(set(self.get_films()) - set(self.get_watched())):
            return None

        watch_stats = {}
        for film in films:
            watch_stats[film.get_title()] = (
                len(film.get_watch_dates()), film.get_length() * len(film.get_watch_dates()))

        return watch_stats

    def count_rated_film_by_genre(self, films):
        rated_films = [film for film in films if film.get_rating() != "Not rated yet"]
        return self.count_by_genres(rated_films)

    def clear_collection(self):
        self.film_collection = []
        self.watched_films = set()
