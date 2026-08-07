from fastapi import APIRouter, Depends, status, Response, HTTPException

from blog import oauth2

from .. import models, schemas, database
from typing import List
from sqlalchemy.orm import Session

router = APIRouter(
    prefix = '/blog',
    tags = ['Blogs']
)

@router.get('/', response_model= List[schemas.ShowBlog]) 
#shows server error, therefore use lists as many blogs are there
def all(db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    blogs = db.query(models.Blog).all();
    return blogs 

@router.post("/", status_code=status.HTTP_201_CREATED )
def create(request: schemas.Blog, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    new_blog = models.Blog(title = request.title, body = request.body, user_id = current_user.id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get('/{id}', status_code = 200, response_model = schemas.ShowBlog) 
#response model acts as a filter to prevent showing the id
def show(id, response: Response, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail' : f'blog with id {id} is not available'}

    #or
        raise HTTPException (status_code = status.HTTP_404_NOT_FOUND, detail = f'blog with id {id} is not available')
    return blog

@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete(id, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with id {id} is not available')

    db.delete(blog)
    db.commit()
    return {'detail': f'blog with id {id} deleted successfully'}

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    blog.update(request.model_dump())
    db.commit() 
    return 'updated'
