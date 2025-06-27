# app/models/pydantic_models.py

from typing import Optional
from pydantic import BaseModel, EmailStr

class RegisterUser(BaseModel):
    username: str
    email: EmailStr
    password: str
    firstName: str
    lastName: str
    role: Optional[str] = "buyer"



class UserCreate(BaseModel):
    username: str
    email: EmailStr
    firstName: str
    lastName: str


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None

class UserPublic(BaseModel):
    id: int
    username: str
    email: str
    firstName: str
    lastName: str
    role: str

class LoginUser(BaseModel):
    username: str
    password: str
