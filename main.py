from controllers.student_controller import student_menu
from controllers.admin_controller import admin_menu
from colorama import Fore, Style, init

init(autoreset=True)

def main_menu():
    # Main menu
    while True:
        print(Fore.CYAN + Style.BRIGHT + "\nUniversity System Menu")
        print(Fore.WHITE + "(A)Admin   (S)Student   (X)Exit")

        choice = input(Fore.CYAN + "Select an option: ").strip().lower()
        
        # Handle choices
        if choice == "a":
            admin_menu()
        elif choice == "s":
            student_menu()
        elif choice == "x":
            print(Fore.MAGENTA + "Goodbye my friend. See you next time.")
            break
        else:
            print(Fore.RED + "Invalid option. Please try again.\n")


if __name__ == "__main__":
    main_menu()
