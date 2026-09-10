from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.db.database import get_db
from app.db.models import User, UserRole
from app.schemas import VisitCheckoutResponse
from app.services.visit_service import checkout_visit_service


router = APIRouter(
    prefix="/visits",
    tags=["Visits"]
)


@router.post("/{visit_id}/checkout", response_model=VisitCheckoutResponse)
def checkout_visit(
    visit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.GUARD, UserRole.ADMIN))
):
    return checkout_visit_service(
        db=db,
        visit_id=visit_id,
        actor_id=current_user.id
    )