from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import relationship

from app.db.models.base import Base
from app.db.models.enums import VisitStatus


class Visit(Base):
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True, index=True)

    visitor_id = Column(Integer, ForeignKey("visitors.id"), nullable=False)
    registered_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    host_name = Column(String(150), nullable=False)
    purpose = Column(String(255), nullable=True)

    check_in_time = Column(DateTime, default=datetime.utcnow)
    check_out_time = Column(DateTime, nullable=True)

    status = Column(SqlEnum(VisitStatus), default=VisitStatus.ACTIVE)

    visitor = relationship("Visitor", back_populates="visits")
    registered_by_user = relationship("User", back_populates="visits_registered")
    audit_logs = relationship("AuditLog", back_populates="visit")