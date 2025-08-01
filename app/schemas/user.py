from pydantic import BaseModel, constr
from uuid import UUID

class UserBase(BaseModel):
    username: str
    group: str

class UserCreate(UserBase):
    password: str  # for auth (hash and store in model)

class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True
