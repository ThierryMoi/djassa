from typing import List
import httpx
import os
from functools import lru_cache

class VaultClient:
    def __init__(self, vault_addr: str, vault_token: str):
        self.vault_addr = vault_addr.rstrip("/")
        self.vault_token = vault_token
        self.headers = {"X-Vault-Token": vault_token}

    def get_secret(self, path: str, key: str) -> str:
        url = f"{self.vault_addr}/v1/{path}"
        try:
            response = httpx.get(url, headers=self.headers, timeout=5.0)
            response.raise_for_status()
            data = response.json()
            # Vault KV v2 nested under "data" key twice
            return data["data"]["data"][key]
        except Exception as e:
            raise RuntimeError(f"Erreur récupération secret Vault {path}/{key} : {e}")

@lru_cache()
def get_settings():
    vault_addr = os.getenv("VAULT_ADDR", "http://vault:8200")
    vault_token = os.getenv("VAULT_TOKEN", "root")
    vault_client = VaultClient(vault_addr, vault_token)

    class Settings:
        KEYCLOAK_URL: str = os.getenv("keycloak_url" )   
        KEYCLOAK_ADMIN_USERNAME: str = vault_client.get_secret("secret/data/keycloak", "admin")
        KEYCLOAK_ADMIN_PASSWORD: str = vault_client.get_secret("secret/data/keycloak", "password")

        POSTGRES_USER: str = vault_client.get_secret("secret/data/postgres", "username")
        POSTGRES_PASSWORD: str = vault_client.get_secret("secret/data/postgres", "password")
        POSTGRES_DB: str =  os.getenv("postgres_db", "") 
        DATABASE_URL: str = os.getenv("database_url", f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres:5432/{POSTGRES_DB}") 
        KEYCLOAK_CLIENT_ID: str = vault_client.get_secret("secret/data/keycloak", "client_id")
        KEYCLOAK_CLIENT_SECRET:str = vault_client.get_secret("secret/data/keycloak", "client_secret") 
        KEYCLOAK_PUBLIC_KEY: str = vault_client.get_secret("secret/data/keycloak", "public_key")
        KEYCLOAK_REALM: str =  os.getenv("realm", "") 
        ALGORITHM: str = "RS256"
        USERS_SERVICE_URL: str =  os.getenv("user_service_url", "")
        PUBLIC_PATHS_LIST: List[str] =  ["/api/users/v1/login","/api/users/v1/register", "/v1/validate"]
        AUDIENCE: str = os.getenv("audience", "")

    return Settings()

settings = get_settings()
