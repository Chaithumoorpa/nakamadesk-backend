from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import SessionLocal
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemResponse
from app.schemas.stock import StockUpdate
from app.api.auth import get_db, get_current_user

router = APIRouter(prefix="/items", tags=["Items"])

@router.post("/", response_model=ItemResponse)
def create_item(
    item: ItemCreate,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_item = Item(**item.model_dump())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@router.get("/", response_model=List[ItemResponse])
def get_items(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    items = db.query(Item).all()
    return items

@router.get("/{item_id}", response_model=ItemResponse)
def get_item(
    item_id: int,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: int,
    item_data: ItemCreate,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    for key, value in item_data.model_dump().items():
        setattr(item, key, value)
    
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{item_id}")
def delete_item(
    item_id: int,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(item)
    db.commit()
    return {"message": "Item deleted successfully"}

@router.patch("/{item_id}/stock", response_model=ItemResponse)
def adjust_stock(
    item_id: int,
    stock_update: StockUpdate,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    item.stock_quantity = (item.stock_quantity or 0) + stock_update.quantity
    
    db.commit()
    db.refresh(item)
    return item
