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
class Query:
    @strawberry.field
    def all_users(self, info) -> List[UserType]:
        db: Session = next(database.get_db())
        return db.query(models.User).all()

    @strawberry.field
    def user_by_id(self, info, user_id: int) -> Optional[UserType]:
        db: Session = next(database.get_db())
        return db.query(models.User).filter(models.User.id == user_id).first()

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

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)
