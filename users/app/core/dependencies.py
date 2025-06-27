from fastapi import Depends
from .security import verify_token

async def get_current_user(payload=Depends(verify_token)):
    return {
        "user_id": payload.get("sub"),
        "username": payload.get("preferred_username"),
        "email": payload.get("email"),
        "roles": payload.get("realm_access", {}).get("roles", [])
    }
