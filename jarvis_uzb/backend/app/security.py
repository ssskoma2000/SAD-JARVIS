import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status, WebSocketException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

load_dotenv()

# --- Konfiguratsiya ---
# .env faylida kuchli, tasodifiy SECRET_KEY yaratish muhim!
SECRET_KEY = os.getenv("SECRET_KEY", "a_very_secret_key_that_should_be_in_env_file")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --- Parolni xeshlash ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- OAuth2 ---
# Tokenni HTTP header'dan oladi (REST API uchun)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Oddiy parolni xeshlangan parol bilan solishtiradi."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Parolni xeshlaydi."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Yangi JWT access token yaratadi."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user_from_token(token: str = Depends(oauth2_scheme)) -> str:
    """
    Tokenni tekshiradi va foydalanuvchi nomini qaytaradi.
    Bu himoyalangan endpoint'lar uchun "dependency" sifatida ishlatiladi.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Autentifikatsiya ma'lumotlari tasdiqlanmadi",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        if username is None:
            raise credentials_exception
        # Haqiqiy ilovada bu yerda ma'lumotlar bazasidan foydalanuvchi olinadi.
        # Hozircha faqat foydalanuvchi nomini qaytaramiz.
        return username
    except JWTError:
        raise credentials_exception

async def get_user_from_ws_query_param(token: str) -> str:
    """WebSocket uchun tokenni query parameter'dan oladi."""
    if not token:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason="Token topilmadi")
    return await get_current_user_from_token(token)



    #menga qizm aytgan yoomon gapla boru oshani aytvor men seni sevmima brnarsala db koop yozganu 