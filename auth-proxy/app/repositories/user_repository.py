import httpx
from app.core.config import settings

class UserRepository:
    def __init__(self):
        self.base_url = settings.USERS_SERVICE_URL

    async def get_user_info(self, token: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api/v1/users/me",
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            return response.json()
