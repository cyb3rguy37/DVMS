from pydantic import BaseModel

#define a schema for token response
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

#define a schema for current user response
class CurrentUserResponse(BaseModel):
    id: int
    username: str
    role: str
