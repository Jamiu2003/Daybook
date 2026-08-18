from pwdlib import PasswordHash
import jwt
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
load_dotenv()

secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")


password_hash = PasswordHash.recommended()

def hash_password(password:str):
    return password_hash.hash(password)

def verify_password(password:str, hashed_password:str) -> bool:
    return password_hash.verify(password, hashed_password)

def create_access_token(username:str):
    expires = datetime.now(timezone.utc) + timedelta(minutes=30)
    payload = {
        "sub": username,
        "exp": expires
    }
    return jwt.encode(payload, secret_key, algorithm)

def decode_access_token(token:str):
    try:
        payload = jwt.decode(
            token,
            secret_key,
            algorithm
        )
        return payload
    except jwt.InvalidTokenError:
        return None