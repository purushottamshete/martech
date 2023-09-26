"""Adding Page table

Revision ID: 590bad289ad5
Revises: dd2023a84f16
Create Date: 2023-09-26 18:24:49.062288

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision: str = '590bad289ad5'
down_revision: Union[str, None] = 'dd2023a84f16'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pages_table = op.create_table('pages',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('name', sa.String(length=30), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=func.now()),
        sa.Column('updated_at', sa.DateTime,onupdate=func.now()),
    )
    op.create_index(op.f('ix_pages_id'), 'pages', ['id'], unique=True)
    op.bulk_insert(
        pages_table,
        [
            {
                "id": 1,
                "name": "page1",
                "description": "Test Page 1",
            },
            {
                "id": 2,
                "name": "page2",
                "description": "Test Page 2",
            },
            {
                "id": 3,
                "name": "page3",
                "description": "Test Page 3",
            },

        ],
    )


def downgrade() -> None:
    op.drop_index(op.f('ix_pages_id'), table_name='pages')
    op.drop_table('pages')
