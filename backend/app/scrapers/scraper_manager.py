"""
Scraper manager to coordinate all job scrapers
"""
import logging
from typing import List, Dict
from datetime import datetime
from sqlalchemy.orm import Session

from app.database.models import Job
from app.scrapers.internshala_scraper import IntershalaScraper
from app.scrapers.naukri_scraper import NaukriScraper

logger = logging.getLogger(__name__)


class ScraperManager:
    """Manages all job scrapers"""
    
    def __init__(self):
        self.scrapers = {
            'internshala': IntershalaScraper(),
            'naukri': NaukriScraper(),
        }
    
    def scrape_all(self, keywords: List[str] = None, location: str = "India", limit_per_source: int = 50) -> List[Dict]:
        """
        Scrape jobs from all sources
        
        Args:
            keywords: Search keywords
            location: Job location
            limit_per_source: Maximum jobs per source
            
        Returns:
            List of all scraped jobs
        """
        all_jobs = []
        
        logger.info(f"[SCRAPE] Starting job scraping from {len(self.scrapers)} sources...")
        
        for source_name, scraper in self.scrapers.items():
            try:
                logger.info(f"[SCRAPE] Scraping {source_name}...")
                jobs = scraper.scrape(keywords=keywords, location=location, limit=limit_per_source)
                all_jobs.extend(jobs)
                logger.info(f"[OK] {source_name}: {len(jobs)} jobs scraped")
            except Exception as e:
                logger.error(f"[ERROR] Error scraping {source_name}: {str(e)}")
                continue
        
        logger.info(f"[OK] Total jobs scraped: {len(all_jobs)}")
        return all_jobs
    
    def save_jobs_to_db(self, jobs: List[Dict], db: Session) -> int:
        """
        Save scraped jobs to database
        
        Args:
            jobs: List of job dictionaries
            db: Database session
            
        Returns:
            Number of jobs saved
        """
        saved_count = 0
        
        for job_data in jobs:
            try:
                # Check if job already exists
                existing_job = db.query(Job).filter(Job.job_id == job_data['job_id']).first()
                
                if existing_job:
                    # Update existing job
                    for key, value in job_data.items():
                        setattr(existing_job, key, value)
                    existing_job.scraped_at = datetime.utcnow()
                    logger.debug(f"Updated job: {job_data['title']}")
                else:
                    # Create new job
                    new_job = Job(**job_data)
                    db.add(new_job)
                    saved_count += 1
                    logger.debug(f"Added new job: {job_data['title']}")
                
                db.commit()
                
            except Exception as e:
                logger.error(f"Error saving job {job_data.get('title', 'Unknown')}: {str(e)}")
                db.rollback()
                continue
        
        logger.info(f"[SAVE] Saved {saved_count} new jobs to database")
        return saved_count
    
    def scrape_and_save(self, db: Session, keywords: List[str] = None, location: str = "India", limit_per_source: int = 50) -> Dict:
        """
        Scrape jobs and save to database in one operation
        
        Returns:
            Dictionary with scraping results
        """
        start_time = datetime.now()
        
        # Scrape jobs
        jobs = self.scrape_all(keywords=keywords, location=location, limit_per_source=limit_per_source)
        
        # Save to database
        saved_count = self.save_jobs_to_db(jobs, db)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        result = {
            'total_scraped': len(jobs),
            'total_saved': saved_count,
            'duration_seconds': duration,
            'timestamp': end_time.isoformat(),
            'sources': list(self.scrapers.keys())
        }
        
        logger.info(f"[COMPLETE] Scraping complete: {saved_count}/{len(jobs)} jobs saved in {duration:.2f}s")
        
        return result


# Global scraper manager instance
scraper_manager = ScraperManager()
