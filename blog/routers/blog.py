from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from blog import oauth2
from .. import models, schemas, database

router = APIRouter(
    prefix='/blog',
    tags=['Blogs']
)


def get_owned_blog(id: int, db: Session, current_user: models.User):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'blog with id {id} is not available'
        )
    if blog.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You can only modify your own blogs'
        )
    return blog


@router.get('/', response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowBlog)
def create(request: schemas.Blog, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=current_user.id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def show(id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'blog with id {id} is not available'
        )
    return blog


@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete(id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    blog = get_owned_blog(id, db, current_user)
    db.delete(blog)
    db.commit()
    return {'detail': f'blog with id {id} deleted successfully'}


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ShowBlog)
def update(id: int, request: schemas.Blog, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    blog = get_owned_blog(id, db, current_user)
    blog.title = request.title
    blog.body = request.body
    db.commit()
    db.refresh(blog)
    return blog
