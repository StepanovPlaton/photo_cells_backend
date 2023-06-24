from pydantic import BaseModel


class Authorization(BaseModel):
    password: str


class SuccessAuthorizationResponse(BaseModel):
    token: str


class NeedToken(BaseModel):
    token: str
