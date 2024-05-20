from datetime import datetime

from exceptions import ScaleError

status = ["watched", "not watched"]


class Film:
    def __init__(self, title: str, director: str, year: int, length: int, genre: str, rating=0.0,
                 watch_status="not watched"):
        self.__title = title
        self.__director = director
        self.__year = year
        self.__length = length
        self.__rating = rating
        self.__genre = genre
        self.__status = watch_status
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
        return self.__status

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
        self.__rating = rating
        if self.__rating < 0 or self.__rating > 10:
            raise ScaleError("Rating must be in range 0-10")

    def change_status(self):
        self.__status = status[0] if self.__status == status[1] else status[1]

    def add_comment(self, comment: str):
        self.__comments.append(comment)

    def add_watch_date(self, date: str):
        self.__watch_dates.append(date)

    # ========== Overriden default methods

    def __str__(self):
        film_info = "● "
        if self.__status == "watched" and len(self.__comments) == 0:  # If the film is watched but has no comments
            film_info += f"{self.__title} ({self.__year}), directed by {self.__director}.\n"
            film_info += (f"\t- Genre: {self.__genre}\n"
                          f"\t- Length: {self.__length} minutes\n"
                          f"\t- Rating: {self.__rating}/10\n"
                          f"\t- Status: {self.__status}\n"
                          f"\t- Watched on: {', '.join(self.__watch_dates)}")
        elif self.__status == "watched" and len(self.__comments) > 0:  # If the film is watched and has comments
            film_info += f"{self.__title} ({self.__year}), directed by {self.__director}.\n"
            film_info += (f"\t- Genre: {self.__genre}\n"
                          f"\t- Length: {self.__length} minutes\n"
                          f"\t- Rating: {self.__rating}/10\n"
                          f"\t- Status: {self.__status}\n"
                          f"\t- Watched on: {', '.join(self.__watch_dates)}\n"
                          f"\t- Comments: {', '.join(self.__comments)}")
        elif not self.__status == "not watched" and len(self.__comments) > 0:  # if the film is not watched but commented
            film_info += f"{self.__title} ({self.__year}), directed by {self.__director}.\n"
            film_info += (f"\t- Genre: {self.__genre}\n"
                          f"\t- Length: {self.__length} minutes\n"
                          f"\t- Rating: {self.__rating}/10\n"
                          f"\t- Status: {self.__status}\n"
                          f"\t- Comments: {', '.join(self.__comments)}")
        else:  # if the film is not watched and has no comments
            film_info += f"{self.__title} ({self.__year}), directed by {self.__director}.\n"
            film_info += (f"\t- Genre: {self.__genre}\n"
                          f"\t- Length: {self.__length} minutes\n"
                          f"\t- Rating: {self.__rating}/10\n"
                          f"\t- Status: {self.__status}")

        film_info += "\n"
        return film_info

    def __repr__(self):
        return f"Film('{self.__title}', '{self.__director}', {self.__year}, '{self.__genre}', {self.__rating}, {self.__status}, {self.__comments}, {self.__watch_dates})"

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
