from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, database
from app.utils import security
from fastapi.security import OAuth2PasswordRequestForm
from jwt import encode
from app.config import SECRET_KEY, ALGORITHM
from app.schemas.user import UserCreate, UserRead
import os

router = APIRouter()

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    token_data = {"sub": user.username}
    token = encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def signup(user: UserCreate, db: Session = Depends(database.get_db)):
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    hashed_password = security.hash_password(user.password)
    new_user = models.User(
        username=user.username,
        hashed_password=hashed_password,
        group=user.group
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user