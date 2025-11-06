from student_controller import student_menu
from admin_controller import admin_menu
from colorama import Fore, Style, init

init(autoreset=True)

def main_menu():
    # Main menu
    while True:
        choice = input(Fore.CYAN + Style.BRIGHT + "\nUniversity System Menu: (A)dmin (S)tudent or X: ", end=" ").strip().lower()
        
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
