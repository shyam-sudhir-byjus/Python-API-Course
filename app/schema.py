from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

'''
    Validates whether data field provided in request/response matches
'''

class CreateUser(BaseModel):
    email: EmailStr
    password: str
    
    
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    

class CreatePost(PostBase):
    pass


class UpdatePost(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse
    
    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: PostResponse
    votes: int
        
    class Config:
        orm_mode = True
        
        
class LoginUser(BaseModel):
    email: EmailStr
    password: str
    

class Token(BaseModel):
    access_token: str
    token_type: str
    
    
class TokenData(BaseModel):
    id: Optional[str] = None
    

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
    
    