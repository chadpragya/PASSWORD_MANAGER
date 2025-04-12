import hashlib
import base64
from cryptography.fernet import Fernet

def generate_encryption_key(master_password, salt):
    key = hashlib.pbkdf2_hmac(
        'sha256',
        master_password.encode(),
        salt.encode(),
        100000
    )
    return base64.urlsafe_b64encode(key)

def get_cipher(master_password, salt):
    key = generate_encryption_key(master_password, salt)
    return Fernet(key)
