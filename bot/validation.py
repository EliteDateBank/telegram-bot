import re

PHONE_RE = re.compile(r"^[0-9+()\-.\s]{6,}$")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def valid_phone(text: str) -> bool:
    return bool(PHONE_RE.match(text.strip()))

def valid_email(text: str) -> bool:
    return bool(EMAIL_RE.match(text.strip()))
