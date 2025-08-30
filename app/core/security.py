from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_token(subject: str, expires_delta: timedelta) -> str:
    now = datetime.now(timezone.utc)
    to_encode = {"sub": subject, "iat": now, "exp": now + expires_delta}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_access_token(user_id: int) -> str:
    return create_token(str(user_id), timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))

def create_refresh_token(user_id: int) -> str:
    return create_token(str(user_id), timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))
