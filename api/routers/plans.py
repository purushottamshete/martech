from fastapi import APIRouter, Depends, Body, HTTPException, status
import logging
from models import Plan as PlanModel, PLAN_STATUS, USER_ROLES
from .auth import get_current_active_user, get_current_superadmin_user
from schema import PlanInDB as PlanInDBSchema, PlanUpdate as PlanUpdateSchema
from schema import Plan as PlanSchema
from typing import List
from fastapi_sqlalchemy import db

logger = logging.getLogger(__name__)
router = APIRouter()

# Get Plans
@router.get("/plans/", dependencies=[Depends(get_current_active_user)], response_model=List[PlanInDBSchema])
async def get_plans():
    plans =  db.session.query(PlanModel).filter(PlanModel.status == PLAN_STATUS.ACTIVE).all()
    return plans

# Create Plans
@router.post("/plans/", dependencies=[Depends(get_current_superadmin_user)], response_model=PlanInDBSchema)
async def create_plan(plan: PlanSchema):
    plans_check =  db.session.query(PlanModel).filter(PlanModel.name == plan.name).first()
    if plans_check:
        raise HTTPException(status_code=400, detail="Plan already exists")

    db_plan = PlanModel(name=plan.name, 
                        price=plan.price, 
                        billing_cycle=plan.billing_cycle, 
                        page_list_limit=plan.page_list_limit,
                        api_list_limit=plan.api_list_limit,
                        users_limit=plan.users_limit,
                        storage_limit=plan.storage_limit,
                        )
    db.session.add(db_plan)
    db.session.commit()
    db.session.refresh(db_plan)
    return db_plan

# Update Plan
@router.put("/plans/{plan_id}", response_model=PlanInDBSchema, dependencies=[Depends(get_current_superadmin_user)])
def update_plan(plan_id: int, plan: PlanUpdateSchema):
    db_plan =  db.session.query(PlanModel).filter(PlanModel.id == plan_id).first()
    if not db_plan:
        raise HTTPException(status_code=400, detail="Invalid Plan")
    
    db_plan.name = plan.name
    db_plan.price = plan.price
    db_plan.billing_cycle = plan.billing_cycle
    db_plan.page_list_limit = plan.page_list_limit
    db_plan.api_list_limit = plan.api_list_limit
    db_plan.users_limit = plan.users_limit
    db_plan.storage_limit = plan.storage_limit
    db_plan.status = plan.status

    db.session.commit()
    db.session.refresh(db_plan)
    return db_plan

# Delete Plan
@router.delete("/plans/{plan_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_superadmin_user)])
def delete_plan(plan_id:int, current_user = Depends(get_current_superadmin_user)):

    # Only Super Admin can delete Plans
    if current_user.role != USER_ROLES.SUPERADMIN: 
        raise HTTPException(status_code=401, detail="Not Autherized")
    
    db_plan =  db.session.query(PlanModel).filter(PlanModel.id == plan_id).first()
    if not db_plan:
        raise HTTPException(status_code=400, detail="Invalid Plan")
    
    db.session.delete(db_plan)
    db.session.commit()

    return None