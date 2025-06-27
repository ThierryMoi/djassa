from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user_service import get_user_profile, create_user_profile, update_user_profile
from app.models.pydantic_models import UserCreate, UserUpdate

async def get_or_create_user_profile(db: AsyncSession, user_in: UserCreate, keycloak_id: str):
    user = await get_user_profile(db, keycloak_id)
    if not user:
        user = await create_user_profile(db, user_in, keycloak_id)
    return user

async def get_user(db: AsyncSession, keycloak_id: str):
    user = await get_user_profile(db, keycloak_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user


async def update_user(db: AsyncSession, keycloak_id: str, user_update: UserUpdate):
    user = await get_user_profile(db, keycloak_id)
    if not user:
        raise HTTPException(404, "User not found")
    user = await update_user_profile(db, user, user_update)
    return user
