from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.api.routes import auth, enhanced_resume
from app.database.database import init_db

# logging config...
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    logger.info("[STARTUP] Starting application...")
    
    # Initialize database
    init_db()
    logger.info("[OK] Database initialized")
    
    yield
    
    # Shutdown
    logger.info("[SHUTDOWN] Shutting down application...")


app = FastAPI(
    title="AI-Powered Resume-Based Job Search API",
    description="API for resume parsing and job matching (n8n integration)",
    version="2.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(enhanced_resume.router, prefix="/api/v2/resume", tags=["Enhanced Resume"])
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to AI-Powered Resume-Based Job Search API",
        "version": "2.0.0",
        "features": [
            "Daily automated job scraping",
            "Intelligent resume parsing",
            "AI-powered job matching",
            "Local database storage"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}