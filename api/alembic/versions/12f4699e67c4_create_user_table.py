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
from models import USER_ROLES
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
        sa.Column('phone_no', sa.String(length=15), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=False),
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
        sa.Column('language', sa.String(length=2), nullable=True),
        sa.Column('timezone', sa.String(30), nullable=True),
        sa.Column('role', ENUM(USER_ROLES, name="role"), nullable=False, default=USER_ROLES.USER),
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
                "email": "sadmin@martech.com",
                "hashed_password": pwd_context.hash("Admin@123"),
                "phone_no": "9999911111",
                "is_active": True,
                "language": 'EN',
                "timezone": pytz.country_timezones['IT'][0],
                "role": USER_ROLES.SUPERADMIN
            },
            {
                "id": uuid.uuid4(),
                "first_name": "Test 1",
                "last_name": "Admin",
                "email": "admin1@martech.com",
                "hashed_password": pwd_context.hash("Admin@123"),
                "phone_no": "9999922222",
                "is_active": True,
                "language": 'EN',
                "timezone": pytz.country_timezones['IT'][0],
                "role": USER_ROLES.ADMIN
            },
            {
                "id": uuid.uuid4(),
                "first_name": "Test 2",
                "last_name": "Admin",
                "email": "admin2@martech.com",
                "hashed_password": pwd_context.hash("Admin@123"),
                "phone_no": "9999933333",
                "is_active": True,
                "language": 'EN',
                "timezone": pytz.country_timezones['IT'][0],
                "role": USER_ROLES.ADMIN
            },
            {
                "id": uuid.uuid4(),
                "first_name": "Test 1",
                "last_name": "User",
                "email": "user1@martech.com",
                "hashed_password": pwd_context.hash("Admin@123"),
                "phone_no": "9999944444",
                "is_active": True,
                "language": 'EN',
                "timezone": pytz.country_timezones['IT'][0],
                "role": USER_ROLES.USER
            },
            {
                "id": uuid.uuid4(),
                "first_name": "Test 2",
                "last_name": "User",
                "email": "user2@martech.com",
                "hashed_password": pwd_context.hash("Admin@123"),
                "phone_no": "9999955555",
                "is_active": True,
                "language": 'EN',
                "timezone": pytz.country_timezones['IT'][0],
                "role": USER_ROLES.USER
            },
            {
                "id": uuid.uuid4(),
                "first_name": "Test 3",
                "last_name": "User",
                "email": "user3@martech.com",
                "hashed_password": pwd_context.hash("Admin@123"),
                "phone_no": "9999966666",
                "is_active": True,
                "language": 'EN',
                "timezone": pytz.country_timezones['IT'][0],
                "role": USER_ROLES.USER
            },

        ],
    )


def downgrade() -> None:
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    op.execute('DROP TYPE role;')
