from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from fastapi import Request
from app.core.config import settings
from app.core.security import verify_token

class AuthProxyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        print(f"Incoming request path: {path}")
        print(settings.PUBLIC_PATHS_LIST)
        if any(path.startswith(p) for p in settings.PUBLIC_PATHS_LIST):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"detail": "Token manquant"})

        token = auth_header.split(" ")[1]

        try:
            payload = verify_token(token)
            request.state.user = payload  # toujours dispo si le backend veut l’utiliser

            # Claims clés
            user_id = payload.get("sub")
            username = payload.get("preferred_username")
            email = payload.get("email")

            # Injecter dans les headers HTTP downstream (users, etc.)
            request.scope["headers"] += [
                (b"x-user-id", user_id.encode()) if user_id else b"",
                (b"x-user-username", username.encode()) if username else b"",
                (b"x-user-email", email.encode()) if email else b"",
            ]

        except Exception as e:
            return JSONResponse(status_code=401, content={"detail": f"Token invalide: {str(e)}"})

        return await call_next(request)
