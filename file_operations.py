import json

import film


def write_collection_to_json_file(file_path, film_collection):
    with open(file_path, "w") as file:
        films = film_collection.get_films()
        films_json = []
        for film_obj in films:
            film_dict = film_obj.to_dict()
            films_json.append(film_dict)

        json.dump(films_json, file, indent=4)


def load_collection_from_json_file(file_path, film_collection):
    # Clear the collection before loading the films
    film_collection.clear_collection()
    with open(file_path, "r") as file:
        data = json.load(file)
        for film_json in data:
            film_obj = film.Film(film_json["title"], film_json["director"], film_json["year"],
                                 film_json["length"], film_json["genre"])
            if "rating" in film_json:
                film_obj.set_rating(film_json["rating"])
            if "watch_status" in film_json:
                film_obj.set_status(film_json["watch_status"])
            if "comments" in film_json:
                for comment in film_json["comments"]:
                    film_obj.add_comment(comment)
            if "watch_dates" in film_json:
                for watch_date in film_json["watch_dates"]:
                    film_obj.add_watch_date(watch_date)
            if "cover_image_path" in film_json:
                film_obj.set_cover_image_path(film_json["cover_image_path"])
            film_collection.add_film(film_obj)


def export_to_txt_file(file_path, film_collection):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("=================Your awesome film collection!=======================\n\n")
        file.write(str(film_collection))
        file.write("=====================================================================\n")

    # Remove trailing empty lines
    remove_trailing_empty_lines(file_path)


def remove_trailing_empty_lines(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Remove trailing empty lines
    while lines and not lines[-1].strip():
        lines.pop()

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)


def select_directory():
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory()
    return folder_selected
