import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db , Base
from app.recently_viewed_service import recently_viewed_service

# Test database URL - using SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


class TestArticles:
    
    def setup_method(self):
        """Setup test database for each test"""
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        # Clear recently viewed service
        recently_viewed_service._user_recent_views.clear()
    
    def create_user_and_get_token(self, username="testuser", email="test@example.com"):
        """Helper method to create user and get auth token"""
        user_data = {
            "username": username,
            "email": email,
            "password": "testpassword123"
        }
        client.post("/auth/register", json=user_data)
        
        login_data = {
            "username": username,
            "password": "testpassword123"
        }
        login_response = client.post("/auth/login", data=login_data)
        return login_response.json()["access_token"]
    
    def test_create_article_success(self):
        """Test successful article creation"""
        token = self.create_user_and_get_token()
        headers = {"Authorization": f"Bearer {token}"}
        
        article_data = {
            "title": "Test Article",
            "content": "This is a test article content."
        }
        
        response = client.post("/articles/", json=article_data, headers=headers)
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Article"
        assert data["content"] == "This is a test article content."
        assert "id" in data
        assert "created_at" in data
        assert "author" in data
    
    def test_create_article_unauthorized(self):
        """Test creating article without authentication"""
        article_data = {
            "title": "Test Article",
            "content": "This is a test article content."
        }
        
        response = client.post("/articles/", json=article_data)
        
        assert response.status_code == 403
    
    def test_get_articles_paginated(self):
        """Test getting paginated articles"""
        token = self.create_user_and_get_token()
        headers = {"Authorization": f"Bearer {token}"}
        
        # Create multiple articles
        for i in range(5):
            article_data = {
                "title": f"Test Article {i}",
                "content": f"Content for article {i}"
            }
            client.post("/articles/", json=article_data, headers=headers)
        
        # Get first page
        response = client.get("/articles/?page=1&page_size=3", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["articles"]) == 3
        assert data["total"] == 5
        assert data["page"] == 1
        assert data["page_size"] == 3
        assert data["total_pages"] == 2
    
    def test_get_single_article(self):
        """Test getting a single article"""
        token = self.create_user_and_get_token()
        headers = {"Authorization": f"Bearer {token}"}
        
        # Create article
        article_data = {
            "title": "Test Article",
            "content": "This is a test article content."
        }
        create_response = client.post("/articles/", json=article_data, headers=headers)
        article_id = create_response.json()["id"]
        
        # Get article
        response = client.get(f"/articles/{article_id}", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Article"
        assert data["content"] == "This is a test article content."
    
    def test_get_nonexistent_article(self):
        """Test getting a nonexistent article"""
        token = self.create_user_and_get_token()
        headers = {"Authorization": f"Bearer {token}"}
        
        response = client.get("/articles/999", headers=headers)
        
        assert response.status_code == 404
        assert "Article not found" in response.json()["detail"]
    
    def test_update_article_success(self):
        """Test successful article update"""
        token = self.create_user_and_get_token()
        headers = {"Authorization": f"Bearer {token}"}
        
        # Create article
        article_data = {
            "title": "Original Title",
            "content": "Original content"
        }
        create_response = client.post("/articles/", json=article_data, headers=headers)
        article_id = create_response.json()["id"]
        
        # Update article
        update_data = {
            "title": "Updated Title",
            "content": "Updated content"
        }
        response = client.put(f"/articles/{article_id}", json=update_data, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["content"] == "Updated content"
    
    def test_update_article_unauthorized(self):
        """Test updating article by non-author"""
        token1 = self.create_user_and_get_token("user1", "user1@example.com")
        token2 = self.create_user_and_get_token("user2", "user2@example.com")
        headers1 = {"Authorization": f"Bearer {token1}"}
        headers2 = {"Authorization": f"Bearer {token2}"}
        
        # Create article with user1
        article_data = {
            "title": "Original Title",
            "content": "Original content"
        }
        create_response = client.post("/articles/", json=article_data, headers=headers1)
        article_id = create_response.json()["id"]
        
        # Try to update with user2
        update_data = {
            "title": "Updated Title"
        }
        response = client.put(f"/articles/{article_id}", json=update_data, headers=headers2)
        
        assert response.status_code == 403
        assert "You can only update your own articles" in response.json()["detail"]
    
    def test_delete_article_success(self):
        """Test successful article deletion"""
        token = self.create_user_and_get_token()
        headers = {"Authorization": f"Bearer {token}"}
        
        # Create article
        article_data = {
            "title": "Test Article",
            "content": "This is a test article content."
        }
        create_response = client.post("/articles/", json=article_data, headers=headers)
        article_id = create_response.json()["id"]
        
        # Delete article
        response = client.delete(f"/articles/{article_id}", headers=headers)
        
        assert response.status_code == 204
        
        # Verify article is deleted
        get_response = client.get(f"/articles/{article_id}", headers=headers)
        assert get_response.status_code == 404
    
    def test_delete_article_unauthorized(self):
        """Test deleting article by non-author"""
        token1 = self.create_user_and_get_token("user1", "user1@example.com")
        token2 = self.create_user_and_get_token("user2", "user2@example.com")
        headers1 = {"Authorization": f"Bearer {token1}"}
        headers2 = {"Authorization": f"Bearer {token2}"}
        
        # Create article with user1
        article_data = {
            "title": "Test Article",
            "content": "This is a test article content."
        }
        create_response = client.post("/articles/", json=article_data, headers=headers1)
        article_id = create_response.json()["id"]
        
        # Try to delete with user2
        response = client.delete(f"/articles/{article_id}", headers=headers2)
        
        assert response.status_code == 403
        assert "You can only delete your own articles" in response.json()["detail"]
    
    def test_recently_viewed_functionality(self):
        """Test recently viewed articles functionality"""
        token = self.create_user_and_get_token()
        headers = {"Authorization": f"Bearer {token}"}
        
        # Create multiple articles
        article_ids = []
        for i in range(3):
            article_data = {
                "title": f"Article {i}",
                "content": f"Content {i}"
            }
            create_response = client.post("/articles/", json=article_data, headers=headers)
            article_ids.append(create_response.json()["id"])
        
        # View articles in order
        for article_id in article_ids:
            client.get(f"/articles/{article_id}", headers=headers)
        
        # Get recently viewed
        response = client.get("/articles/recently-viewed/me", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        # Should be in reverse order (most recent first)
        assert data[0]["title"] == "Article 2"
        assert data[1]["title"] == "Article 1"
        assert data[2]["title"] == "Article 0"