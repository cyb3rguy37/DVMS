from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum as SqlEnum,
    ForeignKey,
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class UserRole(str, Enum):
    GUARD = "guard"
    ADMIN = "admin"
    AUDITOR = "auditor"

class VisitStatus(str, Enum):
    ACTIVE = "active"
    CHECKED_OUT = "checked_out"
    CANCELLED = "cancelled"

class AuditEventType(str, Enum):
    LOGIN = "login"
    LOGOUT = "logout"
    CREATE_USER = "create_user"
    REGISTER_VISITOR = "register_visitor"
    CHECK_IN = "check_in"
    CHECK_OUT = "check_out"
    SEARCH_VISITOR = "search_visitor"
    VIEW_REPORT = "view_report"
    VERIFY_AUDIT_CHAIN = "verify_audit_chain"
    RETENTION_DELETE = "retention_delete"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(SqlEnum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    visits_registered = relationship("Visit", back_populates="registered_by_user")
    audit_logs = relationship("AuditLog", back_populates="actor")

class Visitor(Base):
    __tablename__ = "visitors"

    id = Column(Integer, primary_key=True, index=True)

    encrypted_name = Column(Text, nullable=False)
    encrypted_phone = Column(Text, nullable=False)
    encrypted_id_number = Column(Text, nullable=False)

    phone_blind_index = Column(String(128), nullable=True, index=True)
    id_blind_index = Column(String(128), nullable=True, index=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    retention_expiry = Column(DateTime, nullable=False)

    consent_records = relationship("ConsentRecord", back_populates="visitor")
    visits = relationship("Visit", back_populates="visitor")

class Visit(Base):
    __tablename__ = "visits" 

    id = Column(Integer, primary_key=True, index=True)

    visitor_id = Column(Integer, ForeignKey("visitors.id"), nullable=False)
    registered_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    host_name = Column(String(128), nullable=False)
    purpose = Column(String(255), nullable=False)

    check_in_time = Column(DateTime, default=datetime.utcnow)
    check_out_time = Column(DateTime, nullable=True)

    status = Column(SqlEnum(VisitStatus), default=VisitStatus.ACTIVE)

    visitor = relationship("Visitor", back_populates="visits")
    registered_by_user = relationship("User", back_populates="visits_registered")
    audit_logs = relationship("AuditLog", back_populates="visit")

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)

    actor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    visitor_id = Column(Integer, ForeignKey("visitors.id"), nullable=True)

    event_type = Column(SqlEnum(AuditEventType), nullable=False)
    event_data = Column(Text, nullable=True)

    previous_hash = Column(String(64), nullable=False)
    current_hash = Column(String(64), nullable=False, unique=True)

    timestamp = Column(DateTime, default=datetime.utcnow)

    actor = relationship("User", back_populates="audit_logs")
    visit = relationship("Visit", back_populates="audit_logs")

class ConsentRecord(Base):
    __tablename__ = "consent_records"

    id = Column(Integer, primary_key=True, index=True)

    visitor_id = Column(Integer, ForeignKey("visitors.id"), nullable=False)

    consent_text = Column(Text, nullable=False)
    consent_given = Column(Boolean, default=True)
    consent_timestamp = Column(DateTime, default=datetime.utcnow)

    visitor = relationship("Visitor", back_populates="consent_records")

class RetentionPolicy(Base):
    __tablename__ = "retention_policies"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(128), nullable=False)
    description = Column(Text, nullable=True)

    retention_days = Column(Integer, nullable=False, default=90)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)

