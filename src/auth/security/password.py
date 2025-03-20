import hashlib


def hash_password(password: str) -> str:
    hasher = hashlib.md5(bytes(password, "utf-8"))
    hashed_password = hasher.hexdigest()
    return hashed_password


def check_password(password: str, password_in_db: str) -> bool:
    hashed_password = hash_password(password)
    return hashed_password == password_in_db
