import tkinter
import tkinter as tk
from datetime import date

import requests
from PIL import Image, ImageTk

import collection_manager
import file_operations
import film
import exceptions

from dotenv import load_dotenv
import os

import ctypes as ct

load_dotenv()

OMDB_API_KEY = os.getenv("OMDB_API_KEY")

# Sample film data (replace with your actual data)
film_collection = collection_manager.CollectionManager()
file_operations.load_collection_from_json_file("films.json", film_collection)
film_collection.add_to_watched()


def dark_title_bar(window):
    """
    This function is used to apply a dark theme to the title bar of a window.

    Args:
        window (tkinter.Tk): The window to apply the dark theme to.
    """
    window.update()
    dwmwa_use_immersive_dark_mode = 20
    set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
    get_parent = ct.windll.user32.GetParent
    hwnd = get_parent(window.winfo_id())
    rendering_policy = dwmwa_use_immersive_dark_mode
    value = 2
    value = ct.c_int(value)
    set_window_attribute(hwnd, rendering_policy, ct.byref(value),
                         ct.sizeof(value))


def export_to_file():
    """
    This function is used to export the film collection to a file.
    It opens a popup window where the user can enter the path to the directory where they want to save the file.
    """
    # display a popup window with a message, text entry, and a button
    popup_top = tk.Toplevel()
    popup_top.title("Export to file")
    popup_top.geometry("455x195")
    popup_top.config(bg="#333")


    label = tk.Label(popup_top, text="Enter the path to a directory where you want to save the file:\n"
                                     "(e.g. C:/Users/JohnDoe/Desktop/films)\n"
                                     "or select a directory:", bg="#333", fg="white", font=("Bahnschrift", 11, "bold"))
    label.pack(pady=10)

    entry = tk.Entry(popup_top, bg="#444", fg="white")
    entry.pack(side="top", padx=10)

    # put the button next to the entry widget
    icon = tk.PhotoImage(file="img/folder_icon_white.png")
    icon = icon.subsample(20)
    button = tk.Button(popup_top, text="Choose a directory: ", image=icon, compound="right",
                       command=lambda: select_directory(entry))
    button.image = icon
    button.pack(side="top", pady=5)

    # create a button
    button = tk.Button(popup_top, text="Choose", command=lambda: set_file_name(entry.get()))
    button.pack(pady=10, side="top")

    # center the popup window
    center_popup(popup_top)

    # bind the <Return> event to the entry widget
    entry.bind("<Return>", lambda event: export_to_file_action(entry.get(), popup_top))

    def select_directory(entry):
        # open a directory selection dialog
        directory = file_operations.select_directory()
        # set the selected directory as the entry widget's value
        entry.delete(0, tk.END)
        entry.insert(0, directory)
        # set the focus to the entry widget
        entry.focus()

    def set_file_name(file_target_dir):
        popup = tk.Toplevel()
        popup.title("Choose file name")
        popup.geometry("370x150")
        popup.config(bg="#333")

        label = tk.Label(popup, text="Enter the name of the file (without the extension):", bg="#333", fg="white",
                         font=("Bahnschrift", 11, "bold"))
        label.pack(pady=10)

        entry = tk.Entry(popup, bg="#444", fg="white")
        entry.pack(pady=10)

        button = tk.Button(popup, text="Export",
                           command=lambda: export_to_file_action(file_target_dir + "/" + entry.get(), popup))
        button.pack(pady=10)

        center_popup(popup)

    def export_to_file_action(file_name, popup):
        popup.destroy()
        if not file_name:
            # display an error message
            # destroy the previous error message if it exists
            for widget in popup.winfo_children():
                if isinstance(widget, tk.Label) and widget.cget("fg") == "red":
                    widget.destroy()
            error_label = tk.Label(popup, text="File name cannot be empty!", bg="#333", fg="red")
            error_label.pack()
            return

        try:
            file_operations.export_to_txt_file(file_name + ".txt", film_collection)
            popup.destroy()
        except exceptions.FileError as e:
            # display an error message
            # destroy the previous error message if it exists
            for widget in popup.winfo_children():
                if isinstance(widget, tk.Label) and widget.cget("fg") == "red":
                    widget.destroy()
            error_label = tk.Label(popup, text=str(e), bg="#333", fg="red")
            error_label.pack()
            return

        check_if_file_was_created(file_name + ".txt", popup)

    def check_if_file_was_created(file_name, popup):
        popup_top.destroy()
        if os.path.exists(file_name):
            tkinter.messagebox.showinfo("Success", f"File {file_name} was created successfully!")
        else:
            tkinter.messagebox.showerror("Error", f"File {file_name} was not created!")


def center_popup(popup):
    dark_title_bar(popup)
    popup.update_idletasks()
    width = popup.winfo_width()
    height = popup.winfo_height()
    x = (popup.winfo_screenwidth() // 2) - (width // 2)
    y = (popup.winfo_screenheight() // 2) - (height // 2)
    popup.geometry(f"{width}x{height}+{x}+{y}")


def generate_stats():
    """
    This function is used to generate statistics about the film collection.
    It opens a popup window where the statistics are displayed.
    """
    # display a popup window with the stats
    popup = tk.Toplevel()
    popup.title("Stats")
    popup.geometry("800x850")
    popup.config(bg="#333")


    title_label = tk.Label(popup, text="Your statistics:", bg="#333", fg="white", font=("Bahnschrift", 22, "bold"))
    title_label.pack(pady=(10, 20))

    stats = film_collection.generate_stats(film_collection.get_films())
    response = ""

    for key, value in stats.items():
        if key == "genres_stats":
            # set color to red if the value is empty
            response += f"● Number of films by genre:\n"
            value = sorted(value.items(), key=lambda x: x[1], reverse=True)
            for genre, count in value:
                response += f"   ○ {genre}: {count} films\n"
        elif key == "avg_rating":
            value = round(value, 2)
            response += (f"● Average rating:\n"
                         f"     {value}\n")
        elif key == "watch_stats":
            response += "● Top 10 most watched films:\n"
            if not value:
                response += "   ○ No films watched yet\n"
            else:
                value = sorted(value.items(), key=lambda x: x[1], reverse=True)
                rank = 1
                for film, count in value[:10]:
                    response += f"    {rank}. {film}: ({count[0]} times, {count[1]} minutes total)\n"
                    rank += 1
        elif key == "rated_film_by_genre":
            response += "● Number of rated films by genre:\n"
            value = sorted(value.items(), key=lambda x: x[1], reverse=True)
            for genre, count in value:
                response += f"   ○ {genre}: {count} films\n"
        else:
            response += f"   ○ {value}\n"

        response += "\n"

    label = tk.Label(popup, text=response, bg="#333", fg="white", font=("Bahnschrift", 14, "bold"))
    # allign the text to the left
    label.config(justify="left")

    label.pack(pady=10)
    center_popup(popup)


class WatchlistApp:
    def __init__(self, root):
        """
        This is the constructor of the WatchlistApp class. It initializes the main window of the application.
        It creates the main frame, search frame, film list frame, details frame, and buttons.
        It also populates the film listbox with the films from the film collection.
        """
        self.root = root
        self.root.title("Watchlist App")
        self.root.geometry("1600x1000")
        self.root.tk_setPalette(background='#333', foreground='white')
        self.last_search = ""
        self.current_film = 0
        self.is_show_only_watched = tk.BooleanVar()

        # center the window
        center_popup(self.root)

        # Menu (same as before)
        self.menu = tk.Menu(self.root, bg='blue', fg="white")

        # Menubar
        self.file_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Export to file", command=export_to_file)

        self.stats_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="Stats", menu=self.stats_menu)
        self.stats_menu.add_command(label="Generate stats", command=lambda: generate_stats())

        self.root.config(menu=self.menu)

        # Main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)
        # Search frame
        self.search_frame = tk.Frame(self.main_frame)
        self.search_frame.pack(pady=10)

        self.search_label = tk.Label(self.search_frame, text="Search:", fg="white")
        self.search_label.config(font=("Bahnschrift", 16, "bold"))
        self.search_label.pack(side="left")

        self.search_entry = tk.Entry(self.search_frame)
        self.search_entry.config(font=("Bahnschrift", 14))
        self.search_entry.pack(side="left", padx=10)

        self.search_button = tk.Button(self.search_frame, text="Search",
                                       command=lambda: self.search(self.search_entry.get()))
        self.search_button.config(font=("Bahnschrift", 14, "bold"))
        self.search_button.pack(side="left")

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

        self.watch_film_button = tk.Button(self.button_frame, text="Watch film",
                                           command=self.watch_film)
        self.watch_film_button.config(font=("Bahnschrift", 18, "bold"))
        self.watch_film_button.config(activebackground="DarkOrchid3")
        self.watch_film_button.pack(side="left", padx=10, pady=10)

        self.rate_film_button = tk.Button(self.button_frame, text="Rate film", command=self.rate_film)
        self.rate_film_button.config(font=("Bahnschrift", 18, "bold"))
        self.rate_film_button.config(activebackground="goldenrod1")
        self.rate_film_button.pack(side="left", padx=10, pady=10)

        self.add_comment_button = tk.Button(self.button_frame, text="Add comment", command=self.add_comment)
        self.add_comment_button.config(font=("Bahnschrift", 18, "bold"))
        self.add_comment_button.config(activebackground="sea green")
        self.add_comment_button.pack(side="left", padx=(10, 120), pady=10)

        self.add_button = tk.Button(self.button_frame, text="Add film", command=self.add_film)
        self.add_button.config(font=("Bahnschrift", 18, "bold"))
        self.add_button.config(activebackground="lightgreen")
        self.add_button.pack(side="left", padx=10, pady=10)

        self.edit_button = tk.Button(self.button_frame, text="Edit film", command=self.edit_film)
        self.edit_button.config(font=("Bahnschrift", 18, "bold"))
        self.edit_button.config(activebackground="lightblue")
        self.edit_button.pack(side="left", padx=10, pady=10)

        self.delete_button = tk.Button(self.button_frame, text="Delete film", command=self.delete_film)
        self.delete_button.config(font=("Bahnschrift", 18, "bold"))
        self.delete_button.config(activebackground="lightcoral")
        self.delete_button.pack(side="left", padx=10, pady=10)

        self.only_watched_button = tk.Checkbutton(self.button_frame, text="Show only watched",
                                                  variable=self.is_show_only_watched,
                                                  onvalue=True, offvalue=False,
                                                  command=lambda: self.show_only_watched(
                                                      self.is_show_only_watched.get()))
        self.only_watched_button.config(font=("Bahnschrift", 18, "bold"), bg="#333", fg="white", selectcolor="black",
                                        foreground="white")
        self.only_watched_button.pack(side="left", padx=10, pady=10)

        # Populate film listbox initially
        self.populate_film_list()

        # Bind export to file event to Ctrl+S
        self.root.bind("<Control-s>", lambda event: export_to_file())

        # Bind delete film event to Delete key
        self.root.bind("<Control-Delete>", lambda event: self.delete_film())

        self.film_listbox.bind("<<ListboxSelect>>", self.set_default_color_on_select)

        # Display details for the first film
        self.film_listbox.selection_set(0)  # Select the first film
        self.display_film_details()  # Call the function with a dummy event

    def populate_film_list(self):
        """
        This method is used to populate the film listbox with the films in the collection.
        """
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

    def display_film_details(self):
        """
        This method is used to display the details of a film in the details frame.
        """
        # Clear the details frame
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        # Get the selected film
        selection = self.film_listbox.curselection()
        if selection:
            index = selection[0]
            if self.is_show_only_watched.get():
                film = list(film_collection.get_watched())[index]
            else:
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

                if key == "director":
                    value = ", ".join(value) if isinstance(value, list) else value

                    key = "Director"
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
                                       font=("Bahnschrift", 15, "bold"), wraplength=500)
                value_label.pack(side="left")

    def search(self, value_to_find):
        """
        This method is used to search for a film in the collection.
        It highlights the found film in the listbox and displays its details.
        It also clears the selection if the search is empty.
        It displays an error message if no results are found.

        Args:
            value_to_find (str): The value to search for.
        """
        # Clear the listbox selection to clear the last search when a new search is performed
        # but the user didn't select all last results
        self.film_listbox.selection_clear(0, tk.END)
        for i in range(self.film_listbox.size()):
            self.film_listbox.itemconfig(i, selectbackground="#555", selectforeground="white")
            self.film_listbox.itemconfig(i, background="#444", foreground="white")

        if not value_to_find:
            return

        found_films = []

        for i, film in enumerate(film_collection.get_films()):
            for value in film.to_dict().values():
                if value_to_find.lower() in str(value).lower():
                    self.film_listbox.itemconfig(i, selectbackground="#abffb6", selectforeground="black")
                    self.film_listbox.itemconfig(i, background="#abffb6", foreground="black")
                    self.film_listbox.see(i)
                    self.film_listbox.selection_set(i)
                    self.display_film_details()
                    found_films.append(i)
                    break

        if not found_films:
            self.search_entry.delete(0, tk.END)
            self.search_entry.insert(0, "No results found")
            self.search_entry.config(fg="red")
            self.root.after(2000, lambda: self.search_entry.delete(0, tk.END))

    def add_film(self):
        """
        This method is used to add a film to the collection.
        It opens a popup window where the user can enter the details of the film.
        """
        # kill the popup window if it exists
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Toplevel):
                widget.destroy()

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
        for field in ["Title", "Director", "Year", "Length", "Genre(s)", "Cover image path"]:
            entry_frame = tk.Frame(popup, bg="#333")
            entry_frame.pack(pady=5)
            label = tk.Label(entry_frame, text=field, bg="#333", fg="white")
            label.pack(side="left")
            entry = tk.Entry(entry_frame, bg="#444", fg="white")
            entry.pack(side="right")
            entries.append(entry)

        for entry in entries:
            # make entry widget expandable
            entry.pack(fill="x")

        # center the popup window
        center_popup(popup)

        # create a button
        button = tk.Button(popup, text="Add", command=lambda: add_film_action(entries))
        button.pack(pady=10)

        # bind the <Return> event to the last entry widget
        entries[-1].bind("<Return>", lambda event: add_film_action(entries))

        def add_film_action(entries):
            # get the values from the entry widgets
            title, director, year, length, genres, cover_file_path = [entry.get() for entry in entries]

            if not title:  # display an error message
                # destroy the previous error message if it exists
                for widget in popup.winfo_children():
                    if isinstance(widget, tk.Label) and widget.cget("fg") == "red":
                        widget.destroy()
                error_label = tk.Label(popup, text="Title cannot be empty!", bg="#333", fg="red")
                error_label.pack()
                return

            is_custom_film = False

            if not year:
                film_json = requests.get(f"https://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}").json()
                if film_json["Response"] == "False":
                    is_custom_film = True
            else:
                film_json = requests.get(f"https://www.omdbapi.com/?t={title}&y={year}&apikey={OMDB_API_KEY}").json()
                if film_json["Response"] == "False":
                    is_custom_film = True

            if not is_custom_film:
                if title != film_json["Title"]:
                    title = film_json["Title"]

                if not director:
                    director = film_json["Director"]
                if not year:
                    year = film_json["Year"]
                if not length:
                    length = film_json["Runtime"].split(" ")[0]
                    if length == "N/A":
                        length = 0
                if not genres:
                    genres = film_json["Genre"]
            else:
                if not director:
                    director = "Unknown"
                if not year:
                    year = 0
                if not length:
                    length = 0
                if not genres:
                    genres = "Unknown"

            if cover_file_path:
                if cover_file_path.startswith("http"):
                    image = Image.open(requests.get(cover_file_path, stream=True).raw)
                else:
                    image = Image.open(cover_file_path)
                image = image.resize((300, 400))
                image.save(f"img/{title}.png")
                cover_file_path = f"img/{title}.png"
            else:
                cover_file_path = "N/A"

            # add the film to the collection
            new_film = film.Film(title, director.split(", "), year, length, genres.split(", "))
            film_collection.add_film(new_film)
            # close the popup window
            popup.destroy()
            # repopulate the film listbox
            self.populate_film_list()
            # select the newly added film in the listbox
            self.search_in_listbox(new_film.get_title(), new_film.get_year())
            # display the details of the newly added film
            self.display_film_details()

    def edit_film(self):
        """
        This method is used to add a film to the collection.
        It opens a popup window where the user can enter the details of the film.
        It also populates the entry widgets with the details of the selected film.
        It displays an error message if the title is empty.
        """
        pass
        # display a popup window with a message, 5 text entries, and a button
        popup = tk.Toplevel()
        popup.title("Edit film")
        popup.geometry("300x400")
        popup.config(bg="#333")

        # create a label
        label = tk.Label(popup, text="Enter the details of the film:", bg="#333", fg="white",
                         font=("Bahnschrift", 11, "bold"))
        label.pack(pady=10)

        # create entry widgets
        entries = []
        for field in ["Title", "Director", "Year", "Length", "Genre(s)", "Cover image path"]:
            entry_frame = tk.Frame(popup, bg="#333")
            entry_frame.pack(pady=5)
            label = tk.Label(entry_frame, text=field, bg="#333", fg="white")
            label.pack(side="left")
            entry = tk.Entry(entry_frame, bg="#444", fg="white")
            entry.pack(side="right")
            entries.append(entry)

        # center the popup window
        center_popup(popup)

        # get the selected film
        selection = self.film_listbox.curselection()
        index = selection[0]
        selected_film = film_collection.get_films()[index]

        # populate the entry widgets with the selected film's details
        values = []
        for key, value in selected_film.to_dict().items():
            if key in ["title", "director", "year", "length", "genre", "cover_image_path"]:
                if isinstance(value, list):
                    value = ", ".join(value)
                values.append(value)

        for entry, value in zip(entries, values):
            entry.insert(0, value)

        # create a button
        button = tk.Button(popup, text="Edit", command=lambda: edit_film_action(entries))
        button.pack(pady=10)

        # bind the <Return> event to the last entry widget
        entries[-1].bind("<Return>", lambda event: edit_film_action(entries))

        def edit_film_action(entries):
            # get the values from the entry widgets
            title, director, year, length, genres, cover_file_path = [entry.get() for entry in entries]

            # check if the director and genre are lists
            if "," in director:
                director = director.split(", ")
            if "," in genres:
                genres = genres.split(", ")

            if not title:
                # display an error message
                # destroy the previous error message if it exists
                for widget in popup.winfo_children():
                    if isinstance(widget, tk.Label) and widget.cget("fg") == "red":
                        widget.destroy()
                error_label = tk.Label(popup, text="Title cannot be empty!", bg="#333", fg="red")
                error_label.pack()
                return

            is_custom_film = False

            if not year:
                film_json = requests.get(f"https://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}").json()
                if film_json["Response"] == "False":
                    is_custom_film = True
            else:
                film_json = requests.get(f"https://www.omdbapi.com/?t={title}&y={year}&apikey={OMDB_API_KEY}").json()
                if film_json["Response"] == "False":
                    is_custom_film = True

            if not is_custom_film:
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
                if not cover_file_path:
                    cover_file_path = film_json["Poster"]
            else:
                if not director:
                    director = "Unknown"
                if not year:
                    year = 0
                if not length:
                    length = 0
                if not genres:
                    genres = "Unknown"
                if not cover_file_path:
                    cover_file_path = "img/missing_cover.png"

            selected_film.set_title(title)
            selected_film.set_director(director)
            selected_film.set_year(int(year))
            selected_film.set_length(int(length))
            selected_film.set_genre(genres)
            selected_film.set_cover_image_path(cover_file_path)
            popup.destroy()

            self.populate_film_list()

            self.search_in_listbox(selected_film.get_title(), selected_film.get_year())

            self.display_film_details()

    def delete_film(self):
        """
        This method is used to delete a film from the collection.
        """
        try:
            index = self.film_listbox.curselection()[0]
            film = film_collection.get_films()[index]
            film_collection.remove_film(film)
            self.film_listbox.delete(index)
            self.film_listbox.selection_set(index)
            self.display_film_details()
        except IndexError:
            pass

    def watch_film(self):
        """
        This method is used to mark a film as watched.
        It opens a popup window where the user can enter the watch date. If the watch date is empty, the current date
        is used.
        """

        popup = tk.Toplevel()
        popup.title("Watch film")
        popup.geometry("400x175")
        popup.config(bg="#333")

        label = tk.Label(popup, text="Enter the watch date (YYYY-MM-DD)\nor leave empty for today:", bg="#333",
                         fg="white", font=("Bahnschrift", 11, "bold"))
        label.pack(pady=10)

        entry = tk.Entry(popup, bg="#444", fg="white")
        entry.pack(pady=10)

        center_popup(popup)

        button = tk.Button(popup, text="Watch", command=lambda: watch_film_action(entry.get()))
        button.pack(pady=10)

        entry.bind("<Return>", lambda event: watch_film_action(entry.get()))

        def watch_film_action(watch_date):
            if not watch_date:
                watch_date = date.today().isoformat()
            else:
                try:
                    year, month, day = map(int, watch_date.split("-"))
                    date(year, month, day)
                except ValueError:
                    for widget in popup.winfo_children():
                        if isinstance(widget, tk.Label) and widget.cget("fg") == "red":
                            widget.destroy()
                    error_label = tk.Label(popup,
                                           text="Invalid date format! Please enter a date in the format YYYY-MM-DD.",
                                           bg="#333", fg="red")
                    error_label.pack()
                    return

            index = self.film_listbox.curselection()[0]
            film = film_collection.get_films()[index]
            film_collection.watch_film(film, watch_date)
            popup.destroy()
            self.display_film_details()

    def rate_film(self):
        """
        This method is used to rate a film.
        It opens a popup window where the user can enter the rating. If the rating is empty or not in the range 0-10,
        an error message is displayed.
        """
        popup = tk.Toplevel()
        popup.title("Rate film")
        popup.geometry("300x150")
        popup.config(bg="#333")

        label = tk.Label(popup, text="Enter the rating (0-10):", bg="#333", fg="white",
                         font=("Bahnschrift", 11, "bold"))
        label.pack(pady=10)

        entry = tk.Entry(popup, bg="#444", fg="white")
        entry.pack(pady=10)

        center_popup(popup)

        button = tk.Button(popup, text="Rate", command=lambda: rate_film_action(entry.get()))
        button.pack(pady=10)

        entry.bind("<Return>", lambda event: rate_film_action(entry.get()))

        def rate_film_action(rating):
            try:
                if not rating:
                    raise exceptions.ScaleError("Rating cannot be empty!")
                rating = float(rating)
                if rating < 0 or rating > 10:
                    raise exceptions.ScaleError("Rating must be in range 0-10")
            except exceptions.ScaleError:
                for widget in popup.winfo_children():
                    if isinstance(widget, tk.Label) and widget.cget("fg") == "red":
                        widget.destroy()
                error_label = tk.Label(popup, text="Invalid rating! Please enter a number between 0 and 10.", bg="#333",
                                       fg="red")
                error_label.pack()
                return

            index = self.film_listbox.curselection()[0]
            film = film_collection.get_films()[index]
            film.set_rating(rating)
            popup.destroy()
            self.display_film_details()

    def add_comment(self):
        """
        This method is used to add a comment to a film.
        It opens a popup window where the user can enter the comment. If the comment is empty, an error message is
        displayed.
        """
        popup = tk.Toplevel()
        popup.title("Add comment")
        popup.geometry("300x150")
        popup.config(bg="#333")

        label = tk.Label(popup, text="Enter your comment:", bg="#333", fg="white", font=("Bahnschrift", 11, "bold"))
        label.pack(pady=10)

        entry = tk.Entry(popup, bg="#444", fg="white")
        entry.pack(pady=10)

        center_popup(popup)

        button = tk.Button(popup, text="Add", command=lambda: add_comment_action(entry.get()))
        button.pack(pady=10)

        entry.bind("<Return>", lambda event: add_comment_action(entry.get()))

        def add_comment_action(comment):
            if not comment:
                for widget in popup.winfo_children():
                    if isinstance(widget, tk.Label) and widget.cget("fg") == "red":
                        widget.destroy()
                error_label = tk.Label(popup, text="Comment cannot be empty!", bg="#333", fg="red")
                error_label.pack()
                return
            else:
                index = self.film_listbox.curselection()[0]
                film = film_collection.get_films()[index]
                film.add_comment(comment)
                popup.destroy()
                self.display_film_details()

    def show_only_watched(self, is_show_only_watched):
        """
        This method is used to filter the film listbox to show only watched films. It clears the listbox and populates
        it with the watched films. As watched_films is a set, the films are added to the listbox in the "random" order.

        Args:
            is_show_only_watched (bool): Whether to show only watched films.
        """
        if is_show_only_watched:
            # Clear the listbox
            self.film_listbox.delete(0, tk.END)

            already_added = []
            for film in film_collection.get_watched():
                if film.get_title() in already_added:
                    self.film_listbox.insert(tk.END, film.get_title() + " (" + str(film.get_year()) + ")")
                else:
                    self.film_listbox.insert(tk.END, film.get_title())
                    already_added.append(film.get_title())
        else:
            self.populate_film_list()

    def search_in_listbox(self, title, year):
        """
        This method is used to search for a film in the listbox.
        It is used when adding a new film and editing a film to highlight the newly added or edited film in the listbox.

        Args:
            title (str): The title of the film to search for.
            year (int): The year of the film to search for.
        """

        if not title:
            return
        for i, film in enumerate(film_collection.get_films()):
            if title.lower() in film.get_title().lower() and year == film.get_year():
                self.film_listbox.selection_clear(0, tk.END)
                self.film_listbox.selection_set(i)
                self.film_listbox.see(i)
                break

    def get_current_index(self):
        index = self.film_listbox.curselection()[0]
        self.current_film = index
        print(self.current_film)

    def set_default_color_on_select(self, event):
        """
        This method is used to set the default color of the selected item in the listbox. It helps un-highlight the
        found films when checking them out.

        Args:
            event (tkinter.Event): The event that triggered the method.
        """
        try:
            # Change the background color of the selected item to default
            index = event.widget.curselection()[0]
            event.widget.itemconfig(index, selectbackground="#555", selectforeground="white")
            event.widget.itemconfig(index, background="#444", foreground="white")
            self.display_film_details()
        except IndexError:
            pass


if __name__ == "__main__":
    root = tk.Tk()
    app = WatchlistApp(root)
    root.mainloop()
    file_operations.write_collection_to_json_file("films.json", film_collection)
    exit()
