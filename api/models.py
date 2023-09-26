from sqlalchemy import UUID, Boolean, String, ForeignKey, Integer, Date, Float, DateTime, Column, Enum
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Relationship
from sqlalchemy.sql import func
import enum
import uuid

class Base(DeclarativeBase):
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class ROLES(str, enum.Enum):
    SUPERADMIN = 'SUPERADMIN'
    ADMNIN = 'ADMIN'
    USER = 'USER'

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    first_name = Column(String(30))
    last_name = Column(String(30))
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    phone_no = Column(String(15))
    is_active = Column(Boolean, default=False)
    last_login = Column(DateTime(timezone=True))
    language = Column(String(2))
    timezone = Column(String(30))
    role = Column(Enum(ROLES), default=ROLES.USER)
    # TODO Permissions/Groups
    

