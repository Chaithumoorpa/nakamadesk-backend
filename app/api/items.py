from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import SessionLocal
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemResponse
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
