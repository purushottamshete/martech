from fastapi import APIRouter, Depends, Body
from .auth import get_current_superadmin_user
from models import User as UserModel, USER_ROLES, ActivityLog as ActivityLogModel
from schema import User as UserSchema, ActivityLog as ActivityLogSchema
from fastapi_sqlalchemy import db
from typing import List, Annotated
from datetime import datetime

import logging
logger = logging.getLogger(__name__)

router = APIRouter()

# Get Activity Logs
@router.get("/activity_log/", dependencies=[Depends(get_current_superadmin_user)], response_model=List[ActivityLogSchema])
async def get_activity_logs(from_dt: datetime = datetime.now(), to_dt: datetime=datetime.now()):
    print(type(from_dt))
    activity_logs =  db.session.query(ActivityLogModel).filter(ActivityLogModel.created_at >= from_dt).filter(ActivityLogModel.created_at <= to_dt).order_by(ActivityLogModel.created_at)
    return activity_logs