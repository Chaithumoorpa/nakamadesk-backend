from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.purchase import Purchase
from app.models.purchase_item import PurchaseItem
from app.models.supplier import Supplier
from app.models.item import Item
from app.schemas.purchase import PurchaseCreate, PurchaseResponse
from app.api.auth import get_db, get_current_user

router = APIRouter(prefix="/purchases", tags=["Purchases"])

@router.post("/", response_model=PurchaseResponse)
def create_purchase(
    purchase_data: PurchaseCreate,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Validate supplier exists
    supplier = db.query(Supplier).filter(Supplier.id == purchase_data.supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")

    if not purchase_data.items:
        raise HTTPException(status_code=400, detail="Purchase must contain at least one item")

    new_purchase = Purchase(supplier_id=purchase_data.supplier_id, total_amount=0.0)
    db.add(new_purchase)
    db.flush()

    total_amount = 0.0

    for item_data in purchase_data.items:
        if item_data.quantity <= 0:
            db.rollback()
            raise HTTPException(status_code=400, detail="Quantity must be greater than zero")

        item = db.query(Item).filter(Item.id == item_data.item_id).first()
        if not item:
            db.rollback()
            raise HTTPException(status_code=404, detail=f"Item with ID {item_data.item_id} not found")

        # Increase inventory stock
        item.stock_quantity = (item.stock_quantity or 0) + item_data.quantity

        total_amount += item_data.cost_price * item_data.quantity

        purchase_item = PurchaseItem(
            purchase_id=new_purchase.id,
            item_id=item.id,
            quantity=item_data.quantity,
            cost_price=item_data.cost_price
        )
        db.add(purchase_item)

    new_purchase.total_amount = total_amount
    db.commit()
    db.refresh(new_purchase)
    return new_purchase

@router.get("/", response_model=List[PurchaseResponse])
def get_purchases(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Purchase).all()

@router.get("/{purchase_id}", response_model=PurchaseResponse)
def get_purchase(
    purchase_id: int,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    purchase = db.query(Purchase).filter(Purchase.id == purchase_id).first()
    if not purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")
    return purchase
