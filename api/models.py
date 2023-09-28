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

class USER_ROLES(str, enum.Enum):
    SUPERADMIN = 'SUPERADMIN'
    ADMNIN = 'ADMIN'
    USER = 'USER'

class PLAN_STATUS(enum.Enum):
    ACTIVE = 1
    DISABLED = 0

class ORDER_STATUS(enum.Enum):
    CREATED = 1
    SUCCESS = 2
    FAILED = 3

class PAYMENT_METHODS(enum.Enum):
    CREDIT_CARD = 1
    ESCROW = 2
    PAISA_PAY = 3
    PAYPAL = 4
    OTHER = 5

class PAYMENT_STATUS(enum.Enum):
    CANCELED_REVERSAL = 1
    COMPLETED = 2
    CREATED = 3
    DENINED = 3
    EXPIRED = 4
    FAILED = 5
    PENDING = 6
    REFUNDED = 7
    REVERSED = 8
    PROCESSED = 9
    VOIDED = 10

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
    role = Column(Enum(USER_ROLES), default=USER_ROLES.USER)
    # TODO Permissions/Groups
    
class Plan(Base):
    __tablename__ = "plans"
    id = Column(primary_key=True, index=True)
    name = Column(String(30))
    price = Column(Float())
    billing_cycle = Column(Integer())
    page_list_limit = Column(String())
    api_list_limit = Column(String())
    users_limit = Column(Integer())
    storage_limit = Column(Integer())
    status = Column(Enum(PLAN_STATUS), default=PLAN_STATUS.ACTIVE)

class Order(Base):
    __tablename__ = "orders"
    id = Column(primary_key=True, index=True)
    user_id = Column(ForeignKey("users.id"))
    plan_id = Column(ForeignKey("plans.id"))
    date = Column(DateTime(timezone=True))
    status = Column(Enum(ORDER_STATUS), default=ORDER_STATUS.CREATED)
    payment_method = Column(Enum(PAYMENT_METHODS), nullable=True)
    payment_status = Column(Enum(PAYMENT_STATUS), nullable=True)
    invoice_id = Column(String(30))
    billing_address = Column(String())

class Api(Base):
    __tablename__ = "apis"
    id = Column(primary_key=True, index=True)
    name = Column(String(30), unique=True)
    description = Column(String())

class Page(Base):
    __tablename__ = "pages"
    id = Column(primary_key=True, index=True)
    name = Column(String(30), unique=True)
    description = Column(String())
