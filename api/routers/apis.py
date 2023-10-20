from fastapi import APIRouter, Depends, HTTPException, status
import logging
from models import Api as ApiModel
from .auth import get_current_superadmin_user
from schema import ApiInDB as ApiInDBSchema
from schema import Api as ApiSchema
from typing import List
from fastapi_sqlalchemy import db

logger = logging.getLogger(__name__)
router = APIRouter()

# Get Apis
@router.get("/apis/", dependencies=[Depends(get_current_superadmin_user)], response_model=List[ApiInDBSchema])
async def get_apis():
    apis =  db.session.query(ApiModel).order_by(ApiModel.created_at).all()
    return apis

# Create Api
@router.post("/apis/", dependencies=[Depends(get_current_superadmin_user)], response_model=ApiInDBSchema)
async def create_api(api: ApiSchema):

    api_check =  db.session.query(ApiModel).filter(ApiModel.name == api.name).first()
    if api_check:
        raise HTTPException(status_code=400, detail="Api already exists")

    db_api = ApiModel(  name=api.name, 
                        description=api.description )
    db.session.add(db_api)
    db.session.commit()
    db.session.refresh(db_api)
    return db_api

# Update Api
@router.put("/apis/{api_id}", dependencies=[Depends(get_current_superadmin_user)], response_model=ApiInDBSchema)
def update_api(api_id: int, api: ApiSchema):
    db_api =  db.session.query(ApiModel).filter(ApiModel.id == api_id).first()
    if not db_api:
        raise HTTPException(status_code=400, detail="Invalid Api")
    
    if db_api.name != api.name:
        api_check =  db.session.query(ApiModel).filter(ApiModel.name == api.name).first()
        if api_check:
            raise HTTPException(status_code=400, detail="Api already exists")
    
    db_api.name = api.name
    db_api.description = api.description
    
    db.session.commit()
    db.session.refresh(db_api)
    return db_api

# Delete Api
@router.delete("/apis/{api_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_superadmin_user)])
def delete_api(api_id: int):
 
    db_api =  db.session.query(ApiModel).filter(ApiModel.id == api_id).first()
    if not db_api:
        raise HTTPException(status_code=400, detail="Invalid Api")
    
    db.session.delete(db_api)
    db.session.commit()

    return None