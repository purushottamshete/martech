"""Adding plan table

Revision ID: 6b3b6ebf54ba
Revises: 12f4699e67c4
Create Date: 2023-09-26 16:29:36.195607

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import ENUM
from models import PLAN_STATUS

# revision identifiers, used by Alembic.
revision: str = '6b3b6ebf54ba'
down_revision: Union[str, None] = '12f4699e67c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    plans_table = op.create_table('plans',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('name', sa.String(length=30), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('billing_cycle', sa.Integer(), nullable=False),
        sa.Column('trial_period', sa.Integer(), nullable=True),
        sa.Column('discount', sa.Float(), nullable=True),
        sa.Column('status', ENUM(PLAN_STATUS, name='status'), nullable=False, default=PLAN_STATUS.ACTIVE),
        sa.Column('created_at', sa.DateTime, server_default=func.now()),
        sa.Column('updated_at', sa.DateTime,onupdate=func.now()),
    )
    op.create_index(op.f('ix_plans_id'), 'plans', ['id'], unique=True)
    op.bulk_insert(
        plans_table,
        [
            {
                "id": 1,
                "name": "Basic",
                "price": 199,
                "billing_cycle": 28,
            },
            {
                "id": 2,
                "name": "Starter",
                "price": 269,
                "billing_cycle": 28,
            },
            {
                "id": 3,
                "name": "Advanced",
                "price": 449,
                "billing_cycle": 28,
            },

        ],
    )


def downgrade() -> None:
    op.drop_index(op.f('ix_plans_id'), table_name='plans')
    op.drop_table('plans')
    op.execute('DROP TYPE status;')
