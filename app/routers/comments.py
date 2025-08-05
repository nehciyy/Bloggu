from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/comments", tags=["Comments"])

@router.get("/", response_model=list[schemas.CommentOut])
def get_comments(db: Session = Depends(get_db)):
    return db.query(models.Comment).all()

@router.get("/{comment_id}", response_model=schemas.CommentOut)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment

@router.post("/newcomment", response_model=schemas.CommentOut, status_code=201)
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    db_comment = models.Comment(**comment.dict())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment
