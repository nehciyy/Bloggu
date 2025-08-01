from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class CommentHistoryBase(BaseModel):
    old_value: str
    new_value: str

class CommentHistoryCreate(CommentHistoryBase):
    comment_id: int

class CommentHistoryRead(CommentHistoryBase):
    id: int
    comment_id: int
    timestamp: datetime

    class Config:
        orm_mode = True
