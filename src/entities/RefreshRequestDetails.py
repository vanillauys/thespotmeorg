from pydantic import BaseModel, Field


class RefreshRequestHeaders(BaseModel):
    Authorization: str
    Content_Type: str = Field(alias="Content-Type")


class RefreshRequestParams(BaseModel):
    grant_type: str
    refresh_token: str


class RefreshRequestDetails(BaseModel):
    url: str
    headers: RefreshRequestHeaders
    params: RefreshRequestParams
