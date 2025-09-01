from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.config import settings
from app.db.session import get_db
from app.models.user import User

# -------------------------------
# Password Hashing (bcrypt)
# -------------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash plain text password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against the stored hash."""
    return pwd_context.verify(plain_password, hashed_password)


# -------------------------------
# JWT Token Handling
# -------------------------------
def create_access_token(data: dict, expires_minutes: Optional[int] = None) -> str:
    """Create a JWT token with expiry."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    """Decode JWT token and return payload, or None if invalid/expired."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None


# -------------------------------
# FastAPI Dependencies
# -------------------------------
# Used by FastAPI to extract Bearer tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
) -> User:
    """Get the current logged-in user from the JWT token."""
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# -------------------------------
# Role-Based Access
# -------------------------------
def require_role(user: User, roles: list[str]):
    """Ensure user has one of the required roles."""
    if user.role not in roles:
        raise HTTPException(
            status_code=403,
            detail=f"User does not have required role. Needs one of: {roles}"
        )
