from fastapi import FastAPI
from app.api.v1.endpoints import validate

app = FastAPI(title="Auth Proxy")

app.include_router(validate.router, prefix="/v1")
