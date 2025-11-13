"""
Enhanced resume upload and matching endpoints
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Dict
import logging

from app.database.database import get_db
from app.database.models import Resume, Job
from app.services.enhanced_resume_parser import enhanced_resume_parser
from app.services.job_matcher import job_matcher

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/upload-and-match")
async def upload_resume_and_match(
    file: UploadFile = File(...),
    limit: int = 50,
    min_match_score: float = 30.0,
    db: Session = Depends(get_db)
):
    """
    Upload resume, parse it, and match with jobs from database
    
    Args:
        file: Resume file (PDF or DOCX)
        limit: Maximum number of matches to return
        min_match_score: Minimum match score (0-100)
        
    Returns:
        Parsed resume data and matched jobs
    """
    try:
        logger.info(f"📄 Processing resume upload: {file.filename}")
        
        # Validate file type
        if not file.filename.endswith(('.pdf', '.docx')):
            raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported")
        
        # Parse resume
        resume_data = await enhanced_resume_parser.parse_resume(file)
        logger.info(f"✅ Resume parsed: {len(resume_data.skills)} skills, {resume_data.name}")
        
        # Save resume to database
        resume_db = Resume(
            resume_id=resume_data.id,
            filename=file.filename,
            name=resume_data.name,
            email=resume_data.email,
            phone="",  # Phone not extracted yet
            skills=resume_data.skills,
            experience_years=2.0,  # Default for now
            education=[edu.dict() for edu in resume_data.education],
            certifications=[],  # Not implemented yet
            raw_text=""  # Not storing raw text for now
        )
        db.add(resume_db)
        db.commit()
        db.refresh(resume_db)
        
        logger.info(f"💾 Resume saved to database with ID: {resume_db.id}")
        
        # Convert ResumeData to dict for job matching
        resume_dict = {
            "skills": resume_data.skills,
            "experience_years": 2.0,  # Default for now
            "name": resume_data.name,
            "email": resume_data.email,
            "education": [edu.dict() for edu in resume_data.education],
            "country": resume_data.country
        }
        
        # Match with jobs
        job_matches = job_matcher.match_resume_with_jobs(
            resume_data=resume_dict,
            db=db,
            limit=limit,
            min_match_score=min_match_score
        )
        
        logger.info(f"🎯 Found {len(job_matches)} matching jobs")
        
        # Save matches to database
        job_matcher.save_matches_to_db(
            resume_id=resume_db.id,
            job_matches=job_matches,
            db=db
        )
        
        return {
            "success": True,
            "resume_data": {
                "id": resume_db.id,
                "resume_id": resume_data.id,
                "name": resume_data.name,
                "email": resume_data.email,
                "skills": resume_data.skills,
                "experience_years": 2.0,
                "education": [edu.dict() for edu in resume_data.education],
                "country": resume_data.country
            },
            "job_matches": job_matches,
            "total_matches": len(job_matches)
        }
        
    except Exception as e:
        logger.error(f"❌ Error processing resume: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")


@router.get("/matches/{resume_id}")
async def get_resume_matches(
    resume_id: str,
    limit: int = 50,
    min_match_score: float = 30.0,
    db: Session = Depends(get_db)
):
    """
    Get job matches for a previously uploaded resume
    
    Args:
        resume_id: Resume ID
        limit: Maximum matches to return
        min_match_score: Minimum match score
        
    Returns:
        List of matched jobs
    """
    try:
        # Find resume in database
        resume = db.query(Resume).filter(Resume.resume_id == resume_id).first()
        
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
        
        # Get resume data
        resume_data = resume.to_dict()
        
        # Match with jobs
        job_matches = job_matcher.match_resume_with_jobs(
            resume_data=resume_data,
            db=db,
            limit=limit,
            min_match_score=min_match_score
        )
        
        return {
            "success": True,
            "resume_id": resume_id,
            "job_matches": job_matches,
            "total_matches": len(job_matches)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting matches: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting matches: {str(e)}")


@router.get("/stats")
async def get_database_stats(db: Session = Depends(get_db)):
    """Get statistics about jobs and resumes in database"""
    try:
        total_jobs = db.query(Job).count()
        active_jobs = db.query(Job).filter(Job.is_active == True).count()
        total_resumes = db.query(Resume).count()
        
        # Get jobs by source
        jobs_by_source = {}
        for source in ['internshala', 'naukri', 'google', 'meta', 'linkedin']:
            count = db.query(Job).filter(Job.source == source).count()
            if count > 0:
                jobs_by_source[source] = count
        
        return {
            "total_jobs": total_jobs,
            "active_jobs": active_jobs,
            "total_resumes": total_resumes,
            "jobs_by_source": jobs_by_source
        }
        
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
