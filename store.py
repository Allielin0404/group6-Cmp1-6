import json
from pathlib import Path

DATA_FILE = Path("students.data")

def ensure_file():
    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]", encoding="utf-8")

'''read student data'''
def load_all():
    ensure_file()
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except Exception as e:
        print("[error] read failed:", e)
        return []

'''rewrite and save, return Ture'''
def save_all(students):
    try:
        DATA_FILE.write_text(
            json.dumps(students, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        return True
    except Exception as e:
        print("[error] write failed:", e)
        return False