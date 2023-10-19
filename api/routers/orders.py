from fastapi import APIRouter, Depends, Body, HTTPException, status
import logging
from models import Order as OrderModel, ORDER_STATUS, PAYMENT_METHODS, PAYMENT_STATUS
from .auth import get_current_active_user, get_current_superadmin_user
from schema import OrderInDB as OrderInDBSchema, OrderUpdate as OrderUpdateSchema
from schema import Order as OrderSchema
from typing import List
from fastapi_sqlalchemy import db
from datetime import datetime
import pytz

logger = logging.getLogger(__name__)
router = APIRouter()

# Get Orders
@router.get("/orders/", dependencies=[Depends(get_current_superadmin_user)], response_model=List[OrderInDBSchema])
async def get_orders():
    orders =  db.session.query(OrderModel).order_by(OrderModel.created_at).all()
    return orders

# Create Orders
@router.post("/orders/", dependencies=[Depends(get_current_active_user)], response_model=OrderInDBSchema)
async def create_order(order: OrderSchema, current_user = Depends(get_current_active_user)):

    if order.payment_status == PAYMENT_STATUS.PROCESSING:
        ord_status = ORDER_STATUS.CREATED
    elif order.payment_status == PAYMENT_STATUS.PAYMENT_FAILED: 
        ord_status = ORDER_STATUS.FAILED
    elif order.payment_status == PAYMENT_STATUS.SUCCEEDED:
        ord_status = ORDER_STATUS.SUCCESS
    else:
        raise HTTPException(status_code=400, detail="Invlaid Payment Status")

    try:
        if current_user.timezone:
            tz = pytz.timezone(current_user.timezone)
        else:
            tz = pytz.UTC
    except Exception as e:
        tz = pytz.UTC
        #raise HTTPException(status_code=400, detail="Invlaid Timezone")
    
    db_order = OrderModel(user_id=order.user_id, 
                        plan_id=order.plan_id, 
                        date=datetime.now(tz=tz),
                        status=ord_status,
                        payment_method=order.payment_method,
                        payment_status=order.payment_status,
                        invoice_id=order.invoice_id,
                        billing_address=order.billing_address,
                        )
    db.session.add(db_order)
    db.session.commit()
    db.session.refresh(db_order)
    return db_order

# # Update Plan
# @router.put("/plans/{plan_id}", response_model=PlanInDBSchema, dependencies=[Depends(get_current_superadmin_user)])
# def update_plan(id: int, plan: PlanUpdateSchema):
#     db_plan =  db.session.query(PlanModel).filter(PlanModel.id == id).first()
#     if not db_plan:
#         raise HTTPException(status_code=400, detail="Invalid Plan")
    
#     plans_check =  db.session.query(PlanModel).filter(PlanModel.name == plan.name).first()
#     if plans_check:
#         raise HTTPException(status_code=400, detail="Plan Name already exists")
    
#     db_plan.name = plan.name
#     db_plan.price = plan.price
#     db_plan.billing_cycle = plan.billing_cycle
#     db_plan.page_list_limit = plan.page_list_limit
#     db_plan.api_list_limit = plan.api_list_limit
#     db_plan.users_limit = plan.users_limit
#     db_plan.storage_limit = plan.storage_limit
#     db_plan.status = plan.status

#     db.session.commit()
#     db.session.refresh(db_plan)
#     return db_plan

# # Delete Plan
# @router.delete("/plans/{plan_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_superadmin_user)])
# def delete_plan(id: int, current_user = Depends(get_current_superadmin_user)):

#     # Only Super Admin can delete Plans
#     if current_user.role != USER_ROLES.SUPERADMIN: 
#         raise HTTPException(status_code=401, detail="Not Autherized")
    
#     db_plan =  db.session.query(PlanModel).filter(PlanModel.id == id).first()
#     if not db_plan:
#         raise HTTPException(status_code=400, detail="Invalid Plan")
    
#     db.session.delete(db_plan)
#     db.session.commit()

#     return None