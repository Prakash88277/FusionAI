"""
Scraper control endpoints for manual scraping
"""
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from app.database.database import get_db
from app.scrapers.scraper_manager import scraper_manager

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/scrape-now")
async def trigger_scraping(
    background_tasks: BackgroundTasks,
    keywords: Optional[List[str]] = None,
    location: str = "India",
    limit_per_source: int = 50,
    db: Session = Depends(get_db)
):
    """Manually trigger job scraping"""
    try:
        if not keywords:
            keywords = ['software', 'developer', 'engineer', 'python', 'java', 'data']
        
        logger.info(f"Manual scraping triggered with keywords: {keywords}")
        
        # Run scraping in background
        background_tasks.add_task(
            scraper_manager.scrape_and_save,
            db=db,
            keywords=keywords,
            location=location,
            limit_per_source=limit_per_source
        )
        
        return {
            "success": True,
            "message": "Scraping started in background",
            "keywords": keywords,
            "location": location,
            "limit_per_source": limit_per_source
        }
        
    except Exception as e:
        logger.error(f"Error triggering scraping: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/scraper-status")
async def get_scraper_status():
    """Get status of available scrapers"""
    try:
        scrapers = scraper_manager.scrapers
        
        return {
            "total_scrapers": len(scrapers),
            "available_sources": list(scrapers.keys()),
            "status": "ready"
        }
        
    except Exception as e:
        logger.error(f"Error getting scraper status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
