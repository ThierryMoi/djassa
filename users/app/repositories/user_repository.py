from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.db_models import UserProfile
from typing import Optional
from app.models.pydantic_models import UserCreate, UserUpdate

async def get_user_by_keycloak_id(db: AsyncSession, keycloak_id: str) -> Optional[UserProfile]:
    result = await db.execute(select(UserProfile).filter_by(keycloak_id=keycloak_id))
    return result.scalars().first()

async def create_user(db: AsyncSession, user: UserCreate, keycloak_id: str) -> UserProfile:
    db_user = UserProfile(
        username=user.username,
        email=user.email,
        firstName= user.firstName,  # <-- ajoute ceci
        lastName=user.lastName,    # <-- et ceci
        role=user.role,
        keycloak_id=keycloak_id,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def update_user(db: AsyncSession, db_user: UserProfile, user_update: UserUpdate):
    for var, value in vars(user_update).items():
        setattr(db_user, var, value) if value else None
    await db.commit()
    await db.refresh(db_user)
    return db_user
