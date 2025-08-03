from fastapi import FastAPI
from app.routers import users, comments, comment_histories

app = FastAPI(title="Bloggu API")

app.include_router(users.router)
app.include_router(comments.router)
app.include_router(comment_histories.router)
