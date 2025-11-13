"""
Daily job scraping scheduler
"""
import schedule
import time
import logging
from datetime import datetime
from threading import Thread

from app.database.database import SessionLocal
from app.database.models import Job
from app.scrapers.scraper_manager import scraper_manager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JobScrapingScheduler:
    """Scheduler for daily job scraping"""
    
    def __init__(self):
        self.is_running = False
        self.thread = None
    
    def scrape_jobs_task(self):
        """Task to scrape jobs"""
        logger.info(f"[SCHEDULE] Starting scheduled job scraping at {datetime.now()}")
        
        db = SessionLocal()
        try:
            # Scrape jobs with common tech keywords
            keywords = ['software', 'developer', 'engineer', 'data', 'python', 'java']
            result = scraper_manager.scrape_and_save(
                db=db,
                keywords=keywords,
                location="India",
                limit_per_source=100
            )
            
            logger.info(f"[OK] Scheduled scraping completed: {result}")
            
        except Exception as e:
            logger.error(f"[ERROR] Error in scheduled scraping: {str(e)}")
        finally:
            db.close()
    
    def run_scheduler(self):
        """Run the scheduler loop"""
        self.is_running = True
        logger.info("[STARTUP] Job scraping scheduler started")
        logger.info("[SCHEDULE] Jobs will be scraped daily at 2:00 AM")
        
        # Schedule daily scraping at 2 AM
        schedule.every().day.at("02:00").do(self.scrape_jobs_task)
        
        # Wait 5 seconds then check if we need to scrape (allows server to start first)
        logger.info("[STARTUP] Checking database status in 5 seconds...")
        time.sleep(5)
        
        # Check if database has jobs
        db = SessionLocal()
        try:
            job_count = db.query(Job).count()
            logger.info(f"[STARTUP] Database currently has {job_count} jobs")
            
            if job_count == 0:
                # Run initial scraping to populate database
                logger.info("[STARTUP] Database is empty. Running initial job scraping...")
                self.scrape_jobs_task()
                logger.info("[STARTUP] Initial scraping complete! Database populated.")
            else:
                logger.info("[STARTUP] Database already has jobs. Skipping initial scraping.")
        finally:
            db.close()
        
        while self.is_running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def start(self):
        """Start scheduler in background thread"""
        if not self.is_running:
            self.thread = Thread(target=self.run_scheduler, daemon=True)
            self.thread.start()
            logger.info("[OK] Scheduler thread started")
    
    def stop(self):
        """Stop the scheduler"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("[STOP] Scheduler stopped")


# Global scheduler instance
job_scheduler = JobScrapingScheduler()
