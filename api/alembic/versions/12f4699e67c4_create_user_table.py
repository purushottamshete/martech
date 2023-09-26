"""Create User Table

Revision ID: 12f4699e67c4
Revises: 
Create Date: 2023-09-26 15:01:08.385738

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID, ENUM
import uuid
import pytz
from models import ROLES

# revision identifiers, used by Alembic.
revision: str = '12f4699e67c4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    users_table = op.create_table('users',
        sa.Column('id', UUID(), primary_key=True, nullable=False),
        sa.Column('first_name', sa.String(length=30), nullable=False),
        sa.Column('last_name', sa.String(length=30), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('phone_no', sa.String(length=15), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=False),
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
        sa.Column('language', sa.String(length=2), nullable=False),
        sa.Column('timezone', sa.String(30), nullable=False),
        sa.Column('role', ENUM(ROLES, name="role"), nullable=False, default=ROLES.USER),
        sa.Column('created_at', sa.DateTime, server_default=func.now()),
        sa.Column('updated_at', sa.DateTime,onupdate=func.now()),
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=True)
    op.bulk_insert(
        users_table,
        [
            {
                "id": uuid.uuid4(),
                "first_name": "Super",
                "last_name": "Admin",
                "email": "contact@martech",
                "hashed_password": "Admin@123",
                "phone_no": "9999911111",
                "is_active": True,
                "language": 'EN',
                "timezone": pytz.country_timezones['IT'][0],
                "role": ROLES.SUPERADMIN
            },

        ],
    )


def downgrade() -> None:
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
