from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.db.models import User, UserRole
from app.db.database import get_db
from app.schemas import UserCreate, UserResponse

from app.services.user_service import create_user_service

#add admin router
router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)

@router.post("/users", response_model=UserResponse)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN))
):
    return create_user_service(db=db, payload=payload)