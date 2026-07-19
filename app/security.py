from fastapi import HTTPException
from pwdlib import PasswordHash
from jose import JWTError , jwt
from app.config.app_config import getApp_config
from datetime import datetime , timedelta , timezone


def hashPassword(password : str) -> str :
    password_hash = PasswordHash.recommended()
    return password_hash.hash(password)

def verifyPassword(password : str , hashed_pass : str) -> bool:
    password_hash = PasswordHash.recommended()
    return password_hash.verify(password , hashed_pass)

def create_AcessToken(data : dict) -> str:
    config = getApp_config()
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=config.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, config.secret_key, algorithm=config.algorithm)

def verifyToken(token:str):
    config = getApp_config()
    try:
        payload = jwt.decode(token, config.secret_key, algorithms=[config.algorithm])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")