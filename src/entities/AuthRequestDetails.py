from pydantic import BaseModel, Field


class AuthRequestHeaders(BaseModel):
    Authorization: str
    Content_Type: str = Field(alias="Content-Type")


class AuthRequestParams(BaseModel):
    grant_type: str
    code: str
    redirect_uri: str


class AuthRequestDetails(BaseModel):
    url: str
    headers: AuthRequestHeaders
    params: AuthRequestParams
