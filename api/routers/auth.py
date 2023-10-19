from fastapi import APIRouter, BackgroundTasks, Request, Response
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from schema import Token, TokenData, User as UserSchema, UserInDB
from utility import verify_password, audit_log
from datetime import datetime, timedelta
from jose import JWTError, jwt
from models import User as UserModel, USER_ROLES, ACTIVITY_TYPE
from fastapi_sqlalchemy import db
from utility import update_user_lastlogin, audit_log
import settings


import logging
logger = logging.getLogger(__name__)

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user_by_email(email: str):
    user =  db.session.query(UserModel).filter(UserModel.email == email).first()
    if user:
        return UserInDB.model_validate(user)
    else:
        return user

def authenticate_user(username: str, password: str):
    user = get_user_by_email(email=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    user = get_user_by_email(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(request: Request, background_tasks: BackgroundTasks, current_user: UserSchema = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    background_tasks.add_task(audit_log, id=current_user.id, type=ACTIVITY_TYPE.CALLAPI, desc=request.url.path)
    return current_user

async def get_current_admin_user(current_user: UserSchema = Depends(get_current_active_user)):
    if not (current_user.role == USER_ROLES.ADMIN or current_user.role == USER_ROLES.SUPERADMIN ):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Not a Admin user")
    return current_user

async def get_current_superadmin_user(current_user: UserSchema = Depends(get_current_active_user)):
    if not current_user.role == USER_ROLES.SUPERADMIN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Not a Super Admin user")
    return current_user

    
@router.post("/token", response_model=Token)
async def login_for_access_token(request: Request, form_data: Annotated[OAuth2PasswordRequestForm, Depends()], background_tasks: BackgroundTasks):
    """
    This method is used to generate the access token

    Args: 
    form_date : OAuth2PasswordRequestForm
        Form data containing username and password of OAuth2PasswordRequestForm type
        In our case we are using email as a Username
    
    Returns:
    Token
        Returns access token and token type
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    background_tasks.add_task(update_user_lastlogin, user.id)
    background_tasks.add_task(audit_log, id=user.id, type=ACTIVITY_TYPE.LOGIN, desc=request.url.path)
    return {"access_token": access_token, "token_type": "bearer"}

