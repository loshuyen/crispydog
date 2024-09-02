from pydantic import BaseModel

class ResponseOK(BaseModel):
    ok: bool

class ResponseError(BaseModel):
    error: bool
    message: str