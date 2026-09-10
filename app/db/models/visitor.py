from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.models.base import Base


class Visitor(Base):
    __tablename__ = "visitors"

    id = Column(Integer, primary_key=True, index=True)

    encrypted_name = Column(Text, nullable=False)
    encrypted_phone = Column(Text, nullable=True)
    encrypted_id_number = Column(Text, nullable=True)

    phone_blind_index = Column(String(128), nullable=True, index=True)
    id_blind_index = Column(String(128), nullable=True, index=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    retention_expiry = Column(DateTime, nullable=True)

    visits = relationship("Visit", back_populates="visitor")
    consent_records = relationship("ConsentRecord", back_populates="visitor")