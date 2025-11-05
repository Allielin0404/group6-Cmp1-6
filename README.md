# University CLI & GUI Application

---

## Table of Contents
- [Project Overview](#project-overview)
- [User Roles](#user-roles)
- [System Requirements](#system-requirements)
- [Installation & Setup Instructions](#installation--setup-instructions)
- [Team Members](#team-members)
- [File Structure](#file-structure)
- [How to Run](#how-to-run)
- [Test](#test)
- [Usage Example](#usage-example)
- [Example Data](#example-data)

---

## Project Overview
This project is a Python-based university enrolment system that provides both a Command-Line Interface (CLI) and a Graphical User Interface (GUI).  

Students can register, log in, manage their accounts, and enrol or remove subjects.  
Administrators can manage and maintain student data records through various functions.

---

## User Roles

### Student
- **R** - Register
- **L** - Login
   - **C** - Change password
   - **E** - Enrol a subject
   - **R** - Remove a subject
   - **S** - Show all enrolled subjects

### Administrator
- **C** - Clear all student data
- **G** - Group students by grade
- **P** - Categorise students into PASS/FAIL
- **R** - Remove a specific student
- **S** - Show list of all students

## System Requirements
- **Python version:** 3.13 or above  
- **Operating System:** Windows, macOS, or Linux  
- **Libraries** json, tkinter, random, colorama

## Installation & Setup Instructions
1. Clone or download the project zip file and extract it to any local directory.  
2. Ensure all `.py` files and `students.data` are in the same folder.  
   *(If `students.data` does not exist, it will be created automatically.)*
3. Open the folder in **VS Code**, **PyCharm**, or **IDLE**.
4. Ensure Python 3.13 (or newer) and libraries are installed.  
5. Open a terminal in the project directory.  
6. Run the CLI version:
   `python main.py`
7. Run the GUI version:
   `python gui.py`

---

## Our 4 Team Members
| NAME | SID | Contribution |
|:----:|:----:|:----|
|Shelly|25725906|Main Menu & Student Register/Login & Documentation|
|Allie|26061085|Subject Enrolment System|
|Rainy|26024354|Admin System|
|Zoeb|25613720|GUI System|


## File Structure
```
UniApp_CLI/
│
├── main.py                           # Main CLI entry point (University System)
├── student_controller.py             # Handles Student's operations
├── subject_controller.py             # 
├── admin_controller                  # Handles Admin's operations
├── admin_system.py                   # 
├── admin_system_implementation.py    # 
│
├── services/                         # Service layer for data and validation
│   ├── store.py                      # Handles read/write operations for students.data
│   └── validators.py                 # Regex input validation (email, password rules)
│
├── gui.py                            # Tkinter-based GUI
│
├── students.data                     # Shared JSON data file (auto-created)
│
└── README.md                         # Project documentation
```

---

## How to Run
**CLI**
`python main.py`  
**GUI**
`python gui.py`

## How to Test
|Test|Description|Expected Result|
|:---:|:---:|:---|
|1| Register new student | New record saved to students.data; valid regex check |
|2| Login with invalid password | Error message displayed without crash |
|3| Enrol in a subject (≤ 4) | Random mark and grade generated and saved |
|4| Try enrolling a 5th subject | Error message shown |
|5| Admin → Show students | Displays all students with subjects, marks and grades |
|6| Admin → Group by grade | Lists students in Z/P/C/D/HD categories |
|7| Admin → Clear database | Deletes all records after confirmation |

## How to Use

**Student Menu**
```
(l) login
(r) register
(x) exit
```

**After successful login**
```
(c) change password
(e) enrol subject
(r) remove subject
(s) show subjects
(x) exit
```

**Admin Menu**
```
(s) show students
(g) group students by grade
(p) partition PASS/FAIL
(r) remove a student
(c) clear all data
(x) exit
```
**Configurations**
- **Data File** -> `students.data`  
  Stores all registered students and enrolment records in JSON format.  
- **Regex Validation Rules**  
  - Email must end with `@university.com`  
  - Password must start with an uppercase letter, include ≥ 5 letters and ≥ 3 digits  
- **Auto-Generation**  
  - Student ID → 6-digit unique number (000001–999999)  
  - Subject ID → 3-digit unique number (001–999)  
  - Marks → random 25–100; grades assigned Z / P / C / D / HD

## Example data
```
[
  {
    "id": "000001",
    "name": "test",
    "email": "Test@university.com",
    "password": "Qwert123",
    "subjects": [
      {
        "id": "858",
        "mark": 49,
        "grade": "F"
      }
    ]
  }
]
```
