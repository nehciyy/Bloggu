import strawberry
from typing import List, Optional
from sqlalchemy.orm import Session
from app import models, database, utils 
from strawberry.fastapi import GraphQLRouter
from datetime import datetime

@strawberry.type
class UserType:
    id: int
    username: str
    group: str

@strawberry.type
class CommentType:
    id: int
    content: str
    user_id: int

@strawberry.type
class CommentHistoryType:
    id: int
    comment_id: int
    timestamp: datetime
    old_value: str
    new_value: str

@strawberry.type
class Query:
    @strawberry.field
    def all_users(self, info) -> List[UserType]:
        db: Session = next(database.get_db())
        return db.query(models.User).all()

    @strawberry.field
    def user_by_id(self, info, user_id: int) -> Optional[UserType]:
        db: Session = next(database.get_db())
        return db.query(models.User).filter(models.User.id == user_id).first()
    
    @strawberry.field
    def all_comments(self, info) -> List[CommentType]:
        db: Session = next(database.get_db())
        return db.query(models.Comment).all()

    @strawberry.field
    def comment_by_id(self, info, comment_id: int) -> Optional[CommentType]:
        db: Session = next(database.get_db())
        return db.query(models.Comment).filter(models.Comment.id == comment_id).first()

    @strawberry.field
    def all_comment_histories(self, info) -> List[CommentHistoryType]:
        db: Session = next(database.get_db())
        return db.query(models.CommentHistory).all()

    @strawberry.field
    def comment_history_by_id(self, info, history_id: int) -> Optional[CommentHistoryType]:
        db: Session = next(database.get_db())
        return db.query(models.CommentHistory).filter(models.CommentHistory.id == history_id).first()

@strawberry.type
class Mutation:
    ##USER MUTATIONS
    @strawberry.mutation
    def create_user(self, info, username: str, password: str, group: str) -> UserType:
        db: Session = next(database.get_db())
        hashed_password = utils.security.hash_password(password)
        db_user = models.User(username=username, group=group, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return UserType(id=db_user.id, username=db_user.username, group=db_user.group)


    @strawberry.mutation
    def update_user(self, info, user_id: int, username: Optional[str] = None, group: Optional[str] = None) -> Optional[UserType]:
        db: Session = next(database.get_db())
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            return None
        if username:
            user.username = username
        if group:
            user.group = group
        db.commit()
        db.refresh(user)
        return UserType(id=user.id, username=user.username, group=user.group)

    @strawberry.mutation
    def delete_user(self, info, user_id: int) -> bool:
        db: Session = next(database.get_db())
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            return False
        db.delete(user)
        db.commit()
        return True
    
## COMMENT MUTATIONS
    @strawberry.mutation
    def create_comment(self, info, user_id: int, content: str) -> CommentType:
        db: Session = next(database.get_db())
        db_comment = models.Comment(user_id=user_id, content=content)
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return CommentType(id=db_comment.id, user_id=db_comment.user_id, content=db_comment.content)
    
    @strawberry.mutation
    def update_comment(self, info, comment_id: int, new_content: str) -> CommentType:
        db: Session = next(database.get_db())
        comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
        if not comment:
            raise Exception("Comment not found")

        old_value = comment.content
        comment.content = new_content

        db_history = models.CommentHistory(
            comment_id=comment.id,
            timestamp=datetime.utcnow(),
            old_value=old_value,
            new_value=new_content
        )
        db.add(db_history)
        
        db.commit()
        db.refresh(comment)
        return CommentType(id=comment.id, user_id=comment.user_id, content=comment.content)


    @strawberry.mutation
    def delete_comment(self, info, comment_id: int) -> bool:
        db: Session = next(database.get_db())
        comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
        if not comment:
            return False
        db.delete(comment)
        db.commit()
        return True

## COMMENT HISTORY MUTATIONS
    @strawberry.mutation
    def create_comment_history(self, info, comment_id: int, timestamp: datetime, old_value: str, new_value: str) -> CommentHistoryType:
        db: Session = next(database.get_db())
        db_history = models.CommentHistory(comment_id=comment_id, timestamp=timestamp, old_value=old_value, new_value=new_value)
        db.add(db_history)
        db.commit()
        db.refresh(db_history)
        return CommentHistoryType(
            id=db_history.id,
            comment_id=db_history.comment_id,
            timestamp=db_history.timestamp,
            old_value=db_history.old_value,
            new_value=db_history.new_value
        )


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)
