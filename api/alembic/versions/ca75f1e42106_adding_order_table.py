"""Adding order table

Revision ID: ca75f1e42106
Revises: 6b3b6ebf54ba
Create Date: 2023-09-26 17:31:05.327388

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func
from models import ORDER_STATUS, PAYMENT_METHODS, PAYMENT_STATUS
from sqlalchemy.dialects.postgresql import UUID, ENUM

# revision identifiers, used by Alembic.
revision: str = 'ca75f1e42106'
down_revision: Union[str, None] = '6b3b6ebf54ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    orders_table = op.create_table('orders',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", UUID(), sa.ForeignKey("users.id")),
        sa.Column("plan_id", sa.INTEGER, sa.ForeignKey("plans.id")),
        sa.Column('date', sa.DateTime, server_default=func.now()),
        sa.Column('status', ENUM(ORDER_STATUS, name='status'), nullable=False, default=ORDER_STATUS.CREATED),
        sa.Column('payment_method', ENUM(PAYMENT_METHODS, name='payment_method'), nullable=True),
        sa.Column('payment_status', ENUM(PAYMENT_STATUS, name='payment_status'), nullable=True),
        sa.Column('invoice_id', sa.String(length=30), nullable=False),
        sa.Column('billing_address', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=func.now()),
        sa.Column('updated_at', sa.DateTime,onupdate=func.now()),
    )
    op.create_index(op.f('ix_orders_id'), 'orders', ['id'], unique=True)
    

def downgrade() -> None:
    op.drop_index(op.f('ix_orders_id'), table_name='orders')
    op.drop_table('orders')
    op.execute('DROP TYPE payment_method;')
    op.execute('DROP TYPE payment_status;')
