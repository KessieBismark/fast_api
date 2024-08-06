from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True


# class CreatePost(BaseModel):
#     title: str
#     content: str
#     published: bool = True
#
#
# class UpdatePost(BaseModel):
#     title: str
#     content: str
#     published: bool

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True  # Update from orm_mode = True


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    owner: UserOut

    class Config:
        from_attributes = True  # Update from orm_mode = True


class PostCreate(PostBase):
    pass


class PostOut(PostBase):
    Post:  PostBase
    votes: int

# class PostUpdate(PostBase):
#     pass

class PostData(PostBase):
    # title: str
    # content: str
    # published: bool
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True  # Update from orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str




class UserLogin(BaseModel):
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