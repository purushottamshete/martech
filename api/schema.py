from pydantic import BaseModel, ConfigDict
from datetime import datetime
from models import USER_ROLES
from uuid import UUID

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    first_name: str
    last_name: str
    email: str | None = None
    phone_no: str | None = None
    is_active: bool | None = None
    last_login: datetime | None = None
    language: str
    timezone: str
    role: USER_ROLES

class UserInDB(User):
    hashed_password: str