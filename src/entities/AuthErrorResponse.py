from typing import Optional

from pydantic import BaseModel


class AuthErrorResponse(BaseModel):
    error: Optional[str] = ""
    error_description: str
