"""Adding Plan Api Limit table

Revision ID: 379f2a61fd33
Revises: e7b23087467e
Create Date: 2023-09-28 12:21:44.974551

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision: str = '379f2a61fd33'
down_revision: Union[str, None] = 'e7b23087467e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    plan_api_limit_table = op.create_table('plan_api_limit',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column("plan_id", sa.INTEGER, sa.ForeignKey("plans.id")),
        sa.Column("api_id", sa.INTEGER, sa.ForeignKey("apis.id")),
        sa.Column('limit', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=func.now()),
        sa.Column('updated_at', sa.DateTime,onupdate=func.now()),
    )
    op.create_index(op.f('ix_plan_api_limit_id'), 'plan_api_limit', ['id'], unique=True)
    op.bulk_insert(
        plan_api_limit_table,
        [
            {
                "id": 1,
                "plan_id": 1,
                "api_id": 1,
                "limit": 100,
            },
            {
                "id": 2,
                "plan_id": 1,
                "api_id": 2,
                "limit": 100,
            },
            {
                "id": 3,
                "plan_id": 1,
                "api_id": 3,
                "limit": 100,
            },
            {
                "id": 4,
                "plan_id": 2,
                "api_id": 1,
                "limit": 100,
            },
            {
                "id": 5,
                "plan_id": 2,
                "api_id": 2,
                "limit": 100,
            },
            {
                "id": 6,
                "plan_id": 2,
                "api_id": 3,
                "limit": 100,
            },
            {
                "id": 7,
                "plan_id": 3,
                "api_id": 1,
                "limit": 100,
            },
            {
                "id": 8,
                "plan_id": 3,
                "api_id": 2,
                "limit": 100,
            },
            {
                "id": 9,
                "plan_id": 3,
                "api_id": 3,
                "limit": 100,
            },

        ],
    )

def downgrade() -> None:
    op.drop_index(op.f('ix_plan_api_limit_id'), table_name='plan_api_limit')
    op.drop_table('plan_api_limit')
