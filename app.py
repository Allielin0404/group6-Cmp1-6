from student_controller import student_menu
from admin_controller import admin_menu

def main_menu():
    while True:
        print("\n─═=═─‧─═=═─‧─═=═─‧─═=═─‧─═=═─")
        print("::::: University System :::::")
        print("─═=═─‧─═=═─‧─═=═─‧─═=═─‧─═=═─")
        print("\n(A) Admin")
        print("(S) Student")
        print("(X) Exit")
        choice = input("University System: (A)Admin, (S)Student, or X : ").strip().lower()
        
        if choice == "a":
            admin_menu()
        elif choice == "s":
            student_menu()
        elif choice == "x":
            print("Goodbye My Friend! See You Next Time :)")
            break
        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    main_menu()