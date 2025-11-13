from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.simple_resume_parser import parse_resume
from app.services.enhanced_resume_parser import parse_resume_enhanced
from app.services.simple_job_recommendation_service import simple_job_recommendation_service
from app.models.resume import ResumeData
from typing import List, Dict

router = APIRouter()

@router.post("/upload", response_model=ResumeData)
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload and parse a resume file (PDF/DOCX)
    """
    # Check file extension
    if not file.filename.endswith(('.pdf', '.docx')):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported")
    
    try:
        # Parse resume using enhanced parser
        resume_data = await parse_resume_enhanced(file)
        return resume_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing resume: {str(e)}")

@router.post("/upload-and-recommend", response_model=Dict)
async def upload_and_recommend_jobs(
    file: UploadFile = File(...),
    job_sources: str = "all",
    limit: int = 20
):
    """
    Upload resume and get job recommendations in one call
    """
    import logging
    logger = logging.getLogger(__name__)
    
    # Check file extension
    if not file.filename.endswith(('.pdf', '.docx')):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported")
    
    try:
        logger.info(f"Starting resume upload and recommendation for file: {file.filename}")
        
        # Determine job sources
        if job_sources.lower() == "all":
            sources_to_scrape = None
        else:
            sources_to_scrape = [s.strip() for s in job_sources.split(',')]
        
        logger.info(f"Job sources: {sources_to_scrape}, Limit: {limit}")
        
        # Process resume and get recommendations
        result = await simple_job_recommendation_service.process_resume_and_get_recommendations(
            resume_file=file,
            job_sources=sources_to_scrape,
            limit=limit
        )
        
        logger.info(f"Successfully processed resume. Found {len(result.get('job_recommendations', []))} jobs")
        return result
        
    except Exception as e:
        logger.error(f"Error in upload_and_recommend_jobs: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")