from datetime import datetime, date

import collection_manager
import film

film_collection = collection_manager.CollectionManager()

film_collection.add_film(film.Film("The Shawshank Redemption", "Frank Darabont", 1994, 142, "Drama"))
film_collection.add_film(film.Film("The Dark Knight", "Christopher Nolan", 2008, 152, "Action"))
film_collection.add_film(film.Film("Inception", "Christopher Nolan", 2010, 148, "Action"))
film_collection.add_film(film.Film("The Matrix", "Lana Wachowski", 1999, 136, "Action"))
film_collection.add_film(film.Film("Interstellar", "Christopher Nolan", 2014, 169, "Sci-Fi"))
film_collection.add_film(
    film.Film("The Lord of the Rings: The Return of the King", "Peter Jackson", 2003, 201, "Fantasy"))
film_collection.add_film(film.Film("The Godfather", "Francis Ford Coppola", 1972, 175, "Crime"))
film_collection.add_film(film.Film("The Dark Knight Rises", "Christopher Nolan", 2012, 164, "Action"))
film_collection.add_film(
    film.Film("The Lord of the Rings: The Fellowship of the Ring", "Peter Jackson", 2001, 178, "Fantasy"))
film_collection.add_film(film.Film("The Lord of the Rings: The Two Towers", "Peter Jackson", 2002, 179, "Fantasy"))

film_collection.watch_film(film_collection.get_films()[0], date(2021, 5, 5))
film_collection.watch_film(film_collection.get_films()[0], date(2021, 5, 8))
film_collection.watch_film(film_collection.get_films()[1], date(2021, 5, 6))

film_collection.get_films()[0].add_comment("This is a great movie!")
film_collection.get_films()[0].add_comment("I love it!")

film_collection.get_films()[1].add_comment("I love this movie!")

film_collection.get_films()[2].add_comment("This is a great movie! POG")

print(film_collection)

print(film_collection.print_watched())


