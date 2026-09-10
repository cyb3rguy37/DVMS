from pydantic import BaseModel

from app.db.models import UserRole

#define a schema for login request
class LoginRequest(BaseModel):
    username: str
    password: str

#define a schema for token response
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

#define a schema for current user response
class CurrentUserResponse(BaseModel):
    id: int
    username: str
    role: str

#define a schema for user creation (admin only)
class UserCreate(BaseModel):
    username: str
    password: str
    role: UserRole

#define a schema for API response for user creation
class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True