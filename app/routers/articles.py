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
