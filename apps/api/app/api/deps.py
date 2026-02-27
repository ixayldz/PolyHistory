from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError
from app.core.database import get_db
from app.core.security import decode_token
from app.core.exceptions import AuthenticationException
from app import models

security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> models.User:
    """Get current authenticated user from JWT token."""
    if not credentials:
        raise AuthenticationException("No authentication credentials provided")
    
    token = credentials.credentials
    payload = decode_token(token)
    
    if not payload:
        raise AuthenticationException("Invalid or expired token")
    
    user_id = payload.get("sub")
    if not user_id:
        raise AuthenticationException("Invalid token payload")
    
    from sqlalchemy import select
    result = await db.execute(
        select(models.User).where(models.User.id == user_id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise AuthenticationException("User not found")
    
    return user


async def get_current_active_user(
    current_user: models.User = Depends(get_current_user)
) -> models.User:
    """Verify user is active (can be extended for account status checks)."""
    return current_user


async def check_analysis_limit(
    current_user: models.User = Depends(get_current_active_user)
) -> models.User:
    """Check if user has remaining analysis quota."""
    if current_user.tier == 'free' and current_user.monthly_analysis_count >= current_user.monthly_analysis_limit:
        from app.core.exceptions import InsufficientBalanceException
        raise InsufficientBalanceException(current_user.monthly_analysis_limit)
    return current_user
