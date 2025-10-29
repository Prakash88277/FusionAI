"""
Simple job recommendation service that combines resume parsing, job scraping, and job matching
"""

import logging
from typing import List, Dict, Optional, Any
from fastapi import UploadFile
from app.services.simple_resume_parser import parse_resume
from app.services.simple_job_aggregator import simple_job_aggregator
from app.services.simple_job_matcher import simple_job_matcher
from app.models.job import Job, JobMatch
from app.models.resume import ResumeData

logger = logging.getLogger(__name__)

class SimpleJobRecommendationService:
    """Simple job recommendation service"""
    
    def __init__(self):
        self.logger = logging.getLogger("app.services.simple_job_recommendation_service")
        self.resume_cache: Dict[str, ResumeData] = {}
        self.recommendation_cache: Dict[str, List[JobMatch]] = {}
    
    async def process_resume_and_get_recommendations(
        self, 
        resume_file: UploadFile,
        job_sources: Optional[List[str]] = None,
        limit: int = 20,
        search_params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Process resume and get job recommendations in one call"""
        
        try:
            self.logger.info(f"Processing resume: {resume_file.filename}")
            
            # Step 1: Parse resume
            resume_data = await parse_resume(resume_file)
            self.logger.info(f"Parsed resume for: {resume_data.name}")
            
            # Cache resume data
            self.resume_cache[resume_data.id] = resume_data
            
            # Step 2: Scrape jobs
            if not search_params:
                search_params = {}
            
            # Add resume skills to search parameters
            if resume_data.skills:
                search_params['keywords'] = ' '.join(resume_data.skills[:5])  # Use top 5 skills
            
            # Scrape jobs
            if job_sources:
                jobs = await simple_job_aggregator.scrape_specific_sources(job_sources, search_params)
            else:
                jobs = await simple_job_aggregator.scrape_all_jobs(search_params)

            # Fallback to mock jobs if live scraping returns nothing
            if not jobs:
                self.logger.warning("No jobs from live scrapers; falling back to mock job service")
                jobs = await simple_job_aggregator.scrape_specific_sources(
                    simple_job_aggregator.get_available_sources(),
                    search_params
                )

            self.logger.info(f"Scraped {len(jobs)} jobs")
            
            # Step 3: Match jobs with resume
            job_recommendations = simple_job_matcher.match_jobs_with_resume(
                resume_data, jobs, limit, resume_data.country
            )
            
            # Cache recommendations
            self.recommendation_cache[resume_data.id] = job_recommendations
            
            self.logger.info(f"Generated {len(job_recommendations)} job recommendations")
            
            # Return result
            return {
                "resume_data": resume_data,
                "job_recommendations": job_recommendations,
                "total_jobs_scraped": len(jobs),
                "total_recommendations": len(job_recommendations),
                "sources_used": job_sources or simple_job_aggregator.get_available_sources(),
                "search_params": search_params
            }
            
        except Exception as e:
            self.logger.error(f"Error processing resume and getting recommendations: {e}")
            raise
    
    async def get_job_recommendations_by_resume_id(self, resume_id: str, limit: int = 20) -> Optional[List[JobMatch]]:
        """Get job recommendations for a previously parsed resume"""
        try:
            if resume_id in self.recommendation_cache:
                recommendations = self.recommendation_cache[resume_id]
                return recommendations[:limit]
            
            # If not in cache, try to get from resume cache and re-match
            if resume_id in self.resume_cache:
                resume_data = self.resume_cache[resume_id]
                
                # Get scraped jobs
                jobs = simple_job_aggregator.get_scraped_jobs()
                
                if jobs:
                    # Re-match jobs
                    recommendations = simple_job_matcher.match_jobs_with_resume(
                        resume_data, jobs, limit, resume_data.country
                    )
                    return recommendations
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting job recommendations: {e}")
            return None
    
    async def refresh_job_recommendations(self, resume_id: str, job_sources: Optional[List[str]] = None, limit: int = 20) -> Optional[List[JobMatch]]:
        """Refresh job recommendations for an existing resume"""
        try:
            if resume_id not in self.resume_cache:
                self.logger.error(f"Resume {resume_id} not found in cache")
                return None
            
            resume_data = self.resume_cache[resume_id]
            
            # Scrape fresh jobs
            search_params = {}
            if resume_data.skills:
                search_params['keywords'] = ' '.join(resume_data.skills[:5])
            
            if job_sources:
                jobs = await simple_job_aggregator.scrape_specific_sources(job_sources, search_params)
            else:
                jobs = await simple_job_aggregator.scrape_all_jobs(search_params)
            
            # Re-match jobs
            recommendations = simple_job_matcher.match_jobs_with_resume(
                resume_data, jobs, limit, resume_data.country
            )
            
            # Update cache
            self.recommendation_cache[resume_id] = recommendations
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Error refreshing job recommendations: {e}")
            return None
    
    def get_recommendation_stats(self, resume_id: str) -> Optional[Dict[str, Any]]:
        """Get statistics about job recommendations for a resume"""
        try:
            if resume_id not in self.recommendation_cache:
                return None
            
            recommendations = self.recommendation_cache[resume_id]
            
            if not recommendations:
                return {"total_recommendations": 0}
            
            # Calculate statistics
            total_recommendations = len(recommendations)
            avg_match_score = sum(r.match_score for r in recommendations) / total_recommendations
            max_match_score = max(r.match_score for r in recommendations)
            min_match_score = min(r.match_score for r in recommendations)
            
            # Count by source
            sources = {}
            for rec in recommendations:
                source = rec.job.source
                sources[source] = sources.get(source, 0) + 1
            
            # Count by company
            companies = {}
            for rec in recommendations:
                company = rec.job.company
                companies[company] = companies.get(company, 0) + 1
            
            return {
                "total_recommendations": total_recommendations,
                "average_match_score": round(avg_match_score, 2),
                "max_match_score": round(max_match_score, 2),
                "min_match_score": round(min_match_score, 2),
                "sources": sources,
                "companies": companies
            }
            
        except Exception as e:
            self.logger.error(f"Error getting recommendation stats: {e}")
            return None
    
    async def get_resume_data(self, resume_id: str) -> Optional[ResumeData]:
        """Get resume data by ID"""
        return self.resume_cache.get(resume_id)

# Create global instance
simple_job_recommendation_service = SimpleJobRecommendationService()
