from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.api.routes import resume, jobs, auth, enhanced_resume, scraper_control
from app.database.database import init_db
from app.scrapers.scheduler import job_scheduler

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
    
    # Start job scraping scheduler
    job_scheduler.start()
    logger.info("[OK] Job scheduler started")
    
    yield
    
    # Shutdown
    logger.info("[SHUTDOWN] Shutting down application...")
    job_scheduler.stop()


app = FastAPI(
    title="AI-Powered Resume-Based Job Search API",
    description="API for resume parsing and job matching with daily automated scraping",
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
app.include_router(resume.router, prefix="/api/resume", tags=["Resume"])
app.include_router(enhanced_resume.router, prefix="/api/v2/resume", tags=["Enhanced Resume"])
app.include_router(jobs.router, prefix="/api/jobs", tags=["Jobs"])
app.include_router(scraper_control.router, prefix="/api/scraper", tags=["Scraper Control"])
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
    return {"status": "healthy", "scheduler": "running" if job_scheduler.is_running else "stopped"}