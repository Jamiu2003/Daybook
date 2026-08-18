from database import get_db
from security import create_access_token, decode_access_token, hash_password, verify_password
from model import User
from fastapi import Depends, HTTPException
from sqlalchemy import Select
from sqlalchemy.orm import Session
from database import SessionLocal
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
def get_current_user(token:str = Depends(oauth2_scheme), db:Session = Depends(get_db),):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid Token or expired token")
    username = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=401, detail = "User Not Found")
        return user
    finally:
        db.close()
