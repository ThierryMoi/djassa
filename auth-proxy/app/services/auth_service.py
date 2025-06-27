from app.core.security import verify_token
from app.models.token_models import TokenPayload

class AuthService:
    async def validate_token_and_get_user(self, token: str):
        payload = verify_token(token)
        # Ici tu peux appeler user service pour récupérer infos utilisateur
        # ou juste retourner payload pour Traefik
        return payload, {"user_id": payload.get("sub")}
