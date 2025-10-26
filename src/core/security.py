"""
Security utilities: password hashing and JWT creation/verification
"""
from datetime import datetime, timedelta
from typing import Any, Optional

from jose import jwt, JWTError
from passlib.context import CryptContext

from src.core.config import get_settings

settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours
MAX_BCRYPT_PASSWORD_BYTES = 72


def get_password_hash(password: str) -> str:
    # bcrypt has a 72-byte input limit. Enforce it explicitly to provide a clear error.
    if isinstance(password, str):
        pw_bytes = password.encode("utf-8")
    else:
        pw_bytes = bytes(password)
    if len(pw_bytes) > MAX_BCRYPT_PASSWORD_BYTES:
        raise ValueError(
            f"Password too long for bcrypt (max {MAX_BCRYPT_PASSWORD_BYTES} bytes)."
        )
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode: dict[str, Any] = {"sub": subject, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict[str, Any]]:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None