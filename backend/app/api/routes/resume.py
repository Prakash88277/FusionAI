from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.services.resume_parser import resume_parser
from app.services.simple_job_recommendation_service import simple_job_recommendation_service
from app.services.zenrows_job_service import upsert_jobs_from_keywords
from app.services.job_matcher import JobMatcher
from app.database.database import get_db
from sqlalchemy.orm import Session
from typing import Dict, List
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/test")
async def test_endpoint():
    """Test endpoint to verify router is working"""
    return {"message": "Resume router is working", "parser_loaded": True}

@router.post("/upload-text")
async def upload_text_resume(file: UploadFile = File(...)):
    """
    Test endpoint that accepts plain text and parses it directly
    """
    try:
        logger.info(f"Received text file upload: {file.filename}")
        
        # Read file content as text
        content = await file.read()
        text = content.decode('utf-8')
        logger.info(f"Text content length: {len(text)}")
        
        # Parse using individual parser methods
        skills = resume_parser.extract_skills(text)
        roles = resume_parser.extract_roles(text)
        experience = resume_parser.extract_experience(text)
        domain = resume_parser.detect_domain(skills)
        keywords = resume_parser.extract_keywords(text)
        name = resume_parser._extract_name(text)
        email = resume_parser._extract_email(text)
        phone = resume_parser._extract_phone(text)
        
        parsed_data = {
            "name": name,
            "email": email,
            "phone": phone,
            "skills": skills,
            "roles": roles,
            "experience": experience,
            "domain": domain,
            "keywords": keywords,
            "text_length": len(text),
            "skills_count": len(skills)
        }
        
        logger.info(f"Text parsed successfully: {len(skills)} skills found")
        return {"status": "success", "parsed_data": parsed_data}
        
    except Exception as e:
        logger.error(f"Error parsing text: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error parsing text: {str(e)}")

@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload and parse a resume file, trigger live job scraping, and return matches
    """
    try:
        logger.info(f"Received file upload: {file.filename}, content_type: {file.content_type}")
        
        # Check file extension
        if not file.filename.endswith(('.pdf', '.docx')):
            logger.warning(f"Unsupported file type: {file.filename}")
            raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported")
        
        # Read file content
        logger.info("Reading file content...")
        content = await file.read()
        logger.info(f"File content read: {len(content)} bytes")
        
        # Parse resume using new parser
        logger.info("Starting resume parsing...")
        parsed_data = resume_parser.parse(content, file.filename)
        logger.info(f"Resume parsed successfully: {len(parsed_data.get('skills', []))} skills found")
        
        # Build query terms from skills + top keywords
        skills = parsed_data.get('skills', [])
        keywords = parsed_data.get('keywords', [])
        roles = parsed_data.get('roles', [])
        
        # Combine and deduplicate query terms
        query_terms = []
        for term_list in [skills, keywords, roles]:
            for term in term_list:
                if term and isinstance(term, str) and term.lower() not in [t.lower() for t in query_terms]:
                    query_terms.append(term)
        
        # Limit to top 10 terms for better search results
        query_terms = query_terms[:10]
        logger.info(f"Built query terms for job search: {query_terms}")
        
        # Trigger live job scraping via ZenRows
        try:
            logger.info("Starting live job scraping...")
            scraped_jobs = upsert_jobs_from_keywords(query_terms, source='zenrows', max_jobs=50)
            logger.info(f"Scraped and saved {len(scraped_jobs)} jobs")
        except Exception as e:
            logger.warning(f"Job scraping failed: {str(e)}. Continuing with existing jobs...")
            scraped_jobs = []
        
        # Run job matching with existing matcher
        try:
            logger.info("Running job matching...")
            job_matcher = JobMatcher()
            matches = job_matcher.match_resume_with_jobs(parsed_data, db, top_k=20)
            logger.info(f"Found {len(matches)} job matches")
        except Exception as e:
            logger.warning(f"Job matching failed: {str(e)}")
            matches = []
        
        return {
            "status": "success", 
            "parsed_data": parsed_data,
            "scraped_jobs_count": len(scraped_jobs),
            "matches": matches,
            "query_terms": query_terms
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Unexpected error processing resume {file.filename}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")

@router.post("/upload-and-recommend")
async def upload_and_recommend_jobs(
    file: UploadFile = File(...),
    job_sources: str = "all",
    limit: int = 20
):
    """
    Upload resume and get job recommendations using new parser
    """
    # Check file extension
    if not file.filename.endswith(('.pdf', '.docx')):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported")
    
    try:
        logger.info(f"Starting resume upload and recommendation for file: {file.filename}")
        
        # Read file content
        content = await file.read()
        
        # Parse resume using new parser
        parsed_data = resume_parser.parse(content, file.filename)
        
        # For now, return parsed data - job matching integration can be added later
        logger.info(f"Successfully parsed resume: {len(parsed_data.get('skills', []))} skills found")
        
        return {
            "status": "success",
            "parsed_data": parsed_data,
            "message": "Resume parsed successfully. Job matching integration pending."
        }
        
    except Exception as e:
        logger.error(f"Error in upload_and_recommend_jobs: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")