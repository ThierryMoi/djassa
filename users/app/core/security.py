import httpx
from jose import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .config import settings

security = HTTPBearer()
_jwks = None

async def get_jwks():
    global _jwks
    if _jwks is None:
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/certs")
            _jwks = r.json()
    return _jwks

async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    jwks = await get_jwks()

    try:
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header["kid"]
        key = next(k for k in jwks["keys"] if k["kid"] == kid)
    except StopIteration:
        raise HTTPException(401, "Clé publique introuvable")

    try:
        payload = jwt.decode(token, key, algorithms=[settings.ALGORITHM], audience="djassa-client")
        return payload
    except Exception as e:
        raise HTTPException(401, f"Token invalide: {e}")
