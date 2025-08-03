from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    group: str

class UserCreate(UserBase):
    password: str  # Plain password input; store hashed version in DB

class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True  # Pydantic v2 equivalent of orm_mode = True
