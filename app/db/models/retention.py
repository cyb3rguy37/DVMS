from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.db.models.base import Base


class RetentionPolicy(Base):
    __tablename__ = "retention_policies"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)

    retention_days = Column(Integer, nullable=False, default=90)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)