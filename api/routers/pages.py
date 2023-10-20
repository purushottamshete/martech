from fastapi import APIRouter, Depends, HTTPException, status
import logging
from models import Page as PageModel
from .auth import get_current_superadmin_user
from schema import PageInDB as PageInDBSchema
from schema import Page as PageSchema
from typing import List
from fastapi_sqlalchemy import db

logger = logging.getLogger(__name__)
router = APIRouter()

# Get Pages
@router.get("/pages/", dependencies=[Depends(get_current_superadmin_user)], response_model=List[PageInDBSchema])
async def get_pages():
    pages =  db.session.query(PageModel).order_by(PageModel.created_at).all()
    return pages

# Create Page
@router.post("/pages/", dependencies=[Depends(get_current_superadmin_user)], response_model=PageInDBSchema)
async def create_page(page: PageSchema):

    page_check =  db.session.query(PageModel).filter(PageModel.name == page.name).first()
    if page_check:
        raise HTTPException(status_code=400, detail="Page already exists")

    db_page = PageModel(  name=page.name, 
                        description=page.description )
    db.session.add(db_page)
    db.session.commit()
    db.session.refresh(db_page)
    return db_page

# Update Page
@router.put("/pages/{page_id}", dependencies=[Depends(get_current_superadmin_user)], response_model=PageInDBSchema)
def update_page(page_id: int, page: PageSchema):
    db_page =  db.session.query(PageModel).filter(PageModel.id == page_id).first()
    if not db_page:
        raise HTTPException(status_code=400, detail="Invalid Page")
    
    if db_page.name != page.name:
        page_check =  db.session.query(PageModel).filter(PageModel.name == page.name).first()
        if page_check:
            raise HTTPException(status_code=400, detail="Page already exists")
    
    db_page.name = page.name
    db_page.description = page.description
    
    db.session.commit()
    db.session.refresh(db_page)
    return db_page

# Delete Page
@router.delete("/pages/{page_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_superadmin_user)])
def delete_page(page_id: int):
 
    db_page =  db.session.query(PageModel).filter(PageModel.id == page_id).first()
    if not db_page:
        raise HTTPException(status_code=400, detail="Invalid Page")
    
    db.session.delete(db_page)
    db.session.commit()

    return None