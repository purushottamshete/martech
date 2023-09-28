"""Adding Plan Page Limit table

Revision ID: e7b23087467e
Revises: 590bad289ad5
Create Date: 2023-09-28 12:05:55.679188

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision: str = 'e7b23087467e'
down_revision: Union[str, None] = '590bad289ad5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    plan_page_limit_table = op.create_table('plan_page_limit',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column("plan_id", sa.INTEGER, sa.ForeignKey("plans.id")),
        sa.Column("page_id", sa.INTEGER, sa.ForeignKey("pages.id")),
        sa.Column('limit', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=func.now()),
        sa.Column('updated_at', sa.DateTime,onupdate=func.now()),
    )
    op.create_index(op.f('ix_plan_page_limit_id'), 'plan_page_limit', ['id'], unique=True)
    op.bulk_insert(
        plan_page_limit_table,
        [
            {
                "id": 1,
                "plan_id": 1,
                "page_id": 1,
                "limit": 100,
            },
            {
                "id": 2,
                "plan_id": 1,
                "page_id": 2,
                "limit": 100,
            },
            {
                "id": 3,
                "plan_id": 1,
                "page_id": 3,
                "limit": 100,
            },
            {
                "id": 4,
                "plan_id": 2,
                "page_id": 1,
                "limit": 100,
            },
            {
                "id": 5,
                "plan_id": 2,
                "page_id": 2,
                "limit": 100,
            },
            {
                "id": 6,
                "plan_id": 2,
                "page_id": 3,
                "limit": 100,
            },
            {
                "id": 7,
                "plan_id": 3,
                "page_id": 1,
                "limit": 100,
            },
            {
                "id": 8,
                "plan_id": 3,
                "page_id": 2,
                "limit": 100,
            },
            {
                "id": 9,
                "plan_id": 3,
                "page_id": 3,
                "limit": 100,
            },

        ],
    )

def downgrade() -> None:
    op.drop_index(op.f('ix_plan_page_limit_id'), table_name='plan_page_limit')
    op.drop_table('plan_page_limit')
