from services.store import load_all, save_all


def admin_menu():
    """Admin System menu"""
    while True:
        print("\nAdmin System (c/g/p/r/s/x): ", end="")
        choice = input().strip().lower()
        
        if choice == "c":
            clear_database()
        elif choice == "g":
            group_students()
        elif choice == "p":
            partition_students()
        elif choice == "r":
            remove_student()
        elif choice == "s":
            show_all_students()
        elif choice == "x":
            break
        else:
            print("Invalid option, try again.")


def show_all_students():
    """Show all students"""
    students = load_all()
    
    if not students:
        print("< Nothing to Display >")
        return
    
    print("Student List")
    for student in students:
        print(f"{student['name']} :: {student['id']} --> Email: {student['email']}")


def group_students():
    """Group students by grade"""
    students = load_all()
    
    if not students:
        print("< Nothing to Display >")
        return
    
    # Create grade groups
    grade_groups = {
        "HD": [],
        "D": [],
        "C": [],
        "P": [],
        "F": []
    }
    
    # Group students by average grade
    for student in students:
        if student["subjects"]:
            avg_mark = calculate_average(student["subjects"])
            grade = get_grade_from_average(avg_mark)
            grade_groups[grade].append(student)
    
    # Display grouped students
    print("Grade Grouping")
    for grade in ["HD", "D", "C", "P", "F"]:
        if grade_groups[grade]:
            print(f"{grade} --> ", end="")
            for student in grade_groups[grade]:
                avg_mark = calculate_average(student["subjects"])
                print(f"[{student['name']} :: {student['id']} --> GRADE: {grade} - MARK: {avg_mark:.2f}]", end=" ")
            print()


def partition_students():
    """Partition students into PASS/FAIL"""
    students = load_all()
    
    if not students:
        print("< Nothing to Display >")
        return
    
    pass_students = []
    fail_students = []
    
    # Partition based on average mark >= 50
    for student in students:
        if student["subjects"]:
            avg_mark = calculate_average(student["subjects"])
            if avg_mark >= 50:
                pass_students.append(student)
            else:
                fail_students.append(student)
    
    # Display FAIL
    if fail_students:
        print("FAIL --> ", end="")
        for student in fail_students:
            avg_mark = calculate_average(student["subjects"])
            grade = get_grade_from_average(avg_mark)
            print(f"[{student['name']} :: {student['id']} --> GRADE: {grade} - MARK: {avg_mark:.2f}]", end=" ")
        print()
    else:
        print("FAIL --> []")
    
    # Display PASS
    if pass_students:
        print("PASS --> ", end="")
        for student in pass_students:
            avg_mark = calculate_average(student["subjects"])
            grade = get_grade_from_average(avg_mark)
            print(f"[{student['name']} :: {student['id']} --> GRADE: {grade} - MARK: {avg_mark:.2f}]", end=" ")
        print()
    else:
        print("PASS --> []")


def remove_student():
    """Remove a student by ID"""
    students = load_all()
    
    if not students:
        print("< Nothing to Display >")
        return
    
    student_id = input("Remove by ID: ").strip()
    
    # Find and remove student
    updated_students = []
    found = False
    
    for student in students:
        if student["id"] == student_id:
            found = True
            print(f"Removing Student {student_id} Account")
        else:
            updated_students.append(student)
    
    if not found:
        print(f"Student {student_id} does not exist")
        return
    
    # Save updated list
    save_all(updated_students)


def clear_database():
    """Clear all students from database"""
    students = load_all()
    
    if not students:
        print("< Nothing to Display >")
        return
    
    print("Clearing students database")
    confirm = input("Are you sure you want to clear the database (Y)ES / (N)O: ").strip().lower()
    
    if confirm == "y":
        save_all([])
        print("Students data cleared")
    else:
        print("Cancelled.")


def calculate_average(subjects):
    """Calculate average mark from subjects"""
    if not subjects:
        return 0
    total = sum(s["mark"] for s in subjects)
    return total / len(subjects)


def get_grade_from_average(avg_mark):
    """Get grade from average mark"""
    if avg_mark >= 85:
        return "HD"
    elif avg_mark >= 75:
        return "D"
    elif avg_mark >= 65:
        return "C"
    elif avg_mark >= 50:
        return "P"
    else:
        return "F"