"""Adding Subscription Table

Revision ID: da4667847e00
Revises: 590bad289ad5
Create Date: 2023-09-28 13:18:44.558064

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision: str = 'da4667847e00'
down_revision: Union[str, None] = '590bad289ad5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    subscription_table = op.create_table('subscriptions',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", UUID(), sa.ForeignKey("users.id")),
        sa.Column("plan_id", sa.INTEGER, sa.ForeignKey("plans.id")),
        sa.Column('trial_period', sa.Integer(), nullable=False),
        sa.Column('discount', sa.Float(), nullable=False),
        sa.Column('start_date', sa.DateTime, server_default=func.now()),
        sa.Column('end_date', sa.DateTime),
        sa.Column('created_at', sa.DateTime, server_default=func.now()),
        sa.Column('updated_at', sa.DateTime,onupdate=func.now()),
    )
    op.create_index(op.f('ix_subscriptions_id'), 'subscriptions', ['id'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_subscriptions_id'), table_name='subscriptions')
    op.drop_table('subscriptions')
