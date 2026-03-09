from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
from app.models.sale import Sale

def generate_invoice_number(db: Session) -> str:
    """
    Generate a unique invoice number in the format NTD-YYYY-XXXXX
    Example: NTD-2026-00001
    """
    current_year = datetime.now().year
    
    # Prefix for this year
    prefix = f"NTD-{current_year}-"
    
    # Find the latest sale for this year
    latest_sale = db.query(Sale).filter(
        Sale.invoice_number.like(f"{prefix}%")
    ).order_by(desc(Sale.id)).first()
    
    if latest_sale and latest_sale.invoice_number:
        # Extract the sequence number
        try:
            seq_str = latest_sale.invoice_number.split("-")[-1]
            next_seq = int(seq_str) + 1
        except (ValueError, IndexError):
            next_seq = 1
    else:
        next_seq = 1
        
    return f"{prefix}{next_seq:05d}"
