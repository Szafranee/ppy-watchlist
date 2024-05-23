from datetime import datetime

from exceptions import ScaleError

POSSIBLE_STATUSES = ["watched", "not watched"]


class Film:
    def __init__(self, title: str, director: str, year: int, length: int, genre: tuple):
        self.__title = title
        self.__director = director
        self.__year = year
        self.__length = length
        self.__genre = tuple(genre.split(", ")) if isinstance(genre, str) else genre
        self.__rating = 'Not rated yet'
        self.__watch_status = POSSIBLE_STATUSES[1]
        self.__comments = []
        self.__watch_dates = []

    # ========== Getters

    def get_title(self):
        return self.__title

    def get_director(self):
        return self.__director

    def get_year(self):
        return self.__year

    def get_length(self):
        return self.__length

    def get_rating(self):
        return self.__rating

    def get_genre(self):
        return self.__genre

    def get_status(self):
        return self.__watch_status

    def get_comments(self):
        return self.__comments

    def get_watch_dates(self):
        return self.__watch_dates

    # ========== Setters

    def set_title(self, title: str):
        self.__title = title

    def set_director(self, director: str):
        self.__director = director

    def set_year(self, year: int):
        self.__year = year

    def set_length(self, length: int):
        self.__length = length

    def set_genre(self, genre: str):
        self.__genre = genre

    def set_rating(self, rating: float):
        if rating == 'Not rated yet':
            self.__rating = rating
            return

        if rating < 0.0 or rating > 10.0:
            raise ScaleError("Rating must be in range 0-10")

        if rating % 1 == 0:
            rating = int(rating)

        self.__rating = rating

    def set_status(self, status: str):
        if status not in POSSIBLE_STATUSES:
            raise ValueError("Invalid status")
        self.__watch_status = status

    def change_status(self):
        self.__watch_status = POSSIBLE_STATUSES[0] if self.__watch_status == POSSIBLE_STATUSES[1] else \
            POSSIBLE_STATUSES[1]

    def add_comment(self, comment: str):
        self.__comments.append(comment)

    def add_watch_date(self, date: datetime.date):
        self.__watch_dates.append(date)

    # ========== Overriden default methods

    def __str__(self):
        film_info = "● "
        film_info += f"{self.__title} ({self.__year}), directed by {self.__director}.\n"
        film_info += (
            f"\t○ Genre(s): {', '.join(self.__genre)}\n"
            f"\t○ Length: {self.__length} minutes\n"
        )
        film_info += f"\t○ Rating: {self.__rating}/10\n" if self.__rating != 'Not rated yet' else f"\t○ Rating: {self.__rating}\n"
        film_info += f"\t○ Status: {self.__watch_status}\n"

        if self.__comments:
            film_info += "\t○ Comments:\n"
            for comment in self.__comments:
                film_info += f"\t\t- \"{comment}\"\n"

        if self.__watch_dates:
            film_info += "\t○ Watched on:\n"
            for date in self.__watch_dates:
                film_info += f"\t\t- {date}\n"

        return film_info

    def __repr__(self):
        return f"Film('{self.__title}', '{self.__director}', {self.__year}, '{self.__genre}', {self.__rating}, {self.__watch_status}, {self.__comments}, {self.__watch_dates})"

    def __eq__(self, other):
        return self.__title == other.get_title() and self.__director == other.get_director() and self.__year == other.get_year()

    def __lt__(self, other):
        return self.__year < other.get_year()

    def __le__(self, other):
        return self.__year <= other.get_year()

    def __gt__(self, other):
        return self.__year > other.get_year()

    def __ge__(self, other):
        return self.__year >= other.get_year()

    def __ne__(self, other):
        return self.__title != other.get_title() or self.__director != other.get_director() or self.__year != other.get_year()

    def __hash__(self):
        return hash((self.__title, self.__director, self.__year))

    # ========== Additional methods

    def to_dict(self):
        return {
            "title": self.__title,
            "director": self.__director,
            "year": self.__year,
            "length": self.__length,
            "rating": self.__rating,
            "genre": self.__genre,
            "watch_status": self.__watch_status,
            "comments": self.__comments,
            "watch_dates": [str(date) for date in self.__watch_dates]
            # convert date objects to string
        }

    def delete_comment(self):
        print("Select the comment you want to delete:")
        for i, comment in enumerate(self.__comments):
            print(f"{i + 1}. {comment}")
        try:
            index = int(input())
            self.__comments.pop(index - 1)
        except ValueError:
            print("Invalid input. Please enter a number.")
            self.delete_comment()
        except IndexError:
            print("Invalid input. Please enter a number from the list.")
            self.delete_comment()
