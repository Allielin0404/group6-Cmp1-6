import re

# email rule: must end of @university.com 
EMAIL_PATTERN = r"^[a-zA-Z0-9._%+-]+@university\.com$"

# password rule: start with uppercase, at least 5 characters and at least 3 numbers
PASSWORD_PATTERN = r"^[A-Z][A-Za-z]{4,}\d{3,}$"

def is_valid_email(email):
    return re.match(EMAIL_PATTERN, email) is not None

def is_valid_password(password):
    return re.match(PASSWORD_PATTERN, password) is not None
