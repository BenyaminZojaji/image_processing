import hashlib

def encode(password):
    password = password.encode()
    hash = hashlib.sha256(password).hexdigest()
    return hash