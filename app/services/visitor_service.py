from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models import AuditEventType, ConsentRecord, Visit, Visitor, VisitStatus
from app.schemas import VisitorRegisterRequest, VisitorRegisterResponse, VisitorSearchResponse
from app.utils.blind_index import create_blind_index
from app.utils.encryption import decrypt_value, encrypt_value, mask_text
from app.utils.retention import calculate_retention_expiry

from app.services.audit_service import create_audit_event

def register_visitor_service(
    db: Session,
    payload: VisitorRegisterRequest,
    registered_by: int
) -> VisitorRegisterResponse:

#require consent for registration
    if not payload.consent_given:
        raise HTTPException(
            status_code=400,
            detail="Visitor consent is required"
        )

#encrypt visitor PII, create blind indexes, calculate retention expiry
    visitor = Visitor(
        encrypted_name=encrypt_value(payload.full_name),
        encrypted_phone=encrypt_value(payload.phone_number),
        encrypted_id_number=encrypt_value(payload.id_number),
        phone_blind_index=create_blind_index(payload.phone_number),
        id_blind_index=create_blind_index(payload.id_number),
        retention_expiry=calculate_retention_expiry()
    )

#create a visitor record
    db.add(visitor)
    db.commit()
    db.refresh(visitor)

#create a visit record
    visit = Visit(
        visitor_id=visitor.id,
        registered_by=registered_by,
        host_name=payload.host_name,
        purpose=payload.purpose,
        status=VisitStatus.ACTIVE
    )

    db.add(visit)
    db.commit()
    db.refresh(visit)

#create a consent record
    consent = ConsentRecord(
        visitor_id=visitor.id,
        consent_text="Visitor data collected for access control and accountability.",
        consent_given=True
    )

    db.add(consent)
    db.commit()

    create_audit_event(
        db=db,
        event_type=AuditEventType.REGISTER_VISITOR,
        actor_id=registered_by,
        visit_id=visit.id,
        event_data={
            "visitor_id": visitor.id,
            "host_name": visit.host_name,
            "purpose": visit.purpose
        }
    )

#return only masked visitor data
    return VisitorRegisterResponse(
        visitor_id=visitor.id,
        visit_id=visit.id,
        masked_name=mask_text(payload.full_name),
        masked_phone=mask_text(payload.phone_number),
        host_name=visit.host_name,
        status=visit.status,
        check_in_time=visit.check_in_time
    )


def search_visitor_service(
    db: Session,
    phone_number: str | None = None,
    id_number: str | None = None
) -> list[VisitorSearchResponse]:
    if not phone_number and not id_number:
        raise HTTPException(
            status_code=400,
            detail="Provide phone number or ID number"
        )

    query = db.query(Visitor)

    if phone_number:
        query = query.filter(
            Visitor.phone_blind_index == create_blind_index(phone_number)
        )

    if id_number:
        query = query.filter(
            Visitor.id_blind_index == create_blind_index(id_number)
        )

    visitors = query.all()

    results = []

    for visitor in visitors:
        latest_visit = (
            db.query(Visit)
            .filter(Visit.visitor_id == visitor.id)
            .order_by(Visit.id.desc())
            .first()
        )

        if latest_visit:
            name = decrypt_value(visitor.encrypted_name)
            phone = decrypt_value(visitor.encrypted_phone)

            results.append(
                VisitorSearchResponse(
                    visitor_id=visitor.id,
                    visit_id=latest_visit.id,
                    masked_name=mask_text(name),
                    masked_phone=mask_text(phone),
                    host_name=latest_visit.host_name,
                    status=latest_visit.status,
                    check_in_time=latest_visit.check_in_time
                )
            )

    return results