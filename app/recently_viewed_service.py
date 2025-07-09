from collections import defaultdict, deque
from datetime import datetime
from typing import List, Dict
from app.schemas import RecentlyViewedArticleResponse
from app.models import Article, User


class RecentlyViewedService:
    """
    In-memory service to track recently viewed articles per user
    Uses basic collections and primitives as required
    """
    
    def __init__(self, max_recent_items: int = 10):
        # Dictionary to store recently viewed articles per user
        # Key: user_id, Value: deque of article data
        self._user_recent_views: Dict[int, deque] = defaultdict(lambda: deque(maxlen=max_recent_items))
    
    def add_view(self, user_id: int, article: Article) -> None:
        """
        Add an article to user's recently viewed list
        """
        current_time = datetime.utcnow()
        
        # Remove if already exists to avoid duplicates
        self._remove_existing_view(user_id, article.id)
        
        # Add to front of deque (most recent first)
        view_data = {
            'article_id': article.id,
            'title': article.title,
            'author_id': article.author_id,
            'author_username': article.author.username,
            'author_email': article.author.email,
            'viewed_at': current_time
        }
        
        self._user_recent_views[user_id].appendleft(view_data)
    
    def get_recently_viewed(self, user_id: int) -> List[RecentlyViewedArticleResponse]:
        """
        Get recently viewed articles for a user
        """
        recent_views = self._user_recent_views.get(user_id, deque())
        
        result = []
        for view_data in recent_views:
            # Create mock user object for response
            mock_user = type('MockUser', (), {
                'id': view_data['author_id'],
                'username': view_data['author_username'],
                'email': view_data['author_email'],
                'is_active': True,
                'created_at': datetime.utcnow(),
                'updated_at': None
            })()
            
            response = RecentlyViewedArticleResponse(
                id=view_data['article_id'],
                title=view_data['title'],
                author_id=view_data['author_id'],
                viewed_at=view_data['viewed_at'],
                author=mock_user
            )
            result.append(response)
        
        return result
    
    def _remove_existing_view(self, user_id: int, article_id: int) -> None:
        """
        Remove existing view of the same article to avoid duplicates
        """
        user_views = self._user_recent_views.get(user_id)
        if not user_views:
            return
        
        # Create a new deque without the existing article
        filtered_views = deque(
            [view for view in user_views if view['article_id'] != article_id],
            maxlen=user_views.maxlen
        )
        
        self._user_recent_views[user_id] = filtered_views
    
    def clear_user_views(self, user_id: int) -> None:
        """
        Clear all recently viewed articles for a user
        """
        if user_id in self._user_recent_views:
            del self._user_recent_views[user_id]


# Global instance
recently_viewed_service = RecentlyViewedService()