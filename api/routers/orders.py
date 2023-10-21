from fastapi import APIRouter, Depends, Body, HTTPException, status
import logging
from models import Order as OrderModel, ORDER_STATUS, PAYMENT_METHODS, PAYMENT_STATUS
from .auth import get_current_active_user, get_current_superadmin_user, get_current_admin_user
from schema import OrderInDB as OrderInDBSchema, OrderUpdate as OrderUpdateSchema
from schema import Order as OrderSchema
from typing import List
from fastapi_sqlalchemy import db
from datetime import datetime
import pytz
from uuid import UUID 
from models import USER_ROLES, User as UserModel, Plan as PlanModel

logger = logging.getLogger(__name__)
router = APIRouter()

# Get Orders
@router.get("/orders/", dependencies=[Depends(get_current_active_user)], response_model=List[OrderInDBSchema])
async def get_orders(current_user = Depends(get_current_active_user)):
    # Super Admin can view all the order
    if current_user.role == USER_ROLES.SUPERADMIN:
        orders =  db.session.query(OrderModel).order_by(OrderModel.created_at).all()
    else:
        orders =  db.session.query(OrderModel).filter(OrderModel.user_id == current_user.id).order_by(OrderModel.created_at).all()
    return orders


# Get Orders for a User
@router.get("/orders/{user_id}", dependencies=[Depends(get_current_admin_user)], response_model=List[OrderInDBSchema])
async def get_user_orders(user_id: UUID):
    db_user =  db.session.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        logger.exception("Inactive user")
        raise HTTPException(status_code=400, detail="Invalid User")
    
    user_orders =  db.session.query(OrderModel).filter(OrderModel.user_id == db_user.id).order_by(OrderModel.created_at.desc()).all()
    return user_orders
       

# Create Orders
@router.post("/orders/", dependencies=[Depends(get_current_active_user)], response_model=OrderInDBSchema)
async def create_order(order: OrderSchema, current_user = Depends(get_current_active_user)):

    db_user =  db.session.query(UserModel).filter(UserModel.id == order.user_id).first()
    if not db_user:
        logger.exception("Invalid user")
        raise HTTPException(status_code=400, detail="Invalid User")
    
    db_plan =  db.session.query(PlanModel).filter(PlanModel.id == order.plan_id).first()
    if not db_plan:
        logger.exception("Invalid user")
        raise HTTPException(status_code=400, detail="Invalid Plan")
    
    if order.payment_status == PAYMENT_STATUS.PROCESSING:
        ord_status = ORDER_STATUS.CREATED
    elif order.payment_status == PAYMENT_STATUS.PAYMENT_FAILED: 
        ord_status = ORDER_STATUS.FAILED
    elif order.payment_status == PAYMENT_STATUS.SUCCEEDED:
        ord_status = ORDER_STATUS.SUCCESS
    else:
        logger.exception("Invalid Payment Status")
        raise HTTPException(status_code=400, detail="Invlaid Payment Status")

    try:
        if current_user.timezone:
            tz = pytz.timezone(current_user.timezone)
        else:
            tz = pytz.UTC
    except Exception as e:
        logger.exception("Invalid Timezone")
        tz = pytz.UTC
    
    db_order = OrderModel(  user_id=order.user_id, 
                            plan_id=order.plan_id, 
                            date_time=datetime.now(tz=tz),
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

# Update Order
@router.put("/orders/{order_id}", dependencies=[Depends(get_current_active_user)], response_model=OrderInDBSchema)
def update_order(order_id: UUID, order: OrderSchema, current_user = Depends(get_current_active_user)):
    db_order =  db.session.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not db_order:
        logger.exception("Invalid Order")
        raise HTTPException(status_code=400, detail="Invalid Order")
    
    # Super Admin Allowed to update all orders
    if current_user.role == USER_ROLES.SUPERADMIN:
        pass
    else:
        # Others allowed to update own order only
        if current_user.id != db_order.user_id:
            logger.exception("Not Autherized to update this order")
            raise HTTPException(status_code=401, detail="Not Autherized to update this order")
        
    db_user =  db.session.query(UserModel).filter(UserModel.id == order.user_id).first()
    if not db_user:
        logger.exception("Not Autherized to update this order")
        raise HTTPException(status_code=400, detail="Invalid User")
    
    db_plan =  db.session.query(PlanModel).filter(PlanModel.id == order.plan_id).first()
    if not db_plan:
        logger.exception("Invalid Plan")
        raise HTTPException(status_code=400, detail="Invalid Plan")
    
    if order.payment_status == PAYMENT_STATUS.PROCESSING:
        ord_status = ORDER_STATUS.CREATED
    elif order.payment_status == PAYMENT_STATUS.PAYMENT_FAILED: 
        ord_status = ORDER_STATUS.FAILED
    elif order.payment_status == PAYMENT_STATUS.SUCCEEDED:
        ord_status = ORDER_STATUS.SUCCESS
    else:
        logger.exception("Invlaid Payment Status")
        raise HTTPException(status_code=400, detail="Invlaid Payment Status")

    db_order.user_id = order.user_id
    db_order.plan_id = order.plan_id
    db_order.payment_method = order.payment_method
    db_order.payment_status = order.payment_status
    db_order.invoice_id = order.invoice_id
    db_order.billing_address = order.billing_address
    db_order.status = ord_status

    db.session.commit()
    db.session.refresh(db_order)
    return db_order

# Delete Order
@router.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_superadmin_user)])
def delete_order(order_id: UUID, current_user = Depends(get_current_superadmin_user)):

    # Only Super Admin can delete Orders
    if current_user.role != USER_ROLES.SUPERADMIN: 
        logger.exception("Not Autherized")
        raise HTTPException(status_code=401, detail="Not Autherized")
    
    db_order =  db.session.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not db_order:
        logger.exception("Invalid Order")
        raise HTTPException(status_code=400, detail="Invalid Order")
    
    db.session.delete(db_order)
    db.session.commit()

    return None