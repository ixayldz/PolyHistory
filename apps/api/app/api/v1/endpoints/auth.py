from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.deps import get_db, get_current_active_user
from app.core.security import (
    verify_password, get_password_hash, create_access_token, create_refresh_token
)
from app.core.config import get_settings
from app.core.exceptions import AuthenticationException, ValidationException
from app import schemas, models

router = APIRouter()
settings = get_settings()


@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_in: schemas.UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new user."""
    # Check if user exists
    result = await db.execute(
        select(models.User).where(models.User.email == user_in.email)
    )
    if result.scalar_one_or_none():
        raise ValidationException("Email already registered")
    
    # Create new user
    user = models.User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        tier="free",
        monthly_analysis_count=0,
        monthly_analysis_limit=5
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    return user


@router.post("/login", response_model=schemas.Token)
async def login(
    credentials: schemas.LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """Login user and return tokens."""
    result = await db.execute(
        select(models.User).where(models.User.email == credentials.email)
    )
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise AuthenticationException("Incorrect email or password")
    
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh", response_model=schemas.Token)
async def refresh_token(
    refresh_token: str,
    db: AsyncSession = Depends(get_db)
):
    """Refresh access token."""
    from app.core.security import decode_token
    
    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise AuthenticationException("Invalid refresh token")
    
    user_id = payload.get("sub")
    result = await db.execute(
        select(models.User).where(models.User.id == user_id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise AuthenticationException("User not found")
    
    new_access_token = create_access_token(data={"sub": str(user.id)})
    new_refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=schemas.UserResponse)
async def get_current_user_info(
    current_user: models.User = Depends(get_current_active_user)
):
    """Get current user information."""
    return current_user
