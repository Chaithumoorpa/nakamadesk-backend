from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import SessionLocal
from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.models.item import Item
from app.schemas.sale import SaleCreate, SaleResponse
from app.api.auth import get_db, get_current_user

router = APIRouter(prefix="/sales", tags=["Sales"])

@router.post("/", response_model=SaleResponse)
def create_sale(
    sale_data: SaleCreate,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not sale_data.items:
        raise HTTPException(status_code=400, detail="Sale must contain at least one item")

    total_amount = 0.0
    
    new_sale = Sale(total_amount=0.0)
    db.add(new_sale)
    db.flush()

    for item_data in sale_data.items:
        if item_data.quantity <= 0:
            db.rollback()
            raise HTTPException(status_code=400, detail="Quantity must be greater than zero")

        item = db.query(Item).filter(Item.id == item_data.item_id).first()
        if not item:
            db.rollback()
            raise HTTPException(status_code=404, detail=f"Item with ID {item_data.item_id} not found")
        
        current_stock = item.stock_quantity or 0
        if current_stock < item_data.quantity:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Insufficient stock for item '{item.name}'")
        
        item.stock_quantity = current_stock - item_data.quantity
        
        price_at_sale = item.price or 0.0
        total_amount += price_at_sale * item_data.quantity
        
        sale_item = SaleItem(
            sale_id=new_sale.id,
            item_id=item.id,
            quantity=item_data.quantity,
            price_at_sale=price_at_sale
        )
        db.add(sale_item)
    
    new_sale.total_amount = total_amount
    db.commit()
    db.refresh(new_sale)
    return new_sale

@router.get("/", response_model=List[SaleResponse])
def get_sales(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    sales = db.query(Sale).all()
    return sales

@router.get("/{sale_id}", response_model=SaleResponse)
def get_sale(
    sale_id: int,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale
