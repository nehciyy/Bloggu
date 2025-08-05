from fastapi import Request, HTTPException, status
from jwt import decode, exceptions
from app.config import SECRET_KEY, ALGORITHM
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User

def get_current_user(request: Request, db: Session) -> User:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = auth_header.removeprefix("Bearer ").strip()

    try:
        payload = decode(token.encode("utf-8"), SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except Exception:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user