import strawberry
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import Request
from strawberry.fastapi import GraphQLRouter
from datetime import datetime

from app import models, database, utils
from app.auth.auth import get_current_user
from app.models.user import User as UserModel

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


def to_user_type(user: UserModel) -> UserType:
    return UserType(id=user.id, username=user.username, group=user.group)


def to_comment_type(comment: models.Comment) -> CommentType:
    return CommentType(id=comment.id, content=comment.content, user_id=comment.user_id)


def to_comment_history_type(history: models.CommentHistory) -> CommentHistoryType:
    return CommentHistoryType(
        id=history.id,
        comment_id=history.comment_id,
        timestamp=history.timestamp,
        old_value=history.old_value,
        new_value=history.new_value,
    )


@strawberry.type
class Query:
    @strawberry.field
    def all_users(self, info) -> List[UserType]:
        request: Request = info.context["request"]
        db: Session = next(database.get_db())
        user: UserModel = get_current_user(request,db)
        
        users = db.query(models.User).all()
        return [to_user_type(u) for u in users]

    @strawberry.field
    def user_by_id(self, info, user_id: int) -> Optional[UserType]:
        request: Request = info.context["request"]
        db: Session = next(database.get_db())
        user: UserModel = get_current_user(request,db)
        u = db.query(models.User).filter(models.User.id == user_id).first()
        return to_user_type(u) if u else None

    @strawberry.field
    def all_comments(self, info) -> List[CommentType]:
        request: Request = info.context["request"]
        db: Session = next(database.get_db())
        user: UserModel = get_current_user(request, db)
        comments = (
            db.query(models.Comment)
            .join(models.User)
            .filter(models.User.group == user.group)
            .all()
        )
        return [to_comment_type(c) for c in comments]

    @strawberry.field
    def comment_by_id(self, info, comment_id: int) -> Optional[CommentType]:
        request: Request = info.context["request"]
        db: Session = next(database.get_db())
        user: UserModel = get_current_user(request, db)

        comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
        if comment:
            comment_user = db.query(models.User).filter(models.User.id == comment.user_id).first()
            if comment_user and comment_user.group == user.group:
                return to_comment_type(comment)
        return None

    @strawberry.field
    def all_comment_histories(self, info) -> List[CommentHistoryType]:
        request: Request = info.context["request"]
        db: Session = next(database.get_db())
        user: UserModel = get_current_user(request, db)
        histories = (
            db.query(models.CommentHistory)
            .join(models.Comment)
            .join(models.User, models.Comment.user_id == models.User.id)
            .filter(models.User.group == user.group)
            .all()
        )
        return [to_comment_history_type(h) for h in histories]

    @strawberry.field
    def comment_history_by_id(self, info, history_id: int) -> Optional[CommentHistoryType]:
        request: Request = info.context["request"]
        db: Session = next(database.get_db())
        user: UserModel = get_current_user(request, db)
        history = db.query(models.CommentHistory).filter(models.CommentHistory.id == history_id).first()
        if history:
            comment = db.query(models.Comment).filter(models.Comment.id == history.comment_id).first()
            comment_user = db.query(models.User).filter(models.User.id == comment.user_id).first()
            if comment_user and comment_user.group == user.group:
                return to_comment_history_type(history)
        return None


@strawberry.type
class Mutation:
    # user
    @strawberry.mutation
    def create_user(self, info, username: str, password: str, group: str) -> UserType:
        db: Session = next(database.get_db())
        hashed_password = utils.security.hash_password(password)
        db_user = models.User(username=username, group=group, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return to_user_type(db_user)

    @strawberry.mutation
    def update_user(self, info, username: Optional[str] = None, group: Optional[str] = None) -> Optional[UserType]:
        request: Request = info.context["request"]
        db: Session = next(database.get_db())
        user: UserModel = get_current_user(request, db)

        if username:
            user.username = username
        if group:
            user.group = group

        db.commit()
        db.refresh(user)
        return to_user_type(user)

    @strawberry.mutation
    def delete_user(self, info) -> bool:
        request: Request = info.context["request"]
        db: Session = next(database.get_db())
        user: UserModel = get_current_user(request, db)

        db.delete(user)
        db.commit()
        return True

    # comments
    @strawberry.mutation
    def create_comment(self, info, content: str) -> CommentType:
        request: Request = info.context["request"]
        db: Session = next(database.get_db())
        user: UserModel = get_current_user(request, db)

        db_comment = models.Comment(user_id=user.id, content=content)
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return to_comment_type(db_comment)

    @strawberry.mutation
    def update_comment(self, info, comment_id: int, new_content: str) -> CommentType:
        request: Request = info.context["request"]
        db: Session = next(database.get_db())
        user: UserModel = get_current_user(request, db)

        comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
        if not comment or comment.user_id != user.id:
            raise Exception("Unauthorized to update this comment")

        old_value = comment.content
        comment.content = new_content

        db_history = models.CommentHistory(
            comment_id=comment.id,
            timestamp=datetime.utcnow(),
            old_value=old_value,
            new_value=new_content,
        )
        db.add(db_history)
        db.commit()
        db.refresh(comment)
        return to_comment_type(comment)

    @strawberry.mutation
    def delete_comment(self, info, comment_id: int) -> bool:
        request: Request = info.context["request"]
        db: Session = next(database.get_db())
        user: UserModel = get_current_user(request, db)

        comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
        if not comment or comment.user_id != user.id:
            raise Exception("Unauthorized to delete this comment")
        db.delete(comment)
        db.commit()
        return True


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)