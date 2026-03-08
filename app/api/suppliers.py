from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.supplier import Supplier
from app.schemas.supplier import SupplierCreate, SupplierUpdate, SupplierResponse
from app.api.auth import get_db, get_current_user

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])

@router.post("/", response_model=SupplierResponse)
def create_supplier(
    supplier: SupplierCreate,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_supplier = Supplier(**supplier.model_dump())
    db.add(new_supplier)
    db.commit()
    db.refresh(new_supplier)
    return new_supplier

@router.get("/", response_model=List[SupplierResponse])
def get_suppliers(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Supplier).all()

@router.get("/{supplier_id}", response_model=SupplierResponse)
def get_supplier(
    supplier_id: int,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier

@router.put("/{supplier_id}", response_model=SupplierResponse)
def update_supplier(
    supplier_id: int,
    supplier_data: SupplierUpdate,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    for key, value in supplier_data.model_dump(exclude_none=True).items():
        setattr(supplier, key, value)
    db.commit()
    db.refresh(supplier)
    return supplier

@router.delete("/{supplier_id}")
def delete_supplier(
    supplier_id: int,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    db.delete(supplier)
    db.commit()
    return {"message": "Supplier deleted successfully"}
