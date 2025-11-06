from services.store import load_all, save_all
from services.validators import is_valid_email, is_valid_password
from colorama import Fore, Style, init
init(autoreset=True)


def student_menu():
    while True:
        print(Fore.CYAN + Style.BRIGHT + "\nStudent System Menu")
        print("(R)Register   (L)Login   (X)Exit")

        choice = input(Fore.CYAN + "Select an option: ").strip().lower()

        if choice == "r":
            registerStudent()
        elif choice == "l":
            loginStudent()
        elif choice == "x":
            break
        else:
            print(Fore.RED + "Invalid option. Please try again.\n")


def registerStudent():
    print(Fore.CYAN + "\nStudent Registration")
    name = input(Fore.WHITE + "Name: ").strip()
    email = input(Fore.WHITE + "Email: ").strip()
    password = input(Fore.WHITE + "Password: ").strip()

    if not name or not email or not password:
        print(Fore.RED + "All fields are required.\n")
        return
    if not is_valid_email(email):
        print(Fore.RED + "Invalid email format. Must end with @university.com\n")
        return
    if not is_valid_password(password):
        print(Fore.RED + "Invalid password format. Must start with uppercase, have at least 5 letters, and end with 3+ digits.\n")
        return

    students = load_all()
    if any(s["email"] == email for s in students):
        print(Fore.RED + "Email already registered.\n")
        return

    new_id = str(len(students) + 1).zfill(6)

    students.append({
        "id": new_id,
        "name": name,
        "email": email,
        "password": password,
        "subjects": []
    })

    if save_all(students):
        print(Fore.GREEN + f"Registration successful. Your Student ID: {new_id}\n")
    else:
        print(Fore.RED + "Registration failed (file write error).\n")


def loginStudent():
    print(Fore.CYAN + "\nStudent Login")
    email = input(Fore.WHITE + "Email: ").strip()
    password = input(Fore.WHITE + "Password: ").strip()

    students = load_all()
    user = next((s for s in students if s["email"] == email and s["password"] == password), None)

    if user:
        print(Fore.GREEN + f"Login successful. Welcome, {user['name']}.\n")
        from controllers.subject_controller import subject_menu
        subject_menu(user)
    else:
        print(Fore.RED + "Invalid email or password. Please try again.\n")
