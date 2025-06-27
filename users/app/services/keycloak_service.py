# app/services/keycloak_service.py

import httpx
from fastapi import HTTPException
from app.core.config import settings
from app.models.pydantic_models import RegisterUser

async def get_admin_token() -> str:
    async with httpx.AsyncClient() as client:
        data = {
            "client_id": "admin-cli",
            "grant_type": "password",
            "username": settings.KEYCLOAK_ADMIN_USERNAME,
            "password": settings.KEYCLOAK_ADMIN_PASSWORD,
        }
        r = await client.post(f"{settings.KEYCLOAK_URL}/realms/master/protocol/openid-connect/token", data=data)
        if r.status_code != 200:
            raise HTTPException(status_code=500, detail="Cannot get admin token from Keycloak")
        return r.json()["access_token"]

async def create_keycloak_user(user: RegisterUser, admin_token: str):
    async with httpx.AsyncClient() as client:
        headers = {
            "Authorization": f"Bearer {admin_token}",
            "Content-Type": "application/json"
        }

        # Étape 1: Créer l'utilisateur de base
        payload = {
            "username": user.username,
            "email": user.email,
            "firstName": user.firstName,  # <-- ajoute ceci
            "lastName": user.lastName,    # <-- et ceci
            "enabled": True,
            "credentials": [{"type": "password", "value": user.password, "temporary": False}],
        }

        r = await client.post(
            f"{settings.KEYCLOAK_URL}/admin/realms/{settings.KEYCLOAK_REALM}/users",
            json=payload,
            headers=headers,
        )

        if r.status_code != 201:
            raise HTTPException(status_code=400, detail=f"Keycloak user creation failed: {r.text}")

        # Étape 2: Récupérer l'ID de l'utilisateur
        user_id = await get_keycloak_user_id(user.username, admin_token)

        # Étape 3: Définir un mot de passe NON temporaire
        password_payload = {
            "type": "password",
            "value": user.password,
            "temporary": False
        }

        r2 = await client.put(
            f"{settings.KEYCLOAK_URL}/admin/realms/{settings.KEYCLOAK_REALM}/users/{user_id}/reset-password",
            json=password_payload,
            headers=headers,
        )

        if r2.status_code != 204:
            raise HTTPException(status_code=500, detail=f"Password setting failed: {r2.text}")


async def get_keycloak_user_id(username: str, admin_token: str) -> str:
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {admin_token}"}
        r = await client.get(
            f"{settings.KEYCLOAK_URL}/admin/realms/{settings.KEYCLOAK_REALM}/users",
            headers=headers,
            params={"username": username},
        )
        if r.status_code != 200 or not r.json():
            raise HTTPException(status_code=404, detail="User not found in Keycloak")
        return r.json()[0]["id"]
