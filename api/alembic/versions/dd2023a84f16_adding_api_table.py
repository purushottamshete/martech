"""Adding api table

Revision ID: dd2023a84f16
Revises: ca75f1e42106
Create Date: 2023-09-26 18:17:04.838052

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision: str = 'dd2023a84f16'
down_revision: Union[str, None] = 'ca75f1e42106'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    apis_table = op.create_table('apis',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('name', sa.String(length=30), nullable=False, unique=True),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=func.now()),
        sa.Column('updated_at', sa.DateTime,onupdate=func.now()),
    )
    op.create_index(op.f('ix_apis_id'), 'apis', ['id'], unique=True)
    op.bulk_insert(
        apis_table,
        [
            {
                "name": "api1",
                "description": "Test Api 1",
            },
            {
                "name": "api2",
                "description": "Test Api 2",
            },
            {
                "name": "api3",
                "description": "Test Api 3",
            },

        ],
    )

def downgrade() -> None:
    op.drop_index(op.f('ix_apis_id'), table_name='apis')
    op.drop_table('apis')
    
