# app/init_db.py

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from app.core.config import settings

def init_database_if_not_exists():
    sync_url = settings.DATABASE_URL.replace("postgresql+asyncpg", "postgresql")
    engine = create_engine(sync_url)

    if not database_exists(engine.url):
        print("⚙️ Création de la base de données...")
        create_database(engine.url)
    else:
        print("✅ Base de données déjà existante.")
