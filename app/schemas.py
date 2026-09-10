from pydantic import BaseModel, Field, field_validator

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
#with input validation for username and password
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)
    role: UserRole

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        return value.strip().lower()

#define a schema for API response for user creation
class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True