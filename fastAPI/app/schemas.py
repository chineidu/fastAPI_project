from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

from pydantic.types import conint


class UserBase(BaseModel):
    """This is used to validate the creation of new users."""

    email: EmailStr


class UserCreate(UserBase):
    """This is used to validate the creation of new users."""

    password: str


class UserLogin(UserBase):
    """This is used to validate the creation of new users."""

    password: str


class UserResponse(UserBase):
    """This class is used to validate the response gotten from the user after creating
    a new account."""

    id: int
    created_at: datetime

    class Config:
        """This tells the Pydantic model to read the data even if it is not a dict, but an ORM model."""

        orm_mode = True


class PostBase(BaseModel):
    """This Pydantic class is used to validate the input data/schema."""

    title: str
    content: str
    is_published: bool = False


class PostCreate(PostBase):
    """All the fields can be filled."""

    pass


class PostUpdate(PostBase):
    """All the fields can be can be modified."""

    pass


class PostResponse(PostBase):
    """This class is used to validate the response gotten from the user."""

    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse  # It return a Pydaantic class

    class Config:
        """This tells the Pydantic model to read the data even if it is not a dict, but an ORM model."""

        orm_mode = True


class PostResponse2(BaseModel):
    """It validates the posts and the number of votes each post has."""

    Posts: PostResponse
    votes: int

    class Config:
        """This tells the Pydantic model to read the data even if it is not a dict, but an ORM model."""

        orm_mode = True


class TokenData(BaseModel):
    """This is used to validate the payload/data for the token."""

    id: Optional[str] = None


class TokenResponse(BaseModel):
    """This class is used to validate the token."""

    access_token: str
    token_type: str

    class Config:
        """This tells the Pydantic model to read the data even if it is not a dict, but an ORM model."""

        orm_mode = True


class VoteCreate(BaseModel):
    """This is used to validate a vote."""

    post_id: int
    dir: conint(le=1)  # direction
