from pydantic import BaseModel, ConfigDict, EmailStr, Field, validator
from datetime import datetime
from models import USER_ROLES, ACTIVITY_TYPE
from uuid import UUID

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: EmailStr

class UserBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=30)
    last_name: str = Field(min_length=1, max_length=30)
    email: EmailStr

class UserUpdatePassword(BaseModel):
    password: str = Field(min_length=8)
    new_password: str = Field(min_length=8)

class UserUpdate(UserBase):
    phone_no: str | None = Field(max_length=15)
    is_active: bool
    language: str | None = None
    timezone: str | None = None
    role: USER_ROLES

class UserCreate(UserBase):
    password: str = Field(min_length=8)

    # Password Validator
    # @validator('password', always=True)
    # def validate_password1(cls, value):
    #     password = value.get_secret_value()
    #     min_length = 8
    #     errors = ''
    #     if len(password) < min_length:
    #         errors += 'Password must be at least 8 characters long. '
    #     if not any(character.islower() for character in password):
    #         errors += 'Password should contain at least one lowercase character.'
    #     if errors:
    #         raise ValueError(errors)
        
    #     return value

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    phone_no: str | None = Field(max_length=15)
    is_active: bool
    last_login: datetime | None = None
    language: str | None = None
    timezone: str | None = None
    role: USER_ROLES

class UserInDB(User):
    hashed_password: str


class ActivityLog(BaseModel):
    id: int
    user_id: UUID
    activity_type: ACTIVITY_TYPE
    activity_desc: str
    created_at: datetime