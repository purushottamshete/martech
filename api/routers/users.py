from fastapi import APIRouter
from fastapi_sqlalchemy import db
from typing import List
from schema import User as UserSchema, UserCreate as UserCreateSchema, UserUpdate as UserUpdateSchema, UserUpdatePassword as UserUpdatePasswordSchema
from .auth import get_current_superadmin_user, get_current_admin_user, get_user_by_email
from fastapi import Depends, HTTPException, status
from models import User as UserModel, USER_ROLES
from passlib.context import CryptContext
from uuid import UUID
from utility import verify_password, get_password_hash
from fastapi.responses import JSONResponse
from .emails import send_email
import logging

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logger = logging.getLogger(__name__)
router = APIRouter()

# Get Admins
@router.get("/admins/", dependencies=[Depends(get_current_superadmin_user)], response_model=List[UserSchema])
async def get_admins():
    users =  db.session.query(UserModel).filter(UserModel.role == USER_ROLES.ADMIN).all()
    return users


# Get Users
@router.get("/users/", dependencies=[Depends(get_current_admin_user)], response_model=List[UserSchema])
async def get_users():
    users =  db.session.query(UserModel).filter(UserModel.role == USER_ROLES.USER).all()
    return users

# Create User
# Kept API open for User Registration
@router.post("/registration/")
async def create_user(user: UserCreateSchema):
    db_user = get_user_by_email(email=user.email)
    if db_user:
        logger.exception("Email already registered")
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = UserModel(first_name=user.first_name, last_name=user.last_name, email=user.email, hashed_password=get_password_hash(user.password))
    db.session.add(db_user)
    db.session.commit()
    db.session.refresh(db_user)
    await send_email([db_user.email], db_user)
    return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=f"Hi {db_user.first_name}, Thanks for choosing martech. Please check your email: {db_user.email} inbox and click on the link to confirm your registration."
    )

# Update User
@router.put("/users/{user_id}", response_model=UserSchema, dependencies=[Depends(get_current_admin_user)])
def update_user(user_id: UUID, user: UserUpdateSchema, current_user = Depends(get_current_admin_user)):
    db_user =  db.session.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        logger.exception("Invalid User")
        raise HTTPException(status_code=400, detail="Invalid User")
    
    # Change of Role
    if user.role != db_user.role:
        # No one is allowed to change role to Super Admin
        if user.role == USER_ROLES.SUPERADMIN: 
            logger.exception("Not Autherized to change Role to Super Admin")
            raise HTTPException(status_code=401, detail="Not Autherized to change Role to Super Admin")
        
        # Admin Role can be given by SuperAdmin only
        if user.role == USER_ROLES.ADMIN:
            if current_user.role != USER_ROLES.SUPERADMIN:
                logger.exception("Not Autherized to change Role to Admin")
                raise HTTPException(status_code=401, detail="Not Autherized to change Role to Admin")

    db_user.first_name = user.first_name
    db_user.last_name = user.last_name
    db_user.email = user.email
    db_user.phone_no = user.phone_no
    db_user.is_active = user.is_active
    db_user.language = user.language
    db_user.timezone = user.timezone
    db_user.role = user.role

    db.session.commit()
    db.session.refresh(db_user)
    return db_user

# Update User Password
@router.put("/users/password/{user_id}", response_model=UserSchema, dependencies=[Depends(get_current_admin_user)])
def update_user(user_id: UUID, user: UserUpdatePasswordSchema, current_user = Depends(get_current_admin_user)):
    db_user =  db.session.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        logger.exception("Invalid User")
        raise HTTPException(status_code=400, detail="Invalid User")
    
    # No one is allowed to change password of Super Admin 
    # Superadmin password will change only from backend db
    if db_user.role == USER_ROLES.SUPERADMIN: 
        logger.exception("Not Autherized to change Password of Super Admin")
        raise HTTPException(status_code=401, detail="Not Autherized to change Password of Super Admin")
    
    # Admin Role can be given by SuperAdmin only
    if db_user.role == USER_ROLES.ADMIN:
        if current_user.role != USER_ROLES.SUPERADMIN:
            logger.exception("Not Autherized to change password of Admin")
            raise HTTPException(status_code=401, detail="Not Autherized to change password of Admin")

    if not verify_password(user.password, db_user.hashed_password):
        logger.exception("Invalid Existing Password")
        raise HTTPException(status_code=400, detail="Invalid Existing Password")
   
    db_user.hashed_password = get_password_hash(user.new_password)

    db.session.commit()
    db.session.refresh(db_user)
    return db_user


# Delete User
@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_superadmin_user)])
def delete_user(user_id: UUID, current_user = Depends(get_current_admin_user)):

    # Only Super Admin can delete Users
    if current_user.role != USER_ROLES.SUPERADMIN: 
        logger.exception("Not Autherized")
        raise HTTPException(status_code=401, detail="Not Autherized")
    
    db_user =  db.session.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        logger.exception("Invalid User")
        raise HTTPException(status_code=400, detail="Invalid User")
    
    # No one is allowed to delete Super Admin
    if db_user.role == USER_ROLES.SUPERADMIN: 
        logger.exception("Not Autherized")
        raise HTTPException(status_code=401, detail="Not Autherized")
    
    db.session.delete(db_user)
    db.session.commit()

    return None