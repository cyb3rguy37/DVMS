from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import verify_password, create_access_token
from app.db.models import User

from app.schemas import TokenResponse

def authenticate_user(db: Session, username: str, password: str) -> TokenResponse:
    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    token = create_access_token(data={"sub": str(user.id), "role": user.role.value})

    return TokenResponse(access_token=token, token_type="bearer")
