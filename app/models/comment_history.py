import uuid
from datetime import datetime
from sqlalchemy import Column, ForeignKey, DateTime, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base

class CommentHistory(Base):
    __tablename__ = "comment_histories"

    id = Column(Integer, primary_key=True, index=True)
    comment_id = Column(Integer, ForeignKey("comments.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    old_value = Column(Text, nullable=False)
    new_value = Column(Text, nullable=False)

    comment = relationship("Comment", back_populates="histories")
