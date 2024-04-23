from pydantic import BaseModel


class LoginUrlResponse(BaseModel):
    url: str
