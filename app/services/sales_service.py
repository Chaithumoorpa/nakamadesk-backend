import logging
from typing import Dict, List, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from app.models.item import Item
from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.schemas.sale import SaleCreate, SaleItemCreate
from app.services.invoice_service import generate_invoice_number
from app.utils.money import to_decimal

logger = logging.getLogger(__name__)


def create_sale_transaction(
    db: Session, sale_data: SaleCreate, current_user: str
) -> Sale:
    """Handles the business logic for creating a sale, verifying stock, and calculating GST."""

    if not sale_data.items:
        raise HTTPException(
            status_code=400, detail="Sale must contain at least one item"
        )

    # Group requested items
    item_requests: Dict[int, SaleItemCreate] = {}
    for item_data in sale_data.items:
        if item_data.quantity <= 0:
            raise HTTPException(
                status_code=400, detail="Quantity must be greater than zero"
            )
        if item_data.item_id in item_requests:
            item_requests[item_data.item_id].quantity += item_data.quantity
        else:
            item_requests[item_data.item_id] = item_data

    # Fetch all items in a single query
    item_ids = list(item_requests.keys())
    items = db.query(Item).filter(Item.id.in_(item_ids)).all()
    items_map = {item.id: item for item in items}

    # Verify all items exist
    for item_id in item_ids:
        if item_id not in items_map:
            raise HTTPException(
                status_code=404, detail=f"Item with ID {item_id} not found"
            )

    new_sale = Sale(
        total_amount=0.0,
        invoice_number=generate_invoice_number(db),
        customer_id=sale_data.customer_id,
    )
    db.add(new_sale)
    db.flush()

    total_amount = to_decimal(0)

    for item_id, req_data in item_requests.items():
        item = items_map[item_id]

        current_stock = item.stock_quantity or 0
        if current_stock < req_data.quantity:
            db.rollback()
            raise HTTPException(
                status_code=400, detail=f"Insufficient stock for item '{item.name}'"
            )

        # Deduct stock
        item.stock_quantity = current_stock - req_data.quantity

        price_at_sale = to_decimal(item.price)
        gst_percent = to_decimal(item.gst_percent)
        quantity = to_decimal(req_data.quantity)

        base_price = price_at_sale * quantity
        gst_amount = base_price * (gst_percent / to_decimal(100))
        cgst_amount = gst_amount / to_decimal(2)
        sgst_amount = gst_amount / to_decimal(2)
        line_total = base_price + gst_amount

        total_amount += line_total

        sale_item = SaleItem(
            sale_id=new_sale.id,
            item_id=item.id,
            quantity=req_data.quantity,
            price_at_sale=float(price_at_sale),
            gst_percent=float(gst_percent),
            cgst_amount=float(cgst_amount),
            sgst_amount=float(sgst_amount),
            total_price=float(line_total),
        )
        db.add(sale_item)

    new_sale.total_amount = float(total_amount)
    db.commit()
    db.refresh(new_sale)

    logger.info(f"Sale created: {new_sale.id} with invoice {new_sale.invoice_number}")
    return new_sale


def get_all_sales(
    db: Session, 
    limit: int = 50, 
    offset: int = 0, 
    customer_id: Optional[int] = None, 
    date: Optional[str] = None
) -> List[Sale]:
    """Retrieve paginated sales with optional filtering and eager loading of items."""
    query = db.query(Sale).options(joinedload(Sale.items).joinedload(SaleItem.item))
    
    if customer_id:
        query = query.filter(Sale.customer_id == customer_id)
    
    if date:
        from datetime import datetime
        from sqlalchemy import func
        try:
            target_date = datetime.strptime(date, "%Y-%m-%d").date()
            query = query.filter(func.date(Sale.created_at) == target_date)
        except ValueError:
            # Note: We might want to handle this differently in a service, 
            # but for now we follow the existing pattern of raising in the route if needed.
            # Here we just pass it along or ignore invalid dates.
            pass

    sales = query.limit(limit).offset(offset).all()
    return sales


def get_sale_by_id(db: Session, sale_id: int) -> Optional[Sale]:
    """Retrieve a single sale by ID."""
    sale = (
        db.query(Sale)
        .options(joinedload(Sale.items).joinedload(SaleItem.item))
        .filter(Sale.id == sale_id)
        .first()
    )
    return sale
