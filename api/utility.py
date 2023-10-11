from passlib.context import CryptContext
from uuid import UUID
from models import ACTIVITY_TYPE
from fastapi_sqlalchemy import db
from models import ActivityLog as ActivityLogModel, User as UserModel
from fastapi import HTTPException
from datetime import datetime
import pytz
import logging
logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def audit_log(id: UUID, type: ACTIVITY_TYPE, desc: str):
    try:
        db_activity_log = ActivityLogModel(user_id=id, activity_type=type, activity_desc=desc)
        db.session.flush()
        db.session.add(db_activity_log)
        db.session.commit()
        db.session.refresh(db_activity_log)
    except Exception as e:
        logger.exception(f"Exception while audit_logging, {e}")

async def update_user_lastlogin(id: UUID):
    db_user =  db.session.query(UserModel).filter(UserModel.id == id).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid User")
    try:
        if db_user.timezone:
            user_timezone = pytz.timezone(db_user.timezone)
            dt_with_tz = datetime.now(tz=user_timezone)
        else:
            dt_with_tz = datetime.now(tz=pytz.UTC)
        # print(f"User Timezone: {user_timezone}, Datetime: {dt_with_tz}")
        # TODO Timezone check
        db_user.last_login = dt_with_tz
        db.session.commit()
    except Exception as e:
        logger.exception(f"Exception while updating last loging, {e}")