from sqlalchemy import UUID, Boolean, String, ForeignKey, Integer, Date, Float, DateTime, Column, Enum, Identity
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
    ADMIN = 'ADMIN'
    USER = 'USER'

class PLAN_STATUS(enum.Enum):
    ACTIVE = 1
    DISABLED = 2

class ORDER_STATUS(enum.Enum):
    CREATED = 1
    SUCCESS = 2
    FAILED = 3

class PAYMENT_METHODS(enum.Enum):
    CARDS = 1
    WALLETS = 2
    BANK_DEBIT = 3
    BANK_REDIRECT = 4
    BANK_TRANSFER = 5
    OTHER = 6

class PAYMENT_STATUS(enum.Enum):
    PROCESSING = 1
    SUCCEEDED = 2
    PAYMENT_FAILED = 3

class ACTIVITY_TYPE(enum.Enum):
    LOGIN = 1
    LOGOUT = 2
    CALLAPI = 3

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    first_name = Column(String(30))
    last_name = Column(String(30))
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    phone_no = Column(String(15), nullable=True)
    is_active = Column(Boolean, default=False)
    last_login = Column(DateTime(timezone=True), nullable=True)
    language = Column(String(2), nullable=True)
    timezone = Column(String(30), nullable=True)
    role = Column(Enum(USER_ROLES), default=USER_ROLES.USER)
    
class Plan(Base):
    __tablename__ = "plans"
    id = Column(Integer(), Identity(start=3, cycle=True), primary_key=True, index=True, autoincrement=True)
    name = Column(String(30), unique=True)
    price = Column(Float())
    billing_cycle = Column(Integer())
    page_list_limit = Column(String())
    api_list_limit = Column(String())
    users_limit = Column(Integer())
    storage_limit = Column(Float())
    status = Column(Enum(PLAN_STATUS), default=PLAN_STATUS.DISABLED)

class Order(Base):
    __tablename__ = "orders"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(ForeignKey("users.id"))
    plan_id = Column(ForeignKey("plans.id"))
    date_time = Column(DateTime(timezone=True))
    status = Column(Enum(ORDER_STATUS), default=ORDER_STATUS.CREATED)
    payment_method = Column(Enum(PAYMENT_METHODS), nullable=False)
    payment_status = Column(Enum(PAYMENT_STATUS), nullable=False)
    invoice_id = Column(String(50))
    billing_address = Column(String())

class Api(Base):
    __tablename__ = "apis"
    id = Column(Integer(), primary_key=True, index=True, autoincrement=True)
    name = Column(String(30), unique=True)
    description = Column(String())

class Page(Base):
    __tablename__ = "pages"
    id = Column(Integer(), primary_key=True, index=True, autoincrement=True)
    name = Column(String(30), unique=True)
    description = Column(String())

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer(), primary_key=True, index=True, autoincrement=True)
    user_id = Column(ForeignKey("users.id"))
    plan_id = Column(ForeignKey("plans.id"))
    trial_period = Column(Integer())
    discount = Column(Float())
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))

class ActivityLog(Base):
    __tablename__ = "activity_log"
    id = Column(Integer(), primary_key=True, index=True, autoincrement=True)
    user_id = Column(ForeignKey("users.id"))
    activity_type = Column(Enum(ACTIVITY_TYPE), nullable=False)
    activity_desc = Column(String)
