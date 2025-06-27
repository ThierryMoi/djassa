from fastapi import APIRouter, HTTPException, Security, Request, Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.services.auth_service import AuthService
from app.core.config import settings

router = APIRouter()
security = HTTPBearer(auto_error=False)
auth_service = AuthService()

@router.get("/validate")
async def validate_token(
    request: Request,
    response: Response,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    path = request.headers.get("X-Forwarded-Uri", "")

    # Route publique : rien à injecter
    if any(path.startswith(p) for p in settings.PUBLIC_PATHS_LIST):
        return {"detail": "Public route, no auth required"}

    if not credentials:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    token = credentials.credentials
    try:
        payload, user_info = await auth_service.validate_token_and_get_user(token)

        # Injecter des claims dans les headers retournés à Traefik
        if payload.get("sub"):
            response.headers["X-User-Id"] = payload["sub"]
        if payload.get("preferred_username"):
            response.headers["X-User-Username"] = payload["preferred_username"]
        if payload.get("email"):
            response.headers["X-User-Email"] = payload["email"]

        return {"payload": payload}

    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
