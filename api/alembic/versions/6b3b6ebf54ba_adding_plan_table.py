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
        sa.Column('name', sa.String(length=30), nullable=False, unique=True),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('billing_cycle', sa.Integer(), nullable=False),
        sa.Column('page_list_limit', sa.String(), nullable=False),
        sa.Column('api_list_limit', sa.String(), nullable=False),
        sa.Column('users_limit', sa.Integer(), nullable=False),
        sa.Column('storage_limit', sa.Float(), nullable=False),
        sa.Column('status', ENUM(PLAN_STATUS, name='status'), nullable=False, default=PLAN_STATUS.DISABLED),
        sa.Column('created_at', sa.DateTime, server_default=func.now()),
        sa.Column('updated_at', sa.DateTime,onupdate=func.now())
    )
    op.create_index(op.f('ix_plans_id'), 'plans', ['id'], unique=True)
    op.bulk_insert(
        plans_table,
        [
            {
                "name": "Basic",
                "price": 199,
                "page_list_limit": "page1,page2,page3,page4",
                "api_list_limit": "api,api2,api3,page4",
                "users_limit": 4,
                "storage_limit": 1.0,
                "billing_cycle": 28,
                "status": PLAN_STATUS.ACTIVE
            },
            {
                "name": "Starter",
                "price": 269,
                "page_list_limit": "page1,page2,page3,page4,page5,page6",
                "api_list_limit": "api,api2,api3,page4,api5,api6",
                "users_limit": 6,
                "storage_limit": 1.5,
                "billing_cycle": 28,
                "status": PLAN_STATUS.ACTIVE
            },
            {
                "name": "Advanced",
                "price": 449,
                "page_list_limit": "page1,page2,page3,page4,page5,page6,page7,page8",
                "api_list_limit": "api,api2,api3,page4,api5,api6,api7,api8",
                "users_limit": 8,
                "storage_limit": 2.0,
                "billing_cycle": 28,
                "status": PLAN_STATUS.ACTIVE
            },

        ],
    )


def downgrade() -> None:
    op.drop_index(op.f('ix_plans_id'), table_name='plans')
    op.drop_table('plans')
    op.execute('DROP TYPE status;')
