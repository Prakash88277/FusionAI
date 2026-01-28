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
# from app.services.job_matcher import job_matcher
import httpx

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/upload-and-match")
async def upload_resume_and_match(
    file: UploadFile = File(...),
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    Upload resume, parse it, and match with jobs via n8n webhook
    
    Args:
        file: Resume file (PDF or DOCX)
        limit: Maximum number of matches to return (default: 20)
        
    Returns:
        Matched jobs directly from n8n
    """
    try:
        logger.info(f"📄 Processing resume upload: {file.filename}")
        
        # Validate file type
        if not file.filename.endswith(('.pdf', '.docx')):
            raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported")
        
        # Parse resume
        resume_data = await enhanced_resume_parser.parse_resume(file)
        logger.info(f"✅ Resume parsed: {len(resume_data.skills)} skills")
        
        # Extract experience string (e.g., "2 years")
        experience = "0 years"
        if resume_data.experience and len(resume_data.experience) > 0:
            experience = resume_data.experience[0].duration
            
        # Prepare payload for n8n
        payload = {
            "skills": resume_data.skills,
            "experience": experience,
            "location": resume_data.country,
            "limit": limit
        }
        
        logger.info(f"🚀 Sending to n8n: {payload}")
        
        # Call n8n webhook
        webhook_url = "https://tempmail88277.app.n8n.cloud/webhook-test/3d0f11da-ba1a-4f8d-a228-cf6c80c7bc4f"
        
        async with httpx.AsyncClient() as client:
            response = await client.post(webhook_url, json=payload, timeout=120.0)
            
            if response.status_code != 200:
                logger.error(f"❌ n8n Error: {response.text}")
                raise HTTPException(status_code=502, detail="Failed to get matches from matching service")
                
            n8n_data = response.json()
            
            # Debug n8n response
            logger.info(f"🔍 n8n Response Type: {type(n8n_data)}")
            if isinstance(n8n_data, list):
                logger.info(f"✅ Received {len(n8n_data)} items from n8n")
            elif isinstance(n8n_data, dict):
                logger.warning("⚠️ Received SINGLE DICT from n8n (expected List)")
                logger.info(f"Keys: {list(n8n_data.keys())}")
            else:
                logger.warning(f"⚠️ Received unexpected type: {type(n8n_data)}")

            logger.info("✅ Received matches from n8n")
            return n8n_data
        
    except HTTPException:
        raise
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
