import hashlib, os, base64

def derive_key(password: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac(
        'sha256',
        password.encode(),
        salt,
        200000,
        dklen=32
    )

def generate_salt() -> bytes:
    return os.urandom(16)
