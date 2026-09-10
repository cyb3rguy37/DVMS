from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.db.database import get_db
from app.db.models import User, UserRole
from app.schemas import RetentionCleanupResponse
from app.services.retention_service import cleanup_expired_visitors_service


router = APIRouter(
    prefix="/retention",
    tags=["Retention"]
)


@router.post("/cleanup", response_model=RetentionCleanupResponse)
def cleanup_expired_visitors(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN))
):
    return cleanup_expired_visitors_service(
        db=db,
        actor_id=current_user.id
    )