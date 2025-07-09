from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List
import math
from app.database import get_db
from app.models import Article, User
from app.auth import get_current_user
from app.schemas import (
    ArticleResponse,
    ArticleListResponse,
)
from app.schemas import (
    ArticleCreate,
)

router = APIRouter(prefix="/articles", tags=["articles"])

@router.post("/", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED)
def create_article(
    article_data: ArticleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new article
    """
    new_article = Article(
        title=article_data.title,
        content=article_data.content,
        author_id=current_user.id
    )
    
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    
    return new_article