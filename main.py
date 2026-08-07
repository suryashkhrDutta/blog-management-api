from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import uvicorn 

app = FastAPI()

@app.get('/blog')
def index(limit: int, published: Optional[bool] = None, sort: Optional[str] = None):
    #only publish 10 blogs
    #http://127.0.0.1:8000/blog?limit=10&published=true
    if published:
        return {'data': f'{limit} published blogs from the dB'}
    else:
        return{'data' : f'{limit} blogs from the db'}


@app.get('/blog/unpublished') #should be kept above it executes limne by line
def unpublished():
    return {'data': 'all unpublished blogs'}

@app.get('/blog/{id}')
def show(id: int):
    return { 
        'data': id
      }

@app.get('/blog/{id}/comments')
def comments(id, limit=10):
    #fetch comments of blog with id = id
    return {'data' : {'1', '2'}}


#-------------------------------------------------------
#creation of model
class Blog(BaseModel):
    title : str
    body: str
    published: Optional[bool] = None

#post method is used to create something new
@app.post('/blog')
def create_blog(request: Blog):
    
    return{'data': f"blog in post method is created with title as {request.title} and body as {request.body}"}

#if we need a different port to run, for debugging purpose
# if __name__ = "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=9000)
