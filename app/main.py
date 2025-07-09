from fastapi import FastAPI, Depends, HTTPException
from app.database import engine, get_db, check_db_connection
from app.models import Base
import logging
from sqlalchemy import text
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    try:
        # Check database connection
        is_connected = check_db_connection()
        if not is_connected:
            raise HTTPException(status_code=500, detail="Database connection failed")
        
        # Create tables if they don't exist
        logger.info("Checking database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables verified/created successfully")
    except Exception as e:
        logger.error(f"Startup error: {str(e)}")
        raise

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