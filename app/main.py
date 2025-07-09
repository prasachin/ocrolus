from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
from app.database import engine, get_db, check_db_connection
from app.models import Base
import logging
from sqlalchemy import text
from app.routers import auth, articles
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        is_connected = check_db_connection()
        if not is_connected:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        logger.info("Checking database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables verified/created successfully")
        yield
    except Exception as e:
        logger.error(f"Startup error: {str(e)}")
        raise

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(articles.router)

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Hello, World!"}


@app.get("/health")
def health_check(db = Depends(get_db)):
    """
    Health check endpoint with database verification
    """
    try:
        db.execute(text("SELECT 1"))
        logger.info("Health check - Database connection OK")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}