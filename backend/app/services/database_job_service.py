"""
Database job service to fetch jobs from SQLite database
"""

import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from app.database.database import SessionLocal
from app.database.models import Job as DBJob
from app.models.job import Job, JobType, ExperienceLevel
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)

class DatabaseJobService:
    """Service to fetch jobs from the database"""
    
    def __init__(self):
        self.db = SessionLocal()
    
    def get_jobs(self, 
                 keywords: Optional[str] = None,
                 location: Optional[str] = None,
                 company: Optional[str] = None,
                 country: Optional[str] = None,
                 job_type: Optional[str] = None,
                 experience_level: Optional[str] = None,
                 salary_min: Optional[int] = None,
                 salary_max: Optional[int] = None,
                 limit: int = 100) -> List[Job]:
        """
        Get jobs from database with filtering
        """
        try:
            # Only get jobs from database - no external sources
            query = self.db.query(DBJob).filter(DBJob.is_active == True)
            
            # Apply filters
            if keywords:
                keyword_list = [k.strip().lower() for k in keywords.split(',') if k.strip()]
                if keyword_list:
                    # Search in title, description, and skills
                    keyword_conditions = []
                    for keyword in keyword_list:
                        keyword_conditions.append(
                            or_(
                                func.lower(DBJob.title).contains(keyword),
                                func.lower(DBJob.description).contains(keyword),
                                func.lower(DBJob.skills).contains(keyword)
                            )
                        )
                    query = query.filter(or_(*keyword_conditions))
            
            if location:
                query = query.filter(func.lower(DBJob.location).contains(location.lower()))
            
            if company:
                query = query.filter(func.lower(DBJob.company).contains(company.lower()))
            
            if job_type:
                query = query.filter(func.lower(DBJob.job_type) == job_type.lower())
            
            if salary_min:
                query = query.filter(DBJob.salary_min >= salary_min)
            
            if salary_max:
                query = query.filter(DBJob.salary_max <= salary_max)
            
            # Order by scraped date (newest first)
            query = query.order_by(DBJob.scraped_at.desc())
            
            # Apply limit
            db_jobs = query.limit(limit).all()
            
            logger.info(f"Found {len(db_jobs)} jobs in database")
            
            # Convert to API model
            jobs = []
            for db_job in db_jobs:
                try:
                    # Parse skills JSON
                    skills = []
                    if db_job.skills:
                        if isinstance(db_job.skills, str):
                            try:
                                skills = json.loads(db_job.skills)
                            except:
                                skills = [db_job.skills]
                        elif isinstance(db_job.skills, list):
                            skills = db_job.skills
                    
                    # Create Job model
                    job = Job(
                        id=str(db_job.id),
                        title=db_job.title or "",
                        company=db_job.company or "",
                        location=db_job.location or "",
                        description=db_job.description or "",
                        skills=skills,
                        skills_required=skills,  # Use same skills for required
                        apply_link=db_job.apply_link or "",
                        source=db_job.source or "database",
                        posted_date=db_job.posted_date or datetime.now(),
                        scraped_date=db_job.scraped_at or datetime.now(),
                        job_type=JobType.FULL_TIME if db_job.job_type == "full_time" else JobType.PART_TIME,
                        experience_level=ExperienceLevel.MID,  # Default
                        salary_min=db_job.salary_min,
                        salary_max=db_job.salary_max,
                        salary_currency="INR",
                        salary_text=db_job.salary_text or "",
                        is_active=db_job.is_active
                    )
                    jobs.append(job)
                    
                except Exception as e:
                    logger.error(f"Error converting job {db_job.id}: {e}")
                    continue
            
            logger.info(f"Successfully converted {len(jobs)} jobs")
            return jobs
            
        except Exception as e:
            logger.error(f"Error fetching jobs from database: {e}")
            return []
    
    def get_job_count(self) -> int:
        """Get total number of active jobs in database"""
        try:
            return self.db.query(DBJob).filter(DBJob.is_active == True).count()
        except Exception as e:
            logger.error(f"Error getting job count: {e}")
            return 0
    
    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        try:
            total_jobs = self.db.query(DBJob).count()
            active_jobs = self.db.query(DBJob).filter(DBJob.is_active == True).count()
            
            # Get jobs by source
            sources = self.db.query(DBJob.source, func.count(DBJob.id)).group_by(DBJob.source).all()
            jobs_by_source = {source: count for source, count in sources}
            
            return {
                "total_jobs": total_jobs,
                "active_jobs": active_jobs,
                "jobs_by_source": jobs_by_source
            }
        except Exception as e:
            logger.error(f"Error getting database stats: {e}")
            return {"total_jobs": 0, "active_jobs": 0, "jobs_by_source": {}}
    
    def close(self):
        """Close database connection"""
        if self.db:
            self.db.close()

# Global database job service instance
database_job_service = DatabaseJobService()
