from film import Film


class CollectionManager:
    def __init__(self):
        self.collection = []
        self.films = []

    def add_film(self, film: Film):
        self.collection.append(film)

    def remove_film(self, film: Film):
        self.collection.remove(film)

    def get_films(self):
        return self.collection

    def get_watched(self):
        return self.films

    def search_films(self, **kwargs):
        result = []
        for film in self.collection:
            if all(getattr(film, key) == value for key, value in kwargs.items()):
                result.append(film)
        return result

    def __str__(self):
        return '\n'.join([str(film) for film in self.collection])

    def watch_film(self, film: Film, date: str):
        self.films.append(film)
        film.get_watch_dates().append(date)
        film.set_status("watched")

    def print_watched(self):
        return '\n'.join([str(film) + ", watched on: " + ", ".join(film.get_watch_dates()) for film in self.films])

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
        genres_stats = {}
        for film in self.films:
            if film.get_genre() in genres_stats:
                genres_stats[film.get_genre()] += 1
            else:
                genres_stats[film.get_genre()] = 1
        return genres_stats

    def calculate_avg_rating(self, films):
        total = 0
        for film in self.films:
            total += film.get_rating()
        return total / len(films)

    def calculate_watch_stats(self, films):
        if films == self.get_films() or films == list(set(self.get_films()) - set(self.get_watched())):
            return None

        watch_stats = {}
        for film in films:
            watch_stats[film.get_title()] = (
                len(film.get_watch_dates()), film.get_length() * len(film.get_watch_dates()))

        return watch_stats

    def count_rated_film_by_genre(self, films):
        rated_films = [film for film in films if film.get_rating() > 0]
        return self.count_by_genres(rated_films)
