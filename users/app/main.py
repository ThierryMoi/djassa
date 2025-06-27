from fastapi import FastAPI
from app.api.v1.endpoints import users,auth
from app.init_db import init_database_if_not_exists
from app.core.database import engine
from app.models.db_models import Base
from app.models import *  
app = FastAPI(title="Users Microservice")

@app.on_event("startup")
async def startup_event():
    init_database_if_not_exists()  # synchrone !
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Tables créées avec succès.")
        
app.include_router(users.router, prefix="/v1", tags=["users"])
app.include_router(auth.router, prefix="/v1", tags=["authentification"])
