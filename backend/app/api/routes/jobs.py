from fastapi import APIRouter, HTTPException, Query, BackgroundTasks, UploadFile, File
from app.services.simple_job_aggregator import simple_job_aggregator
from app.services.mock_job_service import mock_job_service
from app.services.simple_job_matcher import simple_job_matcher
from app.services.simple_job_recommendation_service import simple_job_recommendation_service
from app.models.job import Job, JobMatch, JobSearchFilters, JobType, ExperienceLevel
from app.models.resume import ResumeData
from typing import List, Optional
import asyncio
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/recommendations", response_model=dict)
async def get_job_recommendations(
    resume_file: UploadFile = File(..., description="Resume file (PDF or DOCX)"),
    job_sources: str = Query("all", description="Comma-separated list of sources"),
    limit: int = Query(20, description="Maximum number of recommendations"),
    keywords: str = Query(None, description="Additional keywords to search for"),
    location: str = Query(None, description="Preferred job location"),
    salary_min: int = Query(None, description="Minimum salary"),
    salary_max: int = Query(None, description="Maximum salary")
):
    """
    Complete workflow: Parse resume -> Scrape jobs -> Match jobs -> Return recommendations
    """
    try:
        # Validate file type
        if not resume_file.filename.endswith(('.pdf', '.docx')):
            raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported")
        
        # Prepare additional search parameters
        additional_params = {}
        if keywords:
            additional_params['keywords'] = keywords
        if location:
            additional_params['location'] = location
        if salary_min:
            additional_params['salary_min'] = salary_min
        if salary_max:
            additional_params['salary_max'] = salary_max
        
        # Determine job sources
        if job_sources.lower() == "all":
            sources_to_scrape = None
        else:
            sources_to_scrape = [s.strip() for s in job_sources.split(',')]
        
        # Process resume and get recommendations
        result = await simple_job_recommendation_service.process_resume_and_get_recommendations(
            resume_file=resume_file,
            job_sources=sources_to_scrape,
            limit=limit,
            search_params=additional_params if additional_params else None
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing resume and getting recommendations: {str(e)}")

@router.get("/recommendations/{resume_id}", response_model=List[JobMatch])
async def get_recommendations_by_resume_id(
    resume_id: str,
    limit: int = Query(20, description="Maximum number of recommendations")
):
    """
    Get job recommendations for a previously parsed resume
    """
    try:
        recommendations = await simple_job_recommendation_service.get_job_recommendations_by_resume_id(
            resume_id, limit
        )
        
        if recommendations is None:
            raise HTTPException(status_code=404, detail="Resume not found or no recommendations available")
        
        return recommendations
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting recommendations: {str(e)}")

@router.post("/recommendations/{resume_id}/refresh", response_model=List[JobMatch])
async def refresh_recommendations(
    resume_id: str,
    job_sources: str = Query("all", description="Comma-separated list of sources"),
    limit: int = Query(20, description="Maximum number of recommendations")
):
    """
    Refresh job recommendations for an existing resume
    """
    try:
        # Determine job sources
        if job_sources.lower() == "all":
            sources_to_scrape = None
        else:
            sources_to_scrape = [s.strip() for s in job_sources.split(',')]
        
        recommendations = await simple_job_recommendation_service.refresh_job_recommendations(
            resume_id, sources_to_scrape, limit
        )
        
        if recommendations is None:
            raise HTTPException(status_code=404, detail="Resume not found")
        
        return recommendations
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error refreshing recommendations: {str(e)}")

@router.get("/recommendations/{resume_id}/stats", response_model=dict)
async def get_recommendation_stats(resume_id: str):
    """
    Get statistics about job recommendations for a resume
    """
    try:
        stats = simple_job_recommendation_service.get_recommendation_stats(resume_id)
        
        if stats is None:
            raise HTTPException(status_code=404, detail="Resume not found")
        
        return stats
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting recommendation stats: {str(e)}")

@router.get("/resume/{resume_id}", response_model=ResumeData)
async def get_resume_data(resume_id: str):
    """
    Get parsed resume data by ID
    """
    try:
        resume_data = await simple_job_recommendation_service.get_resume_data(resume_id)
        
        if resume_data is None:
            raise HTTPException(status_code=404, detail="Resume not found")
        
        return resume_data
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting resume data: {str(e)}")

@router.post("/scrape", response_model=List[Job])
async def scrape_jobs(
    keywords: str = Query("software engineer", description="Keywords to search for"),
    location: str = Query("", description="Job location"),
    company: str = Query(None, description="Company name"),
    country: str = Query(None, description="Country to filter jobs by"),
    sources: str = Query("all", description="Comma-separated list of sources (linkedin,google_careers,microsoft_careers,internshala,indeed,glassdoor)"),
    limit: int = Query(50, description="Maximum number of results per source")
):
    """
    Scrape jobs from multiple sources
    """
    try:
        # Prepare search parameters
        search_params = {
            'keywords': keywords,
            'location': location,
            'company': company,
            'country': country,
            'limit': limit
        }
        
        # Determine which sources to scrape
        if sources.lower() == "all":
            sources_to_scrape = simple_job_aggregator.get_available_sources()
        else:
            sources_to_scrape = [s.strip() for s in sources.split(',')]

        # Scrape jobs from specified sources
        jobs = await simple_job_aggregator.scrape_specific_sources(sources_to_scrape, search_params)
        
        return jobs[:limit * len(sources_to_scrape)]  # Limit total results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scraping jobs: {str(e)}")

@router.get("/search", response_model=List[Job])
async def search_jobs(
    keywords: str = Query(None, description="Keywords to search for"),
    location: str = Query(None, description="Job location"),
    company: str = Query(None, description="Company name"),
    country: str = Query(None, description="Country to filter jobs by"),
    job_type: Optional[JobType] = Query(None, description="Job type filter"),
    experience_level: Optional[ExperienceLevel] = Query(None, description="Experience level filter"),
    salary_min: Optional[int] = Query(None, description="Minimum salary"),
    salary_max: Optional[int] = Query(None, description="Maximum salary"),
    remote_only: Optional[bool] = Query(None, description="Remote jobs only"),
    posted_within_days: Optional[int] = Query(None, description="Posted within last N days"),
    limit: int = Query(20, description="Maximum number of results")
):
    """
    Search for jobs from scraped data with advanced filtering
    """
    try:
        # Create search filters
        filters = JobSearchFilters(
            keywords=[keywords] if keywords else None,
            location=location,
            country=country,
            company=company,
            job_type=job_type,
            experience_level=experience_level,
            salary_min=salary_min,
            salary_max=salary_max,
            remote_only=remote_only,
            posted_within_days=posted_within_days
        )
        
        # Get filtered jobs from aggregator
        jobs = simple_job_aggregator.get_scraped_jobs(filters)

        # Seed with mock jobs if none available to prevent empty UI
        if not jobs:
            base_search = {
                'keywords': keywords or '',
                'location': location or '',
                'company': company or '',
                'country': country or ''
            }
            mock_jobs = mock_job_service.get_jobs(base_search)
            # Extend aggregator storage for subsequent requests
            simple_job_aggregator.scraped_jobs.extend(mock_jobs)
            jobs = simple_job_aggregator.get_scraped_jobs(filters)
        
        return jobs[:limit]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching jobs: {str(e)}")

@router.post("/scrape-background")
async def scrape_jobs_background(
    background_tasks: BackgroundTasks,
    keywords: str = Query("software engineer", description="Keywords to search for"),
    location: str = Query("", description="Job location"),
    sources: str = Query("all", description="Comma-separated list of sources")
):
    """
    Start background job scraping
    """
    try:
        # Prepare search parameters
        search_params = {
            'keywords': keywords,
            'location': location
        }
        
        # Determine which sources to scrape
        if sources.lower() == "all":
            sources_to_scrape = simple_job_aggregator.get_available_sources()
        else:
            sources_to_scrape = [s.strip() for s in sources.split(',')]

        # Add background task
        background_tasks.add_task(
            simple_job_aggregator.scrape_specific_sources,
            sources_to_scrape,
            search_params
        )
        
        return {"message": f"Background scraping started for sources: {sources_to_scrape}"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting background scraping: {str(e)}")

@router.get("/match/{resume_id}", response_model=List[JobMatch])
async def match_jobs(
    resume_id: str,
    country: str = Query(None, description="Country to filter jobs by"),
    limit: int = Query(20, description="Maximum number of results")
):
    """
    Match jobs with a parsed resume
    """
    try:
        # Get resume data and jobs, then match
        resume_data = await simple_job_recommendation_service.get_resume_data(resume_id)
        if not resume_data:
            raise HTTPException(status_code=404, detail="Resume not found")
        
        jobs = simple_job_aggregator.get_scraped_jobs()
        matched_jobs = simple_job_matcher.match_jobs_with_resume(resume_data, jobs, limit, country)
        return matched_jobs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error matching jobs: {str(e)}")

@router.get("/sources")
async def get_available_sources():
    """
    Get list of available job sources
    """
    try:
        sources = simple_job_aggregator.get_available_sources()
        status = simple_job_aggregator.get_scraper_status()

        return {
            "available_sources": sources,
            "active_sources": simple_job_aggregator.active_scrapers,
            "scraper_status": status
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting sources: {str(e)}")

@router.post("/sources/activate")
async def activate_sources(sources: List[str]):
    """
    Activate specific job sources
    """
    try:
        simple_job_aggregator.set_active_scrapers(sources)
        return {"message": f"Activated sources: {simple_job_aggregator.active_scrapers}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error activating sources: {str(e)}")

@router.get("/scheduler/status")
async def get_scheduler_status():
    """
    Get job scheduler status
    """
    try:
        status = job_scheduler.get_scheduler_status()
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting scheduler status: {str(e)}")

@router.post("/scheduler/start")
async def start_scheduler(interval_seconds: int = Query(3600, description="Scraping interval in seconds")):
    """
    Start the job scheduler
    """
    # The simple aggregator does not have a scheduler, return a dummy message
    return {"message": "Scheduler not available in simple mode"}

@router.post("/scheduler/stop")
async def stop_scheduler():
    """
    Stop the job scheduler
    """
    # The simple aggregator does not have a scheduler, return a dummy message
    return {"message": "Scheduler not available in simple mode"}

@router.get("/stats")
async def get_job_stats():
    """
    Get job scraping statistics
    """
    try:
        all_jobs = simple_job_aggregator.get_scraped_jobs()

        # Calculate statistics
        stats = {
            "total_jobs": len(all_jobs),
            "jobs_by_source": {},
            "jobs_by_country": {},
            "jobs_by_company": {},
            "recent_jobs": 0
        }
        
        # Count jobs by source
        for job in all_jobs:
            source = job.source
            if source not in stats["jobs_by_source"]:
                stats["jobs_by_source"][source] = 0
            stats["jobs_by_source"][source] += 1
            
            # Count jobs by country
            if job.country:
                if job.country not in stats["jobs_by_country"]:
                    stats["jobs_by_country"][job.country] = 0
                stats["jobs_by_country"][job.country] += 1
            
            # Count jobs by company
            if job.company:
                if job.company not in stats["jobs_by_company"]:
                    stats["jobs_by_company"][job.company] = 0
                stats["jobs_by_company"][job.company] += 1
            
            # Count recent jobs (last 24 hours)
            if job.scraped_date and job.scraped_date > datetime.now() - timedelta(hours=24):
                stats["recent_jobs"] += 1
        
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting job stats: {str(e)}")

@router.get("/{job_id}", response_model=Job)
async def get_job(job_id: str):
    """
    Retrieve a single job by its ID
    """
    try:
        all_jobs = simple_job_aggregator.get_scraped_jobs()
        job = next((j for j in all_jobs if j.id == job_id), None)
        
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        return job
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving job: {str(e)}")