from pydantic import BaseModel


class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    scope: str
    scope: str
    expires_in: int
    expires_at: int
    refresh_token: str
