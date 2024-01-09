from pydantic import BaseModel
from typing import List, Optional, Union


class User(BaseModel):
    id: str
    username: str
    email: str
    posts: Optional[List[str]] = None


class UserUpdate(BaseModel):
    username: str
    email: str
    posts: Optional[List[str]] = None


class Tweet(BaseModel):
    id: str
    user_id: str
    title: str
    content: List[Union[str, bytes]]


class TweetUpdate(BaseModel):
    user_id: str
    title: str
    content: List[Union[str, bytes]]
    comments: Optional[List[str]] = None


