from fastapi import APIRouter, HTTPException
import httpx
from app.models.pydantic_models import LoginUser
from app.core.config import settings
from fastapi import Depends
from app.core.security import verify_token, security
from jose import jwt

from fastapi.responses import JSONResponse


router = APIRouter()

@router.post("/login")
async def login_user(user: LoginUser):
    data = {
        "grant_type": "password",
        "client_id": settings.KEYCLOAK_CLIENT_ID,
        "username": user.username,
        "password": user.password,
    }

    # Si le client est "confidential", on ajoute le client_secret
    if settings.KEYCLOAK_CLIENT_SECRET:
        data["client_secret"] = settings.KEYCLOAK_CLIENT_SECRET

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token",
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

    if response.status_code != 200:
        print(f"Login failed: {response.text}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "access_token": response.json().get("access_token"),
        "refresh_token": response.json().get("refresh_token"),
        "token_type": response.json().get("token_type"),
        "expires_in": response.json().get("expires_in"),
    }


@router.post("/logout")
async def logout_user(credentials = Depends(security)):
    token = credentials.credentials
    unverified = jwt.get_unverified_claims(token)
    session_state = unverified.get("session_state")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/logout",
            data={
                "client_id": "account",
                "refresh_token": "",  # facultatif si tu l’as dans ton front
            },
            headers={"Authorization": f"Bearer {token}"}
        )

    if response.status_code != 204:
        raise HTTPException(status_code=400, detail="Logout failed")

    return {"message": "Logged out successfully"}

@router.get("/")
async def validate_token(payload=Depends(verify_token)):
    return JSONResponse(content={"message": "Token is valid", "claims": payload})
