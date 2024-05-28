import tkinter as tk
import random

import requests
from PIL import Image, ImageTk

import collection_manager
import file_operations
import film

from dotenv import load_dotenv
import os

load_dotenv()

OMDB_API_KEY = os.getenv("OMDB_API_KEY")

# Sample film data (replace with your actual data)
film_collection = collection_manager.CollectionManager()
file_operations.load_collection_from_json_file("films.json", film_collection)


def export_to_file():
    # display a popup window with a message, text entry, and a button
    popup = tk.Toplevel()
    popup.title("Export to file")
    popup.geometry("300x150")
    popup.config(bg="#333")

    # create a label
    label = tk.Label(popup, text="Enter the name of a txt file to export to:\n (w/o the extension)",
                     bg="#333", fg="white", font=("Bahnschrift", 11, "bold"))
    label.pack(pady=10)

    # create an entry widget
    entry = tk.Entry(popup, bg="#444", fg="white")
    entry.pack(pady=10)

    # create a button
    button = tk.Button(popup, text="Export", command=lambda: export_to_file_action(entry.get()))
    button.pack(pady=10)

    # bind the <Return> event to the entry widget
    entry.bind("<Return>", lambda event: export_to_file_action(entry.get()))

    def export_to_file_action(file_name):
        # write the collection to a file
        file_operations.export_to_txt_file(file_name + ".txt", film_collection)
        # close the popup window
        popup.destroy()


class WatchlistApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Watchlist App")
        self.root.geometry("1200x900")
        self.root.tk_setPalette(background='#333', foreground='white')

        # Menu (same as before)
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Export to file", command=export_to_file)

        # Main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        # Search frame
        self.search_frame = tk.Frame(self.main_frame)
        self.search_frame.pack(pady=10)

        self.search_label = tk.Label(self.search_frame, text="Search:", fg="white")
        self.search_label.pack(side="left")

        self.search_entry = tk.Entry(self.search_frame)
        self.search_entry.pack(side="left")

        # film list frame
        self.film_list_frame = tk.Label(self.main_frame, text="Your films:", fg="white")
        # set label font size
        self.film_list_frame.config(font=("Bahnschrift", 18, "bold"))
        self.film_list_frame.pack()
        self.film_list_frame = tk.Frame(self.main_frame)
        self.film_list_frame.config(pady=10, padx=10)
        self.film_list_frame.pack(fill="both", expand=True)

        # Listbox (for holding film entries)
        self.film_listbox = tk.Listbox(self.film_list_frame, bg="#444", fg="white", selectbackground="#555")
        self.film_listbox.config(font=("Bahnschrift", 20, "bold"))
        self.film_listbox.pack(side="left", fill="both", expand=True)

        # Details frame (for displaying film details)
        self.details_frame = tk.Frame(self.film_list_frame, bg="#444")
        # add padding
        self.details_frame.config(pady=10, padx=10)
        self.details_frame.pack(side="left", fill="y")

        # Buttons
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(pady=10)

        self.add_button = tk.Button(self.button_frame, text="Add film", command=self.add_film)
        self.add_button.pack(side="left")
        self.edit_button = tk.Button(self.button_frame, text="Edit film", command=self.edit_film)
        self.edit_button.pack(side="left")
        self.delete_button = tk.Button(self.button_frame, text="Delete film", command=self.delete_film)
        self.delete_button.pack(side="left")

        # Populate film listbox initially
        self.populate_film_list()

        # Bind selection event for film listbox
        self.film_listbox.bind("<<ListboxSelect>>", self.display_film_details)

        # Bind export to file event to Ctrl+S
        self.root.bind("<Control-s>", lambda event: export_to_file())

        # Bind delete film event to Delete key
        self.root.bind("<Control-Delete>", lambda event: self.delete_film())

        self.root.bind(self.delete_button, self.delete_film)

        # Display details for the first film
        self.film_listbox.selection_set(0)  # Select the first film
        self.display_film_details(None)  # Call the function with a dummy event

    def populate_film_list(self):
        # Clear the listbox
        self.film_listbox.delete(0, tk.END)

        already_added = []
        # Add film entries to the listbox
        for film in film_collection.get_films():
            if film.get_title() in already_added:
                self.film_listbox.insert(tk.END, film.get_title() + " (" + str(film.get_year()) + ")")
            else:
                self.film_listbox.insert(tk.END, film.get_title())
                already_added.append(film.get_title())

    def display_film_details(self, event):
        # Clear the details frame
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        # Get the selected film
        selection = self.film_listbox.curselection()
        if selection:
            index = selection[0]
            film = film_collection.get_films()[index]

            # Load and resize image
            image_path = film.get_cover_image_path()
            # the image path can be a URL or a local path
            if image_path.startswith("http"):
                image = Image.open(requests.get(image_path, stream=True).raw)
                image = image.resize((300, 400))
            else:
                image = Image.open(image_path)
                image = image.resize((300, 400))
            photo = ImageTk.PhotoImage(image)

            # Create image label
            image_label = tk.Label(self.details_frame, image=photo)
            image_label.image = photo  # Keep a reference to avoid garbage collection
            image_label.pack(pady=10)

            # Create details labels
            for key, value in film.to_dict().items():
                if key == "cover_image_path":
                    continue
                if key == "comments":
                    if not value:  # Skip if there are no comments
                        continue
                    value = "\"" + "\", \"".join(value) + "\""
                if key == "watch_dates":
                    if not value:  # Skip if there are no watch dates
                        continue
                    key = "Watch dates"
                    value = ", ".join(value)
                if key == "watch_status":
                    key = "Watch status"
                if key == "length":
                    value = f"{value} minutes"
                if key == "rating":
                    value = f"{value}/10" if value != "Not rated yet" else value
                if key == "genre":
                    value = ", ".join(value) if isinstance(value, list) else value
                detail_frame = tk.Frame(self.details_frame, bg="#444")
                detail_frame.pack(fill="x")
                key_label = tk.Label(detail_frame, text=f"{key.capitalize()}:", bg="#444", fg="white",
                                     font=("Bahnschrift", 13))
                key_label.pack(side="left")
                value_label = tk.Label(detail_frame, text=f"{value}", bg="#444", fg="white",
                                       font=("Bahnschrift", 15, "bold"))
                value_label.pack(side="left")

    def search_by_title(self):
        pass

    def search_by_director(self):
        pass

    def add_film(self):
        # display a popup window with a message, 5 text entries, and a button
        popup = tk.Toplevel()
        popup.title("Add film")
        popup.geometry("300x400")
        popup.config(bg="#333")

        # create a label
        label = tk.Label(popup, text="Enter the details of the film:", bg="#333", fg="white",
                         font=("Bahnschrift", 11, "bold"))
        label.pack(pady=10)

        # create entry widgets
        entries = []
        for field in ["Title", "Director", "Year", "Length", "Genre(s)"]:
            entry_frame = tk.Frame(popup, bg="#333")
            entry_frame.pack(pady=5)
            label = tk.Label(entry_frame, text=field, bg="#333", fg="white")
            label.pack(side="left")
            entry = tk.Entry(entry_frame, bg="#444", fg="white")
            entry.pack(side="right")
            entries.append(entry)

        # create a button
        button = tk.Button(popup, text="Add", command=lambda: add_film_action(entries))
        button.pack(pady=10)

        # bind the <Return> event to the last entry widget
        entries[-1].bind("<Return>", lambda event: add_film_action(entries))

        def add_film_action(entries):
            # get the values from the entry widgets
            title, director, year, length, genres = [entry.get() for entry in entries]

            if not title:  # display an error message
                # destroy the previous error message if it exists
                for widget in popup.winfo_children():
                    if isinstance(widget, tk.Label) and widget.cget("fg") == "red":
                        widget.destroy()
                error_label = tk.Label(popup, text="Title cannot be empty!", bg="#333", fg="red")
                error_label.pack()
                return

            if not year:
                film_json = requests.get(f"https://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}").json()
            else:
                film_json = requests.get(f"https://www.omdbapi.com/?t={title}&y={year}&apikey={OMDB_API_KEY}").json()

            if title != film_json["Title"]:
                title = film_json["Title"]

            if not director:
                director = film_json["Director"]
            if not year:
                year = film_json["Year"]
            if not length:
                length = film_json["Runtime"].split(" ")[0]
            if not genres:
                genres = film_json["Genre"]

            # add the film to the collection
            new_film = film.Film(title, director, int(year), int(length), genres.split(", "))
            film_collection.add_film(new_film)
            # close the popup window
            popup.destroy()
            # repopulate the film listbox
            self.populate_film_list()
            # select the newly added film in the listbox
            self.search_in_listbox(new_film.get_title(), new_film.get_year())
            # display the details of the newly added film
            self.display_film_details(None)

    def edit_film(self):
        pass

    def delete_film(self):
        try:
            index = self.film_listbox.curselection()[0]
            film = film_collection.get_films()[index]
            film_collection.remove_film(film)
            self.film_listbox.delete(index)
        except IndexError:
            pass

    def search_in_listbox(self, title, year):
        if not title:
            return
        for i, film in enumerate(film_collection.get_films()):
            if title.lower() in film.get_title().lower() and year == film.get_year():
                self.film_listbox.selection_clear(0, tk.END)
                self.film_listbox.selection_set(i)
                self.film_listbox.see(i)
                break


if __name__ == "__main__":
    root = tk.Tk()
    app = WatchlistApp(root)
    root.mainloop()
    file_operations.write_collection_to_json_file("films.json", film_collection)
