from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class User(Base):
    __tablename__ = "users"
    logger.info(f"Defining model for table: {__tablename__}")

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    articles = relationship("Article", back_populates="author")
    article_views = relationship("ArticleView", back_populates="user")

class Article(Base):
    __tablename__ = "articles"
    logger.info(f"Defining model for table: {__tablename__}")

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    author = relationship("User", back_populates="articles")
    article_views = relationship("ArticleView", back_populates="article")

class ArticleView(Base):
    __tablename__ = "article_views"
    logger.info(f"Defining model for table: {__tablename__}")

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=False)
    viewed_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="article_views")
    article = relationship("Article", back_populates="article_views")