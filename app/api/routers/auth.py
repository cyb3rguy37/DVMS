from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.database import get_db
from app.db.models import User
from app.schemas import CurrentUserResponse, TokenResponse

from app.services.auth_service import authenticate_user

#create authentication router 
router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)

#add login endpoint
@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return authenticate_user(db=db, username=form_data.username, password=form_data.password)


@router.get("/me", response_model=CurrentUserResponse)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return CurrentUserResponse(
        id=current_user.id,
        username=current_user.username,
        role=current_user.role.value
    )