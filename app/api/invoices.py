from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.sale import Sale
from app.schemas.invoice import InvoiceResponse, InvoiceItemResponse
from app.db.deps import get_db
from app.api.auth import get_current_user

router = APIRouter(prefix="/invoices", tags=["Invoices"])

@router.get("/", response_model=List[InvoiceResponse])
def list_invoices(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    sales = db.query(Sale).filter(Sale.invoice_number.isnot(None)).all()
    
    invoices = []
    for sale in sales:
        invoice_items = []
        for si in sale.items:
            invoice_items.append(
                InvoiceItemResponse(
                    item_id=si.item_id,
                    item_name=si.item.name if si.item else "Unknown Item",
                    quantity=si.quantity,
                    price_at_sale=si.price_at_sale,
                    gst_percent=si.gst_percent,
                    cgst_amount=si.cgst_amount,
                    sgst_amount=si.sgst_amount,
                    total_price=si.total_price
                )
            )
        
        invoices.append(
            InvoiceResponse(
                id=sale.id,
                invoice_number=sale.invoice_number,
                invoice_date=sale.invoice_date,
                total_amount=sale.total_amount,
                customer=sale.customer,
                items=invoice_items
            )
        )
    return invoices

@router.get("/{invoice_number}", response_model=InvoiceResponse)
def get_invoice(
    invoice_number: str,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    sale = db.query(Sale).filter(Sale.invoice_number == invoice_number).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Invoice not found")
        
    invoice_items = []
    for si in sale.items:
        invoice_items.append(
            InvoiceItemResponse(
                item_id=si.item_id,
                item_name=si.item.name if si.item else "Unknown Item",
                quantity=si.quantity,
                price_at_sale=si.price_at_sale,
                gst_percent=si.gst_percent,
                cgst_amount=si.cgst_amount,
                sgst_amount=si.sgst_amount,
                total_price=si.total_price
            )
        )
    
    return InvoiceResponse(
        id=sale.id,
        invoice_number=sale.invoice_number,
        invoice_date=sale.invoice_date,
        total_amount=sale.total_amount,
        customer=sale.customer,
        items=invoice_items
    )

from fastapi.responses import FileResponse
from app.services.invoice_pdf_service import generate_invoice_pdf
import os

@router.get("/{invoice_number}/pdf")
def get_invoice_pdf(
    invoice_number: str,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    sale = db.query(Sale).filter(Sale.invoice_number == invoice_number).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Invoice not found")
        
    pdf_path = generate_invoice_pdf(sale)
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=500, detail="Failed to generate PDF")
        
    return FileResponse(
        pdf_path, 
        media_type="application/pdf", 
        filename=os.path.basename(pdf_path)
    )
