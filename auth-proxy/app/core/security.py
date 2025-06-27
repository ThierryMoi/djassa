from jose import jwt, JWTError
from app.core.config import settings

def get_keycloak_public_key_pem() -> str:
    key = settings.KEYCLOAK_PUBLIC_KEY
    pem_key = "-----BEGIN PUBLIC KEY-----\n"
    for i in range(0, len(key), 64):
        pem_key += key[i:i+64] + "\n"
    pem_key += "-----END PUBLIC KEY-----\n"
    return pem_key


def verify_token(token: str) -> dict:
    try:
        public_key = get_keycloak_public_key_pem()
        payload = jwt.decode(
            token,
            public_key,
            algorithms=[settings.ALGORITHM],
            audience=settings.AUDIENCE
        )
        return payload
    except JWTError as e:
        raise Exception(f"Token invalide: {str(e)}")
