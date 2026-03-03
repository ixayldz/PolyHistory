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
    """Check analysis quota and determine analysis mode (PRD v2.0 Free Tier).
    
    Free tier: 1 multi-model + 4 single-model per month.
    Sets current_user._analysis_mode for downstream use.
    """
    from app.core.config import get_settings
    from app.core.exceptions import InsufficientBalanceException
    
    settings = get_settings()
    total_limit = current_user.monthly_analysis_limit
    
    if current_user.tier == 'free':
        multi_limit = settings.FREE_TIER_MULTI_MODEL_LIMIT
        single_limit = settings.FREE_TIER_SINGLE_MODEL_LIMIT
        total_free = multi_limit + single_limit
        
        if current_user.monthly_analysis_count >= total_free:
            raise InsufficientBalanceException(total_free)
        
        # First N analyses are multi-model, rest are single-model
        if current_user.monthly_analysis_count < multi_limit:
            current_user._analysis_mode = "multi_model"
        else:
            current_user._analysis_mode = "single_model"
    else:
        if current_user.monthly_analysis_count >= total_limit:
            raise InsufficientBalanceException(total_limit)
        current_user._analysis_mode = "multi_model"
    
    return current_user
