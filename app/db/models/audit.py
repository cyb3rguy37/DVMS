from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import relationship

from app.db.models.base import Base
from app.db.models.enums import AuditEventType


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)

    actor_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    visit_id = Column(Integer, ForeignKey("visits.id"), nullable=True)

    event_type = Column(SqlEnum(AuditEventType), nullable=False)
    event_data = Column(Text, nullable=True)

    previous_hash = Column(String(64), nullable=False)
    current_hash = Column(String(64), nullable=False, unique=True)

    timestamp = Column(DateTime, default=datetime.utcnow)

    actor = relationship("User", back_populates="audit_logs")
    visit = relationship("Visit", back_populates="audit_logs")