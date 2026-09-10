from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.security import verify_password, create_access_token
from app.db.database import get_db
from app.db.models import User
from app.schemas import CurrentUserResponse, TokenResponse, LoginRequest

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
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    token = create_access_token(data={"sub": str(user.id), "role": user.role.value})

    return TokenResponse(access_token=token, token_type="bearer")

@router.get("/me", response_model=CurrentUserResponse)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return CurrentUserResponse(
        id=current_user.id,
        username=current_user.username,
        role=current_user.role.value
    )