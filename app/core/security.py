from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

#use argon2 for password hashing
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

#password verification function
def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)

#create a JWT access token
def create_access_token(data: dict) -> str:
    payload = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)

    payload.update({"exp": expire})

    token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
    return token
