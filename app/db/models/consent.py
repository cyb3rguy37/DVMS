from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.db.models.base import Base


class ConsentRecord(Base):
    __tablename__ = "consent_records"

    id = Column(Integer, primary_key=True, index=True)

    visitor_id = Column(Integer, ForeignKey("visitors.id"), nullable=False)

    consent_text = Column(Text, nullable=False)
    consent_given = Column(Boolean, default=True)
    consent_timestamp = Column(DateTime, default=datetime.utcnow)

    visitor = relationship("Visitor", back_populates="consent_records")