from pydantic import BaseModel
from datetime import datetime

class CommentCreate(BaseModel):
    user_id: int
    content: str

class CommentOut(CommentCreate):
    id: int
    created_at: datetime
    updated_at: datetime | None

    class Config:
        orm_mode = True
