from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.db.database import get_db
from app.db.models import User, UserRole
from app.schemas import VisitorRegisterRequest, VisitorRegisterResponse
from app.services.visitor_service import register_visitor_service


router = APIRouter(
    prefix="/visitors",
    tags=["Visitors"]
)


@router.post("/register", response_model=VisitorRegisterResponse)
def register_visitor(
    payload: VisitorRegisterRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.GUARD, UserRole.ADMIN))
):
    return register_visitor_service(
        db=db,
        payload=payload,
        registered_by=current_user.id
    )