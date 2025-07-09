from fastapi import APIRouter, Depends, Request, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.pydantic_models import RegisterUser, UserUpdate, UserPublic
from app.controllers.user_controller import get_or_create_user_profile, get_user, update_user
from app.services.keycloak_service import get_admin_token, create_keycloak_user, get_keycloak_user_id

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: RegisterUser, db: AsyncSession = Depends(get_db)):
    admin_token = await get_admin_token()
    await create_keycloak_user(user, admin_token)
    keycloak_id = await get_keycloak_user_id(user.username, admin_token)
    user_profile = await get_or_create_user_profile(db, user, keycloak_id)
    return {"message": "User registered successfully", "user": user_profile}

@router.get("/me", response_model=UserPublic)
async def read_own_profile(request: Request, db: AsyncSession = Depends(get_db)):
    user_id = request.headers.get("x-user-id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Missing user ID")
    return await get_user(db, user_id)

@router.put("/", response_model=UserPublic)
async def update_profile(
    user_update: UserUpdate,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    user_id = request.headers.get("x-user-id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Missing user ID")
    return await update_user(db, user_id, user_update)


@router.get("/health")
async def health_check():
    return JSONResponse(status_code=200, content={"status": "ok"})