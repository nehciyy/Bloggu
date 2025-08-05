from fastapi import FastAPI, Depends
from app.auth import auth_routes
# from app.routers import users, comments, comment_histories
from app.graphql.schema import graphql_app, schema
from app.auth.auth import get_current_user
from strawberry.fastapi import GraphQLRouter


app = FastAPI(title="Bloggu API")

# app.include_router(users.router)
# app.include_router(comments.router)
# app.include_router(comment_histories.router)
def get_context(current_user=Depends(get_current_user)):
    return {"current_user": current_user}

graphql_app = GraphQLRouter(schema, context_getter=get_context)

app.include_router(graphql_app, prefix="/graphql")
app.include_router(auth_routes.router)