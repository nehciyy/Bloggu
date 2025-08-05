from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/comment_histories", tags=["Comment Histories"])

@router.get("/")
async def get_comment_histories():
    return {"message": "List of comment histories"}

@router.get("/{history_id}")
async def get_comment_history(history_id: int):
    return {"message": f"Comment history with id {history_id}"}

@router.post("/", response_model=schemas.CommentHistoryRead)
def create_comment_history(history: schemas.CommentHistoryCreate, db: Session = Depends(get_db)):
    db_history = models.CommentHistory(**history.dict())
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history
