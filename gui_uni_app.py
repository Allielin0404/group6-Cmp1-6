import json
import os
import re
import random
import tkinter as tk
from tkinter import ttk, messagebox

# ----------------------------------------------------------------------
# Fallback storage/validators (GUI built-ins)
# ----------------------------------------------------------------------

DATA_FILE = "students.data"

def _fallback_load_all():
    """Fallback: read students from a JSON array file."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            if isinstance(data, dict) and "students" in data:
                return data["students"]
            return []
    except Exception:
        return []

def _fallback_save_all(students):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(students, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False

def _fallback_is_valid_email(email: str) -> bool:
    pat = re.compile(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
    return bool(pat.fullmatch((email or "").strip()))

def _fallback_is_valid_password(pw: str) -> bool:
    pw = (pw or "")
    if len(pw) < 8:
        return False
    has_lower = any(c.islower() for c in pw)
    has_upper = any(c.isupper() for c in pw)
    has_digit = any(c.isdigit() for c in pw)
    specials = r"!@#$%^&*()_+-=[]{}|;':\",.<>/?`~"
    has_special = any(c in specials for c in pw)
    if any(c.isspace() for c in pw):
        return False
    return has_lower and has_upper and has_digit and has_special

# ----------------------------------------------------------------------
# STORAGE & VALIDATORS (force GUI’s own so it’s deterministic)
# ----------------------------------------------------------------------

# Always use local JSON file in this folder, ignore project services.store
LOAD_ALL = _fallback_load_all
SAVE_ALL = _fallback_save_all

# Always use these simple validators
IS_VALID_EMAIL = _fallback_is_valid_email
IS_VALID_PASSWORD = _fallback_is_valid_password

# ----------------------------------------------------------------------
# Shared helpers (aligned with Members A/B/C)
# ----------------------------------------------------------------------

def grade_from_mark(mark: int) -> str:
    if mark >= 85: return "HD"
    if mark >= 75: return "D"
    if mark >= 65: return "C"
    if mark >= 50: return "P"
    return "F"

def compute_avg(student: dict):
    subs = student.get("subjects") or []
    if not subs:
        student["avg"] = None
        return None
    avg = sum(int(s.get("mark", 0)) for s in subs) / len(subs)
    student["avg"] = avg
    return avg

def next_student_id(students: list) -> str:
    nums = []
    for s in students:
        sid = str(s.get("id", "")).strip()
        if sid.isdigit():
            nums.append(int(sid))
    return str((max(nums) + 1) if nums else 1).zfill(6)

def next_subject_id(student: dict) -> str:
    existing = {str(s.get("id")).zfill(3) for s in (student.get("subjects") or [])}
    while True:
        sid = f"{random.randint(1, 999):03d}"
        if sid not in existing:
            return sid

def find_student_by_email(students: list, email: str):
    email = (email or "").strip().lower()
    for s in students:
        if str(s.get("email", "")).strip().lower() == email:
            return s
    return None

def update_student(students: list, updated: dict):
    for i, s in enumerate(students):
        if str(s.get("id")) == str(updated.get("id")):
            students[i] = updated
            return True
    students.append(updated)
    return True

def _abs_data_path():
    try:
        return os.path.abspath(DATA_FILE)
    except Exception:
        return DATA_FILE

# ----------------------------------------------------------------------
# Tkinter App
# ----------------------------------------------------------------------

class GUIUniApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GUIUniApp - Student Enrolment System")
        self.geometry("780x560")
        self.resizable(False, False)

        self.current_user = None  # dict

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (LoginFrame, RegisterFrame, DashboardFrame):
            frame = F(parent=container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginFrame")

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show()

    # --------- Auth ops ---------
    def login(self, email: str, password: str):
        if not email or not password:
            messagebox.showwarning("Missing", "Please enter email and password")
            return

        students = LOAD_ALL() or []
        user = find_student_by_email(students, email)
        if user and str(user.get("password")) == str(password):
            self.current_user = user
            self.show_frame("DashboardFrame")
        else:
            messagebox.showerror("Login Failed", "Invalid email or password")

    def register(self, name: str, email: str, password: str, confirm: str):
        import traceback
        try:
            name = (name or "").strip()
            email = (email or "").strip().lower()

            # validations
            if not name or not email or not password or not confirm:
                messagebox.showwarning("Missing", "All fields are required"); return
            if not IS_VALID_EMAIL(email):
                messagebox.showerror("Invalid", "Invalid email format"); return
            if not IS_VALID_PASSWORD(password):
                messagebox.showerror("Invalid", "Password must be 8+ chars with upper, lower, digit, special"); return
            if password != confirm:
                messagebox.showerror("Mismatch", "Password and confirm do not match"); return

            # load + duplicate check
            students = LOAD_ALL() or []
            if find_student_by_email(students, email):
                messagebox.showerror("Exists", "Email already registered"); return

            # create + save
            sid = next_student_id(students)
            students.append({
                "id": sid, "name": name, "email": email,
                "password": password, "subjects": [], "avg": None
            })

            ok = SAVE_ALL(students)
            if ok is False:
                messagebox.showerror("Error", "Could not save user (write error)."); return

            messagebox.showinfo("Success", f"Registered. Your ID is {sid}\nSaved to: {os.path.abspath(DATA_FILE)}")
            self.show_frame("LoginFrame")

        except Exception as e:
            traceback.print_exc()
            messagebox.showerror("Unexpected error", f"{e.__class__.__name__}: {e}")

    def logout(self):
        self.current_user = None
        self.show_frame("LoginFrame")

    # --------- Subject ops ---------
    def enrol_subject(self):
        if not self.current_user:
            return
        subs = self.current_user.get("subjects") or []
        if len(subs) >= 4:
            messagebox.showinfo("Limit", "Students are allowed to enrol in 4 subjects only")
            return
        sid = next_subject_id(self.current_user)
        mark = random.randint(25, 100)
        grade = grade_from_mark(mark)
        subs.append({"id": sid, "mark": int(mark), "grade": grade})
        self.current_user["subjects"] = subs
        compute_avg(self.current_user)
        if self._persist_current_user():
            dash = self.frames["DashboardFrame"]
            dash.refresh_table()
            messagebox.showinfo("Enrolled", f"Enrolled in Subject-{sid}")
        else:
            messagebox.showerror("Error", "Could not save enrolment.")

    def remove_subject(self, subject_id: str):
        if not self.current_user:
            return
        subs = self.current_user.get("subjects") or []
        before = len(subs)
        subs = [s for s in subs if str(s.get("id")) != str(subject_id)]
        if len(subs) == before:
            messagebox.showwarning("Not found", "Subject not found in your enrolment")
            return
        self.current_user["subjects"] = subs
        compute_avg(self.current_user)
        if self._persist_current_user():
            dash = self.frames["DashboardFrame"]
            dash.refresh_table()
            messagebox.showinfo("Removed", f"Dropped Subject-{subject_id}")
        else:
            messagebox.showerror("Error", "Could not save changes.")

    def change_password(self, new_pw: str, confirm_pw: str):
        if not self.current_user:
            return
        if new_pw != confirm_pw:
            messagebox.showerror("Mismatch", "Passwords do not match")
            return
        if new_pw == str(self.current_user.get("password")):
            messagebox.showwarning("No change", "New password must differ from current password")
            return
        if not IS_VALID_PASSWORD(new_pw):
            messagebox.showerror("Invalid", "Password must be 8+ chars with upper, lower, digit, special")
            return
        self.current_user["password"] = new_pw
        if self._persist_current_user():
            messagebox.showinfo("Success", "Password changed successfully")
        else:
            messagebox.showerror("Error", "Could not save password change.")

    def _persist_current_user(self) -> bool:
        students = LOAD_ALL() or []
        update_student(students, self.current_user)
        ok = SAVE_ALL(students)
        return ok is not False

# ----------------------------------------------------------------------
# Frames
# ----------------------------------------------------------------------

class LoginFrame(ttk.Frame):
    def __init__(self, parent, controller: GUIUniApp):
        super().__init__(parent)
        self.controller = controller

        title = ttk.Label(self, text="GUIUniApp", font=("Segoe UI", 18, "bold"))
        subtitle = ttk.Label(self, text="Login to your account", font=("Segoe UI", 10))

        self.email_var = tk.StringVar()
        self.pw_var = tk.StringVar()

        email_lbl = ttk.Label(self, text="Email")
        email_ent = ttk.Entry(self, textvariable=self.email_var, width=40)
        pw_lbl = ttk.Label(self, text="Password")
        pw_ent = ttk.Entry(self, textvariable=self.pw_var, width=40, show="*")

        login_btn = ttk.Button(self, text="Login", command=lambda: controller.login(self.email_var.get(), self.pw_var.get()))
        to_reg_btn = ttk.Button(self, text="Create account", command=lambda: controller.show_frame("RegisterFrame"))

        title.pack(pady=(40, 4))
        subtitle.pack(pady=(0, 20))
        email_lbl.pack(anchor="w", padx=40)
        email_ent.pack(padx=40, pady=4)
        pw_lbl.pack(anchor="w", padx=40, pady=(8,0))
        pw_ent.pack(padx=40, pady=4)
        login_btn.pack(pady=16)
        to_reg_btn.pack()

    def on_show(self):
        self.email_var.set("")
        self.pw_var.set("")

class RegisterFrame(ttk.Frame):
    def __init__(self, parent, controller: GUIUniApp):
        super().__init__(parent)
        self.controller = controller
        title = ttk.Label(self, text="Create your account", font=("Segoe UI", 16, "bold"))

        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.pw_var = tk.StringVar()
        self.confirm_var = tk.StringVar()

        name_lbl = ttk.Label(self, text="Full name")
        name_ent = ttk.Entry(self, textvariable=self.name_var, width=40)
        email_lbl = ttk.Label(self, text="Email")
        email_ent = ttk.Entry(self, textvariable=self.email_var, width=40)
        pw_lbl = ttk.Label(self, text="Password")
        pw_ent = ttk.Entry(self, textvariable=self.pw_var, width=40, show="*")
        c_lbl = ttk.Label(self, text="Confirm Password")
        c_ent = ttk.Entry(self, textvariable=self.confirm_var, width=40, show="*")

        create_btn = ttk.Button(self, text="Create Account",
                                command=lambda: controller.register(self.name_var.get(), self.email_var.get(),
                                                                    self.pw_var.get(), self.confirm_var.get()))
        back_btn = ttk.Button(self, text="Back to Login", command=lambda: controller.show_frame("LoginFrame"))

        title.pack(pady=(30, 18))
        for w in [
            (name_lbl, {"anchor":"w","padx":40}), (name_ent, {"padx":40,"pady":4}),
            (email_lbl, {"anchor":"w","padx":40}), (email_ent, {"padx":40,"pady":4}),
            (pw_lbl, {"anchor":"w","padx":40}), (pw_ent, {"padx":40,"pady":4}),
            (c_lbl, {"anchor":"w","padx":40}), (c_ent, {"padx":40,"pady":4}),
        ]:
            w[0].pack(**w[1])
        create_btn.pack(pady=16)
        back_btn.pack()

    def on_show(self):
        self.name_var.set("")
        self.email_var.set("")
        self.pw_var.set("")
        self.confirm_var.set("")

class DashboardFrame(ttk.Frame):
    def __init__(self, parent, controller: GUIUniApp):
        super().__init__(parent)
        self.controller = controller

        header = ttk.Frame(self)
        header.pack(fill="x", pady=(12,4))

        self.welcome_lbl = ttk.Label(header, text="Welcome", font=("Segoe UI", 14, "bold"))
        self.welcome_lbl.pack(side="left", padx=12)

        self.avg_lbl = ttk.Label(header, text="Average: -")
        self.avg_lbl.pack(side="left", padx=12)

        logout_btn = ttk.Button(header, text="Logout", command=controller.logout)
        logout_btn.pack(side="right", padx=12)

        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=12, pady=8)

        self.tree = ttk.Treeview(table_frame, columns=("id","mark","grade"), show="headings", height=12)
        self.tree.heading("id", text="Subject ID")
        self.tree.heading("mark", text="Mark")
        self.tree.heading("grade", text="Grade")
        self.tree.column("id", width=100, anchor="center")
        self.tree.column("mark", width=80, anchor="center")
        self.tree.column("grade", width=80, anchor="center")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        actions = ttk.LabelFrame(self, text="Actions")
        actions.pack(fill="x", padx=12, pady=8)

        enrol_btn = ttk.Button(actions, text="Enrol Random Subject", command=controller.enrol_subject)
        remove_lbl = ttk.Label(actions, text="Remove by Subject ID:")
        self.remove_var = tk.StringVar()
        remove_ent = ttk.Entry(actions, textvariable=self.remove_var, width=8)
        remove_btn = ttk.Button(actions, text="Remove", command=self._remove_selected)

        pw_lbl = ttk.Label(actions, text="Change Password:")
        self.new_pw_var = tk.StringVar()
        self.confirm_pw_var = tk.StringVar()
        new_pw_ent = ttk.Entry(actions, textvariable=self.new_pw_var, width=20, show="*")
        confirm_pw_ent = ttk.Entry(actions, textvariable=self.confirm_pw_var, width=20, show="*")
        pw_btn = ttk.Button(actions, text="Update Password", command=self._change_pw)

        enrol_btn.grid(row=0, column=0, padx=8, pady=8, sticky="w")
        remove_lbl.grid(row=0, column=1, padx=(16,4), pady=8, sticky="e")
        remove_ent.grid(row=0, column=2, padx=4, pady=8, sticky="w")
        remove_btn.grid(row=0, column=3, padx=4, pady=8, sticky="w")

        pw_lbl.grid(row=1, column=0, padx=8, pady=8, sticky="w")
        new_pw_ent.grid(row=1, column=1, padx=4, pady=8, sticky="w")
        confirm_pw_ent.grid(row=1, column=2, padx=4, pady=8, sticky="w")
        pw_btn.grid(row=1, column=3, padx=4, pady=8, sticky="w")

        tip = ttk.Label(self, text="Tip: max 4 subjects. Marks are assigned automatically on enrol; grade is computed.", foreground="gray")
        tip.pack(padx=12, pady=(0,12), anchor="w")

    def on_show(self):
        user = self.controller.current_user or {}
        self.welcome_lbl.config(text=f"Welcome, {user.get('name','Student')} (ID: {user.get('id','-')})")
        self.refresh_table()

    def refresh_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        user = self.controller.current_user or {}
        subs = user.get("subjects") or []
        for s in subs:
            self.tree.insert("", "end", values=(s.get("id"), s.get("mark"), s.get("grade")))
        avg = user.get("avg")
        if avg is None:
            avg = compute_avg(user)
            self.controller._persist_current_user()
        self.avg_lbl.config(text=f"Average: {('-' if avg is None else f'{avg:.2f}') }")

    def _remove_selected(self):
        sid = self.remove_var.get().strip()
        if not sid:
            cur = self.tree.focus()
            if cur:
                vals = self.tree.item(cur, "values")
                if vals:
                    sid = vals[0]
        if not sid:
            messagebox.showwarning("Missing", "Enter or select a Subject ID to remove")
            return
        self.controller.remove_subject(sid)
        self.remove_var.set("")

    def _change_pw(self):
        self.controller.change_password(self.new_pw_var.get(), self.confirm_pw_var.get())
        self.new_pw_var.set("")
        self.confirm_pw_var.set("")

def main():
    app = GUIUniApp()
    app.mainloop()

if __name__ == "__main__":
    main()
