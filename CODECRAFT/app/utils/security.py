import hashlib
import os
import secrets

def generate_salt():
    return secrets.token_hex(16)

def hash_password(password, salt):
    return hashlib.sha256((password + salt).encode()).hexdigest()

def validate_password(password):
    if len(password) < 6:
        return False
    return True