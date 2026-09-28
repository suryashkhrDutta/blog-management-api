from fastapi import FastAPI
from . import models
from .database import engine
from .routers import authentication, blog, user

app = FastAPI(title="Blog Management API")

models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(blog.router)