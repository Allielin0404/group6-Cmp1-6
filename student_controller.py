from services.store import load_all, save_all
from services.validators import is_valid_email, is_valid_password


def student_menu():
    while True:
        print("\n-----================-----")
        print("::::: Student System :::::")
        print("-----================-----")
        print("\n(R) Register")
        print("(L) Login")
        print("(X) Back")
        choice = input("Student System (l/r/x): ").strip().lower()

        if choice == "r":
            registerStudent()
        elif choice == "l":
            loginStudent()
        elif choice == "x":
            break
        else:
            print("Invalid option, try again.")


def registerStudent():
    name = input("Name: ").strip()
    email = input("Email: ").strip()
    password = input("Password: ").strip()

    if not name or not email or not password:
        print("All fields are required.")
        return
    if not is_valid_email(email):
        print("Invalid email format. Must end with @university.com")
        return
    if not is_valid_password(password):
        print("Invalid password format. Must start with uppercase, at least 5 letters, and end with 3+ digits.")
        return

    students = load_all()
    if any(s["email"] == email for s in students):
        print("Email already registered.")
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
        print(f"Register success. Your ID: {new_id}")
    else:
        print("Register failed (write error).")


def loginStudent():
    email = input("Email: ").strip()
    password = input("Password: ").strip()

    students = load_all()
    user = next((s for s in students if s["email"] == email and s["password"] == password), None)

    if user:
        print(f"Login success! Welcome, {user['name']}")
        from subject_controller import subject_menu
        subject_menu(user)
    else:
        print("Invalid email or password.")