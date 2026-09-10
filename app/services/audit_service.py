from datetime import datetime

from sqlalchemy.orm import Session

from app.db.models import AuditEventType, AuditLog
from app.utils.hash_chain import GENESIS_HASH, canonical_json, compute_audit_hash

def create_audit_event(
    db: Session,
    event_type: AuditEventType,
    actor_id: int | None = None,
    visit_id: int | None = None,
    event_data: dict | None = None
) -> AuditLog:
    previous_entry = (
        db.query(AuditLog)
        .order_by(AuditLog.id.desc())
        .first()
    )

    previous_hash = previous_entry.current_hash if previous_entry else GENESIS_HASH

    timestamp = datetime.utcnow()
    event_data_text = canonical_json(event_data)

    current_hash = compute_audit_hash(
        event_type=event_type.value,
        actor_id=actor_id,
        visit_id=visit_id,
        event_data=event_data_text,
        previous_hash=previous_hash,
        timestamp=timestamp
    )

    audit_log = AuditLog(
        actor_id=actor_id,
        visit_id=visit_id,
        event_type=event_type,
        event_data=event_data_text,
        previous_hash=previous_hash,
        current_hash=current_hash,
        timestamp=timestamp
    )

    db.add(audit_log)
    db.commit()
    db.refresh(audit_log)

    return audit_log