from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import models, schemas, hashing
from .database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from . routers import blog, user, authentication
import bcrypt

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# @app.post("/blog", status_code=status.HTTP_201_CREATED, tags= ['blogs'] )
# def create(request: schemas.Blog, db: Session = Depends(get_db)):
#     new_blog = models.Blog(title = request.title, body = request.body, user_id = 1)
#     db.add(new_blog)
#     db.commit()
#     db.refresh(new_blog)
#     return new_blog

# @app.delete('/blog/{id}', status_code=status.HTTP_200_OK, tags= ['blogs'])
# def delete(id, db: Session = Depends(get_db)):
#     blog = db.query(models.Blog).filter(models.Blog.id == id).first()
#     if not blog:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with id {id} is not available')

#     db.delete(blog)
#     db.commit()
#     return {'detail': f'blog with id {id} deleted successfully'}

# @app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags= ['blogs'])
# def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
#     blog = db.query(models.Blog).filter(models.Blog.id == id)
#     if not blog.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     blog.update(request.model_dump())
#     db.commit() 
#     return 'updated'


#getting all the blogs from the db
# @app.get('/blog', response_model= List[schemas.ShowBlog], tags= ['blogs']) 
# #shows server error, therefore use lists as many blogs are there
# def all(db: Session = Depends(get_db)):
#     blogs = db.query(models.Blog).all();
#     return blogs


# @app.get('/blog/{id}', status_code = 200, response_model = schemas.ShowBlog, tags= ['blogs']) 
# #response model acts as a filter to prevent showing the id
# def show(id, response: Response, db: Session = Depends(get_db)):
#     blog = db.query(models.Blog).filter(models.Blog.id == id).first()
#     if not blog:
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {'detail' : f'blog with id {id} is not available'}

#     #or
#         raise HTTPException (status_code = status.HTTP_404_NOT_FOUND, detail = f'blog with id {id} is not available')
#     return blog


#create a user with bcrypt password hashing
# @app.post('/user', response_model=schemas.ShowUser, tags = ['users'])
# def create_user(request: schemas.User, db: Session = Depends(get_db)):
     
#     new_user = models.User(name = request.name, email = request.email, password = hashing.Hash.bcypt(request.password))
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user

#get user from the database
# @app.get('/user/{id}', response_model=schemas.ShowUser, tags = ['users'])
# def get_user(id: int, db : Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == id).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail = f"User with id {id} is not available")
#     return user

 