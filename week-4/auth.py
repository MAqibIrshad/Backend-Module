from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os
from config import settings
load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hashPassword(plain_password:str)->str:
    return password_context.hash(plain_password)

def verifyPassword(plain_password:str, hash_password:str)->bool:
    return password_context.verify(plain_password, hash_password)

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        settings.ALGORITHM
    )

    return encoded_jwt


from fastapi import Depends, HTTPException
from jose import JWTError

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return username

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )