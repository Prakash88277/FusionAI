"""
Simple job aggregator using HTTP-based scrapers
"""

import asyncio
import logging
from datetime import datetime
from typing import List, Dict, Optional, Any
from app.services.simple_scrapers import (
    simple_linkedin_scraper,
    simple_google_scraper, 
    simple_microsoft_scraper,
    simple_internshala_scraper
)
from app.models.job import Job, JobSearchFilters
from app.services.mock_job_service import mock_job_service

logger = logging.getLogger(__name__)

class SimpleJobAggregator:
    """Simple job aggregator using HTTP-based scrapers"""
    
    def __init__(self):
        self.scrapers = {
            'linkedin': simple_linkedin_scraper,
            'google_careers': simple_google_scraper,
            'microsoft_careers': simple_microsoft_scraper,
            'internshala': simple_internshala_scraper
        }
        self.active_scrapers = list(self.scrapers.keys())
        self.scraped_jobs: List[Job] = []
    
    async def scrape_all_jobs(self, search_params: Dict[str, Any] = None) -> List[Job]:
        """Scrape jobs from all active sources"""
        all_jobs = []
        
        if not search_params:
            search_params = {}
        
        logger.info(f"Starting job scraping from {len(self.active_scrapers)} sources")
        
        # Create tasks for concurrent scraping
        tasks = []
        for source_name in self.active_scrapers:
            scraper = self.scrapers[source_name]
            task = asyncio.create_task(self._scrape_source(scraper, source_name, search_params))
            tasks.append(task)
        
        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Collect results
        for i, result in enumerate(results):
            source_name = self.active_scrapers[i]
            if isinstance(result, Exception):
                logger.error(f"Error scraping {source_name}: {result}")
            else:
                all_jobs.extend(result)
                logger.info(f"Scraped {len(result)} jobs from {source_name}")
        
        # Store scraped jobs
        self.scraped_jobs.extend(all_jobs)
        
        logger.info(f"Total jobs scraped: {len(all_jobs)}")
        return all_jobs
    
    async def _scrape_source(self, scraper, source_name: str, search_params: Dict[str, Any]) -> List[Job]:
        """Scrape jobs from a single source"""
        try:
            logger.info(f"Scraping jobs from {source_name}")
            jobs = await scraper.scrape_jobs(search_params)
            logger.info(f"Successfully scraped {len(jobs)} jobs from {source_name}")
            return jobs
        except Exception as e:
            logger.error(f"Error scraping {source_name}: {e}")
            return []
    
    async def scrape_specific_sources(self, sources: List[str], search_params: Dict[str, Any]) -> List[Job]:
        """Scrape jobs from specific sources - using mock data for testing"""
        logger.info(f"Using mock job service for sources: {sources}")
        
        # Use mock job service for testing
        mock_jobs = mock_job_service.get_jobs(search_params)
        
        # Store mock jobs
        self.scraped_jobs.extend(mock_jobs)
        
        logger.info(f"Total mock jobs returned: {len(mock_jobs)}")
        return mock_jobs
    
    def get_scraped_jobs(self, filters: Optional[JobSearchFilters] = None) -> List[Job]:
        """Get scraped jobs with optional filtering"""
        jobs = self.scraped_jobs.copy()
        
        if not filters:
            return jobs
        
        # Apply filters
        if filters.keywords:
            keyword_matches = []
            for job in jobs:
                job_text = f"{job.title} {job.description} {' '.join(job.skills)}".lower()
                if any(keyword.lower() in job_text for keyword in filters.keywords):
                    keyword_matches.append(job)
            jobs = keyword_matches
        
        if filters.location:
            jobs = [job for job in jobs if filters.location.lower() in job.location.lower()]
        
        if filters.company:
            jobs = [job for job in jobs if filters.company.lower() in job.company.lower()]
        
        if filters.salary_min:
            jobs = [job for job in jobs if self._extract_salary_min(job) >= filters.salary_min]
        
        if filters.salary_max:
            jobs = [job for job in jobs if self._extract_salary_max(job) <= filters.salary_max]
        
        return jobs
    
    def _extract_salary_min(self, job: Job) -> int:
        """Extract minimum salary from job"""
        if job.salary_min:
            return job.salary_min
        if job.salary_text:
            # Simple salary extraction
            import re
            numbers = re.findall(r'\d+', job.salary_text)
            if numbers:
                return int(numbers[0])
        return 0
    
    def _extract_salary_max(self, job: Job) -> int:
        """Extract maximum salary from job"""
        if job.salary_max:
            return job.salary_max
        if job.salary_text:
            # Simple salary extraction
            import re
            numbers = re.findall(r'\d+', job.salary_text)
            if len(numbers) > 1:
                return int(numbers[1])
            elif len(numbers) == 1:
                return int(numbers[0])
        return 999999
    
    def get_available_sources(self) -> List[str]:
        """Get list of available sources"""
        return list(self.scrapers.keys())
    
    def set_active_scrapers(self, sources: List[str]):
        """Set active scrapers"""
        self.active_scrapers = [s for s in sources if s in self.scrapers]
        logger.info(f"Active scrapers set to: {self.active_scrapers}")
    
    def get_scraper_status(self) -> Dict[str, bool]:
        """Get status of all scrapers"""
        return {source: True for source in self.scrapers.keys()}

# Create global instance
simple_job_aggregator = SimpleJobAggregator()
