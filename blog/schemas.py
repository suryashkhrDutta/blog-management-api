# we call pydantic model as schema and sqlalchemy model as models
from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class Blog(BaseModel):
    title: str
    body: str
    model_config = ConfigDict(from_attributes=True)



class User(BaseModel):
    name: str
    email: str
    password: str

class ShowUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    email: str

    blogs: List[Blog] = []
    
class ShowBlog(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    body: str

    creator: ShowUser
    
class Login(BaseModel):
    email : str
    password : str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None