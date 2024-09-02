from pydantic import BaseModel, EmailStr

class UserIn(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str

class UserResponse(BaseModel):
    data: UserOut | None

class Token(BaseModel):
    token: str | None = None

class UserInfo(BaseModel):
    id: int
    username: str
    email: EmailStr | None = None
    savings: int
    photo: str | None = None

class RedirectUrl(BaseModel):
    url: str