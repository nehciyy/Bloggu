import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from app import models

class UserType(SQLAlchemyObjectType):
    class Meta:
        model = models.User
        interfaces = (graphene.relay.Node, )

class CommentType(SQLAlchemyObjectType):
    class Meta:
        model = models.Comment
        interfaces = (graphene.relay.Node, )

class CommentHistoryType(SQLAlchemyObjectType):
    class Meta:
        model = models.CommentHistory
        interfaces = (graphene.relay.Node, )
