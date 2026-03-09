from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.db.deps import get_db
from app.schemas.sale import SaleCreate, SaleResponse
from app.services.sales_service import (create_sale_transaction, get_all_sales,
                                        get_sale_by_id)

router = APIRouter(prefix="/sales", tags=["Sales"])


@router.post("/", response_model=SaleResponse)
def create_sale(
    sale_data: SaleCreate,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_sale_transaction(db, sale_data, current_user)


@router.get("/", response_model=List[SaleResponse])
def get_sales(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_all_sales(db, limit, offset)


@router.get("/{sale_id}", response_model=SaleResponse)
def get_sale(
    sale_id: int,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    sale = get_sale_by_id(db, sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale
