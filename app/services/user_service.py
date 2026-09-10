from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.db.models import User
from app.schemas import UserCreate, UserResponse

def create_user_service(db: Session, payload: UserCreate) -> UserResponse:

    # Check if the username already exists
    existing_user = db.query(User).filter(User.username == payload.username).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Create a new user instance
    new_user = User(
        username=payload.username,
        password_hash=hash_password(payload.password),
        role=payload.role, 
        is_active=True
    )

    # Add the new user to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserResponse(
        id=new_user.id,
        username=new_user.username,
        role=new_user.role.value,
        is_active=new_user.is_active
    )