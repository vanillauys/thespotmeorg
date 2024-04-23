from pydantic import BaseModel


class SpotMeInternalError(BaseModel):
    status: int
    errors: list[str]
    description: str
