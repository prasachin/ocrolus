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
    ArticlesPaginatedResponse,
    RecentlyViewedArticleResponse,
    ArticleUpdate,
)
from app.schemas import (
    ArticleCreate,
)

from app.recently_viewed_service import recently_viewed_service

router = APIRouter(prefix="/articles", tags=["articles"])


# Here I created a route so that users can create articles. Also all the routes are protected by authentication.user must be logged in to create an article.
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

# Here I created a route so that users can req articles and also pagination is implemented.
@router.get("/", response_model=ArticlesPaginatedResponse)
def get_articles(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get paginated list of articles
    """
    offset = (page - 1) * page_size
    
    # Get total count
    total_articles = db.query(Article).count()
    
    # Get articles with pagination, it means we are fetching the articles
    # ordered by creation date, with an offset and limit for pagination. if user wants to see the most recent articles first.
    # here i used ordering by created_at in descending order to show the most recent articles first, intentionally.
    articles = (
        db.query(Article)
        .order_by(desc(Article.created_at))
        .offset(offset)
        .limit(page_size)
        .all()
    )
    
    total_pages = math.ceil(total_articles / page_size)
    
    return ArticlesPaginatedResponse(
        articles=articles,
        total=total_articles,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )

# Here i created a endpoint to view a specific article by its ID. 
@router.get("/{article_id}", response_model=ArticleResponse)
def get_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific article by ID and track it as recently viewed
    """
    article = db.query(Article).filter(Article.id == article_id).first()
    
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    # Here i am tracking the article as recently viewed by the user.
    recently_viewed_service.add_view(current_user.id, article)
    
    return article


# Here i created a endpoint to get the recently viewed articles for the current user.
@router.get("/recently-viewed/me", response_model=List[RecentlyViewedArticleResponse])
def get_recently_viewed_articles(
    current_user: User = Depends(get_current_user)
):
    """
    Get recently viewed articles for the current user
    """
    return recently_viewed_service.get_recently_viewed(current_user.id)



# Here i created a endpoint to update the article using its id.Also i am adding functionality that only the author of the article can update it.
@router.put("/{article_id}", response_model=ArticleResponse)
def update_article(
    article_id: int,
    article_update: ArticleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update an article (only by the author)
    """
    article = db.query(Article).filter(Article.id == article_id).first()
    
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    # Check if current user is the author
    if article.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own articles"
        )
    
    # Update fields if provided, we can customize it as per the entities of the article.now we have only title and content.
    if article_update.title is not None:
        article.title = article_update.title
    if article_update.content is not None:
        article.content = article_update.content
    
    db.commit()
    db.refresh(article)
    
    return article


# here i created a endpoint to delete the article using its id. Also i am adding functionality that only the author of the article can delete it.

@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete an article (only by the author)
    """
    article = db.query(Article).filter(Article.id == article_id).first()
    
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    # Check if current user is the author
    if article.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own articles"
        )
    
    db.delete(article)
    db.commit()