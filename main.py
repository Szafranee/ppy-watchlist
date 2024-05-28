import json
from datetime import datetime, date

import collection_manager
import file_operations
import film

film_collection = collection_manager.CollectionManager()

film_collection.add_film(film.Film("The Shawshank Redemption", "Frank Darabont", 1994, 142, ("Drama", "Crime")))
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

film1 = film.Film("Who killed Captain Alex?", "Nabwana I.G.G.", 2010, 68, ("Action", "Comedy"))
film2 = film.Film("The Room", "Tommy Wiseau", 2003, 99, "Drama")

film1.set_rating(10)
film2.set_rating(9.5)

film1.set_status("watched")
film1.add_comment("This is a great movie!")
film1.add_comment("XD")
film1.add_watch_date("2021-05-05")
film1.add_watch_date("2021-05-08")

film2.set_status("watched")
film2.add_comment("I love this movie!")
film2.add_watch_date("2021-05-06")

print("Collection before adding films:")

file_operations.write_collection_to_json_file("films.json", film_collection)

file_operations.load_collection_from_json_file("films.json", film_collection)

print(film_collection)

film_collection.add_film(film1)
film_collection.add_film(film2)

for film in film_collection.get_films():
    film.load_cover_image_path("dark_knight.jpg")


print("Collection after adding films:")
file_operations.write_collection_to_json_file("films.json", film_collection)

file_operations.load_collection_from_json_file("films.json", film_collection)

print(film_collection)



file_operations.export_to_txt_file("films.txt", film_collection)