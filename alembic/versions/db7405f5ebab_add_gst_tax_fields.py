"""add gst tax fields

Revision ID: db7405f5ebab
Revises: 
Create Date: 2026-03-08 19:50:45.120850

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'db7405f5ebab'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add GST and HSN fields to items and sale_items tables."""

    # Add hsn_code and gst_percent columns to items table
    op.add_column('items', sa.Column('hsn_code', sa.String(), nullable=True))
    op.add_column('items', sa.Column('gst_percent', sa.Float(), nullable=True, server_default='0.0'))

    # Add GST tax result columns to sale_items table
    op.add_column('sale_items', sa.Column('gst_percent', sa.Float(), nullable=True, server_default='0.0'))
    op.add_column('sale_items', sa.Column('cgst_amount', sa.Float(), nullable=True, server_default='0.0'))
    op.add_column('sale_items', sa.Column('sgst_amount', sa.Float(), nullable=True, server_default='0.0'))
    op.add_column('sale_items', sa.Column('total_price', sa.Float(), nullable=True, server_default='0.0'))


def downgrade() -> None:
    """Remove GST and HSN fields."""

    # Remove from sale_items
    op.drop_column('sale_items', 'total_price')
    op.drop_column('sale_items', 'sgst_amount')
    op.drop_column('sale_items', 'cgst_amount')
    op.drop_column('sale_items', 'gst_percent')

    # Remove from items
    op.drop_column('items', 'gst_percent')
    op.drop_column('items', 'hsn_code')
