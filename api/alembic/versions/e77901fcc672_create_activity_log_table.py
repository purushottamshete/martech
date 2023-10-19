"""Create Activity_Log Table

Revision ID: e77901fcc672
Revises: da4667847e00
Create Date: 2023-10-10 19:28:10.842978

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func
from models import ACTIVITY_TYPE
from sqlalchemy.dialects.postgresql import UUID, ENUM

# revision identifiers, used by Alembic.
revision: str = 'e77901fcc672'
down_revision: Union[str, None] = 'da4667847e00'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    activity_log_table = op.create_table('activity_log',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", UUID(), sa.ForeignKey("users.id")),
        sa.Column('activity_type', ENUM(ACTIVITY_TYPE, name='activity_type'), nullable=False),
        sa.Column('activity_desc', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=func.now()),
        sa.Column('updated_at', sa.DateTime,onupdate=func.now()),
    )
    op.create_index(op.f('ix_activity_log_id'), 'activity_log', ['id'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_activity_log_id'), table_name='activity_log')
    op.drop_table('activity_log')
    op.execute('DROP TYPE activity_type;')
