from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from pydantic import ConfigDict

class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ArticleBase(BaseModel):
    title: str
    content: str


class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class ArticleResponse(ArticleBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    author: UserResponse

    model_config = ConfigDict(from_attributes=True)


class ArticleListResponse(BaseModel):
    id: int
    title: str
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    author: UserResponse

    model_config = ConfigDict(from_attributes=True)


class ArticlesPaginatedResponse(BaseModel):
    articles: List[ArticleListResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class RecentlyViewedArticleResponse(BaseModel):
    id: int
    title: str
    author_id: int
    viewed_at: datetime
    author: UserResponse

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None