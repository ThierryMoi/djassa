from app.repositories.user_repository import get_user_by_keycloak_id, create_user, update_user
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.pydantic_models import UserCreate, UserUpdate
from typing import Optional
from app.models.db_models import UserProfile

async def get_user_profile(db: AsyncSession, keycloak_id: str) -> Optional[UserProfile]:
    return await get_user_by_keycloak_id(db, keycloak_id)

async def create_user_profile(db: AsyncSession, user_in: UserCreate, keycloak_id: str) -> UserProfile:
    return await create_user(db, user_in, keycloak_id)

async def update_user_profile(db: AsyncSession, db_user: UserProfile, user_update: UserUpdate) -> UserProfile:
    return await update_user(db, db_user, user_update)
