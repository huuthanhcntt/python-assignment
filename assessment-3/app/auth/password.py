import hashlib
import bcrypt

def hash_password(password: str) -> bytes:
    prehashed = hashlib.sha256(password.encode("utf-8")).digest()
    return bcrypt.hashpw(prehashed, bcrypt.gensalt()).decode("utf-8")

def verify_password(password: str, hashed: bytes) -> bool:
    prehashed = hashlib.sha256(password.encode("utf-8")).digest()
    return bcrypt.checkpw(prehashed, hashed.encode("utf-8"))
