import tkinter as tk
from tkinter import messagebox

student_data = {
    "101" : {"password": "1234", "subjects" :{"Maths": "A", "English": "B+", "Sci": "A", "History":"B",}}
}

availaible_subjects = ["Maths", "English", "Science", "History", "Computer Science"]

# login Window
class loginWindow:
    def __init__(self,root):
        self.root = root
        self.root.title("UniAPP")
      
        tk.Label(root, text="StudentID:").grid(row=0,column=0,padx=11,pady=11)
        tk.Label(root, text="Password").grid(row=1,column=0,padx=11,pady=11)

        self.entry_ID = tk.Entry(root)
        self.entry_password = tk.Entry(root, show="*")

        self.entry_ID.grid(row=0, column=1, pady=11)
        self.entry_password.grid(row=1,column=1,padx=11,pady=11)

        tk.Button(root,text="login", command=self.login).grid(row=3,column=0,padx=11,pady=11)

    def login(self):
        stdID = self.entry_ID.get().strip()
        password = self.entry_password.get().strip()

        if not stdID or not password:
            messagebox.showerror("Error","Enter student ID and Password")
            return
        
        if stdID in student_data and student_data[stdID]["password"] == password:
            self.root.destroy()
            open_Enrollment_Window(stdID)
        else:
            messagebox.showerror("login failed", "Invalid Id and Password")


# Enrollment Window----------------\
class EnrollmntWindow:
    def __init__(self, root, stdID):
         self.root = root
         self.stdID = stdID
         self.root.title("Enrollmet of Subject")

         tk.Label(root, text=f"Welcome,{stdID}").grid(row=0, column=0,columnspan=2,pady=11)
         tk.Label(root, text="Select four subjects:").grid(row=1,column=0,sticky="w")

         self.subject_Var = {}
         row = 2
         for Subj in availaible_subjects:
             var = tk.IntVar()
             tk.Checkbutton(root, text=Subj, variable=var).grid(row=row, column=0, sticky="w")
             self.subject_Var[Subj] = var
             row += 1

         tk.Button(root, text='Enroll', command=self.enrol).grid(row=row, column=0, pady=11)
         tk.Button(root, text="Show Grade", command=self.checkGrades).grid(row=row, column=1, pady=11)

    def enrol(self):
        selected = [s for s, v in self.subject_Var.items() if v.get()==1]

        if not selected:
            messagebox.showerror("Error","Select subjects." )
            return
        
        if len(selected)>4:
            messagebox.showerror("Error", "You can enroll in upto four subjects only")
            return
        
        student_data[self.stdID]["Subjects"] = {s:"N/A" for s in selected}
        messagebox.showinfo("Success",f"Enroled in:{','.join(selected)}")
        

    def checkGrades(self):
        self.root.destroy()
        open_Grade_Window(self.stdID)


# Grade Window --------/
class GradeWindow:
    def __init__(self, root, stdID):
        self.root = root
        self.stdID = stdID
        self.root.title ("Grade Window")

        tk.Label(root, text=f"Grades for{stdID} ").grid(row=0, column=0, columnspan=3,pady=10)

        tk.Label(root,text="Subjects").grid(row=1,column=0,padx=11)
        tk.Label(root,text="Grade").grid(row=1,column=1,padx=11)

        subjects = student_data[self.stdID]["subjects"]
        row = 2
        for Subj, grade in subjects.item():
            tk.Label(root,text=Subj).grid(row=row, column=0, padx=11)
            tk.Label(root,text=grade).grid(row=row, column=1, padx=11)
            row += 1


def open_Enrollment_Window(stdID):
    root = tk.Tk()
    EnrollmntWindow(root,stdID)
    root.mainloop()

def open_Grade_Window(sid):
    root = tk.Tk()
    GradeWindow(root, sid)
    root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    loginWindow(root)
    root.mainloop()
    