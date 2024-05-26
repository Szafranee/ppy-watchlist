import collection_manager

def print_main_menu():
    print("============================================================")
    print("Welcome to the Film Collection Manager!")
    print("============================================================")
    print()
    print("=== Main Menu ===")
    print("Select an option:")
    print("1. Show your films")
    print("2. Add a new film")
    print("3. Search for a film")
    print("4. Generate statistics")
    print("5. Export your collection to a file")
    print("6. Exit")
    print("=================")


def print_search_menu():
    print("=== Search Menu ===")
    print("Select a search criterion:")
    print("1. Title")
    print("2. Director")
    print("3. Year")
    print("4. Genre")
    print("5. Rating")
    print("6. Watch status")
    print("7. Comments")
    print("8. Watched on")
    print("9. Go back")
    print("===================")


def print_stats_menu():
    print("=== Generate statistics ===")
    print("Select a statistic:")
    print("1. Average rating")
    print("2. Watched films by genre")
    print("3. Number of rated films by genre")
    print("4. Average length of films by genre")
    print("5. All statistics")
    print("6. Go back")
    print("===========================")


def print_export_menu():
    print("=== Export to file ===")
    print("1. Select a name for the file")
    print("2. Go back")
    print("=======================")


def print_films_action_menu():
    print("=== Films Menu ===")
    print("Select an action:")
    print("1. Watch film")
    print("2. Add comment")
    print("3. Delete comment")
    print("4. Delete film")
    print("5. Go back")
    print("==================")


def handle_films_action_menu(user_input, collection_manager):
    if user_input == "1":
        collection_manager.watch_film()
    elif user_input == "2":
        collection_manager.add_comment()
    elif user_input == "3":
        collection_manager.delete_comment()
    elif user_input == "4":
        collection_manager.delete_film()
    elif user_input == "5":
        return
    else:
        print("Invalid input. Please try again.")

def main_menu(collection_manager):
    while True:
        print_main_menu()
        user_input = input("Enter your choice: ")
        if user_input == "1":
            print(collection_manager)
            print()
            print_films_action_menu()
            user_input = input("Enter your choice: ")
            handle_films_action_menu(user_input, collection_manager)
        elif user_input == "2":

        elif user_input == "3":

        elif user_input == "4":

        elif user_input == "5":

        elif user_input == "6":
            break
        else:
            print("Invalid input. Please try again.")