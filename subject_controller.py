import random
from services.store import load_all, save_all
from services.validators import is_valid_password


def subject_menu(current_student):
    while True:
        print("\nStudent Course Menu (c/e/r/s/x):", end=" ")
        choice = input().strip().lower()
        
        if choice == "c":
            change_password(current_student)
        elif choice == "e":
            enrol_subject(current_student)
        elif choice == "r":
            remove_subject(current_student)
        elif choice == "s":
            show_subjects(current_student)
        elif choice == "x":
            break
        else:
            print("Invalid option, try again.")


def enrol_subject(student):
    if len(student["subjects"]) >= 4:
        print("Students are allowed to enrol in 4 subjects only")
        return
    
    while True:
        subject_id = f"{random.randint(1, 999):03d}"
        if not any(s["id"] == subject_id for s in student["subjects"]):
            break
    
    
    if any(s["id"] == subject_id for s in student["subjects"]):
        print("Already enrolled in this subject")
        return
    
    mark = random.randint(25, 100)
    grade = calculate_grade(mark)
    
    student["subjects"].append({
        "id": subject_id,
        "mark": mark,
        "grade": grade
    })
    
    update_student_in_file(student)
    
    print(f"Enrolling in Subject-{subject_id}")
    print(f"You are now enrolled in {len(student['subjects'])} out of 4 subjects")


def remove_subject(student):
    if not student["subjects"]:
        print("No subjects to remove")
        return
    
    subject_id = input("Remove by ID: ").strip()
    
    original_count = len(student["subjects"])
    
    student["subjects"] = [s for s in student["subjects"] if s["id"] != subject_id]
    
    if len(student["subjects"]) == original_count:
        print("Subject not found in your enrolment")
        return
    
    update_student_in_file(student)
    
    print(f"Dropping Subject-{subject_id}")
    print(f"You are now enrolled in {len(student['subjects'])} out of 4 subjects")


def show_subjects(student):
    subjects = student["subjects"]
    print(f"Showing {len(subjects)} subjects")
    
    if len(subjects) == 0:
        return
    
    for subj in subjects:
        print(f"[ Subject::{subj['id']} -- mark = {subj['mark']} -- grade = {subj['grade']} ]")


def change_password(student):
    new_password = input("New Password: ").strip()
    confirm_password = input("Confirm Password: ").strip()
    
    if new_password != confirm_password:
        print("Password does not match - try again")
        return

    if not is_valid_password(new_password):
        print("Invalid password format. Must start with uppercase, at least 5 letters, and end with 3+ digits.")
        return
    

    student["password"] = new_password
    
    update_student_in_file(student)
    
    print("Password changed successfully")


def calculate_grade(mark):
    if mark >= 85:
        return "HD"
    elif mark >= 75:
        return "D"
    elif mark >= 65:
        return "C"
    elif mark >= 50:
        return "P"
    else:
        return "F"


def update_student_in_file(updated_student):
    students = load_all()
    
    for i, s in enumerate(students):
        if s["id"] == updated_student["id"]:
            students[i] = updated_student
            break

    save_all(students)