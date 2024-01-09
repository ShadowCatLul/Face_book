from pydantic import BaseModel
from typing import List, Optional, Union


class User(BaseModel):
    id: str
    username: str
    email: str
    tweets: Optional[List[str]] = None


class UserUpdate(BaseModel):
    username: str
    email: str
    tweets: Optional[List[str]] = None


class Tweet(BaseModel):
    id: str
    user_id: str
    content: List[Union[str]]


class TweetUpdate(BaseModel):
    user_id: str
    content: List[Union[str]]


