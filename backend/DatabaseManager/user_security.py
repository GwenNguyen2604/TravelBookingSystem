import os, hashlib, base64

def hash_password(password):
    salt = os.urandom(16)
    hash_bytes = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
    return base64.b64encode(salt + hash_bytes).decode()

def verify_password(stored, password):
    stored = base64.b64decode(stored.encode())
    salt, hash_bytes = stored[:16], stored[16:]
    new_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
    return new_hash == hash_bytes