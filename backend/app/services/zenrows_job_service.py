import logging
from typing import List
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from app.scrapers.zenrows_scraper import scrape_jobs_for_keywords
from app.database.database import SessionLocal
from app.database.models import Job

logger = logging.getLogger(__name__)

def upsert_jobs_from_keywords(keywords: List[str], source: str = 'zenrows', max_jobs: int = 30) -> List[dict]:
    """
    Scrape jobs using ZenRows for given keywords and upsert them to database
    
    Args:
        keywords: List of keywords to search for jobs
        source: Source identifier for the jobs
        max_jobs: Maximum number of jobs to process
        
    Returns:
        List of saved job dictionaries
    """
    logger.info(f"Starting job scraping for keywords: {keywords[:5]}... (max: {max_jobs})")
    
    # Scrape jobs using ZenRows
    try:
        jobs = scrape_jobs_for_keywords(keywords, max_per_source=10)[:max_jobs]
        logger.info(f"Scraped {len(jobs)} jobs from ZenRows")
    except Exception as e:
        logger.error(f"Failed to scrape jobs: {str(e)}")
        return []
    
    if not jobs:
        logger.warning("No jobs found for given keywords")
        return []
    
    # Upsert jobs to database
    db = SessionLocal()
    saved = []
    
    try:
        for j in jobs:
            try:
                # Check if job already exists
                db_job = None
                
                # First try to find by apply_link if available
                if j.get('apply_link'):
                    db_job = db.query(Job).filter(Job.apply_link == j.get('apply_link')).first()
                
                # Fallback uniqueness check by title + company
                if not db_job:
                    title = j.get('title') or 'N/A'
                    company = j.get('company') or 'Unknown'
                    db_job = db.query(Job).filter(
                        Job.title == title, 
                        Job.company == company
                    ).first()

                if not db_job:
                    # Create new job
                    db_job = Job(
                        job_id=None,  # Auto-generated
                        title=j.get('title') or 'N/A',
                        company=j.get('company') or 'Unknown',
                        location=j.get('location') or 'India',
                        description=j.get('description') or '',
                        skills=None,  # Will be populated by existing matching logic
                        salary_text=None,
                        apply_link=j.get('apply_link'),
                        job_type=None,
                        posted_date=datetime.utcnow(),
                        is_active=True
                    )
                    
                    # Add optional source if model supports it
                    if hasattr(db_job, 'source'):
                        db_job.source = source
                        
                    db.add(db_job)
                    logger.debug(f"Created new job: {db_job.title} at {db_job.company}")
                    
                else:
                    # Update existing job
                    db_job.description = j.get('description') or db_job.description
                    db_job.is_active = True
                    if j.get('apply_link') and not db_job.apply_link:
                        db_job.apply_link = j.get('apply_link')
                    logger.debug(f"Updated existing job: {db_job.title} at {db_job.company}")

                db.commit()
                
                # Add to saved list
                saved.append({
                    'id': db_job.id if hasattr(db_job, 'id') else None,
                    'title': db_job.title,
                    'company': db_job.company,
                    'location': db_job.location,
                    'apply_link': db_job.apply_link,
                    'source': source
                })
                
            except IntegrityError as e:
                logger.warning(f"Integrity error for job {j.get('title')}: {str(e)}")
                db.rollback()
            except Exception as e:
                logger.error(f"DB save error for job {j.get('title')}: {str(e)}")
                db.rollback()
                
    finally:
        db.close()
    
    logger.info(f"Successfully saved {len(saved)} jobs to database")
    return saved

def clean_old_jobs(days_old: int = 7, source: str = 'zenrows') -> int:
    """
    Clean old jobs from database to prevent accumulation
    
    Args:
        days_old: Remove jobs older than this many days
        source: Only clean jobs from this source
        
    Returns:
        Number of jobs removed
    """
    db = SessionLocal()
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days_old)
        
        # Build query based on whether source column exists
        query = db.query(Job).filter(Job.posted_date < cutoff_date)
        
        if hasattr(Job, 'source'):
            query = query.filter(Job.source == source)
        
        old_jobs = query.all()
        count = len(old_jobs)
        
        for job in old_jobs:
            db.delete(job)
            
        db.commit()
        logger.info(f"Cleaned {count} old jobs from {source}")
        return count
        
    except Exception as e:
        logger.error(f"Failed to clean old jobs: {str(e)}")
        db.rollback()
        return 0
    finally:
        db.close()
