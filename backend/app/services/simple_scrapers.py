"""
Simplified job scrapers using HTTP requests instead of Selenium
"""

import asyncio
import aiohttp
import logging
from datetime import datetime
from typing import List, Dict, Optional, Any
from bs4 import BeautifulSoup
from app.models.job import Job, JobType, ExperienceLevel
import uuid

logger = logging.getLogger(__name__)

class SimpleJobScraper:
    """Simple job scraper base class using HTTP requests"""
    
    def __init__(self, source_name: str):
        self.source_name = source_name
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }

    async def scrape_jobs(self, search_params: Dict[str, Any] = None) -> List[Job]:
        """Scrape jobs - to be implemented by subclasses"""
        return []

    def create_job(self, title: str, company: str, location: str = "", 
                   description: str = "", apply_link: str = "", 
                   salary: str = "", skills: List[str] = None) -> Job:
        """Create a Job object"""
        return Job(
            id=str(uuid.uuid4()),
            title=title,
            company=company,
            location=location,
            description=description,
            skills=skills or [],
            skills_required=(skills or []),
            apply_link=apply_link,
            source=self.source_name,
            posted_date=datetime.now(),
            scraped_date=datetime.now(),
            salary_text=salary,
            job_type=JobType.FULL_TIME,
            experience_level=ExperienceLevel.MID
        )

class SimpleLinkedInScraper(SimpleJobScraper):
    """Simplified LinkedIn scraper"""
    
    def __init__(self):
        super().__init__("LinkedIn")
        self.base_url = "https://www.linkedin.com/jobs/search"
    
    async def scrape_jobs(self, search_params: Dict[str, Any] = None) -> List[Job]:
        """Scrape jobs from LinkedIn"""
        jobs = []
        
        if not search_params:
            search_params = {}
        
        try:
            keywords = search_params.get('keywords', 'software engineer')
            location = search_params.get('location', '')
            limit = min(search_params.get('limit', 10), 20)
            
            # Create search URL
            params = {
                'keywords': keywords,
                'location': location,
                'start': 0
            }
            
            url = f"{self.base_url}?{self._build_params(params)}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers, timeout=10) as response:
                    if response.status == 200:
                        html = await response.text()
                        jobs = self._parse_linkedin_jobs(html, limit)
                        logger.info(f"LinkedIn scraper found {len(jobs)} jobs")
                    else:
                        logger.error(f"LinkedIn scraper failed with status {response.status}")
        
        except Exception as e:
            logger.error(f"LinkedIn scraper error: {e}")
        
        return jobs
    
    def _build_params(self, params: Dict[str, Any]) -> str:
        """Build URL parameters"""
        return "&".join([f"{k}={v}" for k, v in params.items() if v])
    
    def _parse_linkedin_jobs(self, html: str, limit: int) -> List[Job]:
        """Parse LinkedIn job listings from HTML"""
        jobs = []
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Look for job cards - LinkedIn uses various selectors
            job_cards = soup.find_all(['div'], class_=lambda x: x and 'job-card' in x.lower())
            
            if not job_cards:
                # Try alternative selectors
                job_cards = soup.find_all(['li'], class_=lambda x: x and 'job' in x.lower())
            
            for i, card in enumerate(job_cards[:limit]):
                try:
                    title_elem = card.find(['h3', 'h2', 'h1', 'a'], class_=lambda x: x and 'title' in x.lower())
                    title = title_elem.get_text(strip=True) if title_elem else f"Job {i+1}"
                    
                    company_elem = card.find(['h4', 'a', 'span'], class_=lambda x: x and 'company' in x.lower())
                    company = company_elem.get_text(strip=True) if company_elem else "Company"
                    
                    location_elem = card.find(['span', 'div'], class_=lambda x: x and 'location' in x.lower())
                    location = location_elem.get_text(strip=True) if location_elem else "Remote"
                    
                    # Create job
                    job = self.create_job(
                        title=title,
                        company=company,
                        location=location,
                        description=f"Software engineering position at {company}",
                        apply_link=f"https://linkedin.com/jobs/view/{i}",
                        skills=["python", "javascript", "react", "node.js"]
                    )
                    jobs.append(job)
                    
                except Exception as e:
                    logger.error(f"Error parsing LinkedIn job card {i}: {e}")
                    continue
        
        except Exception as e:
            logger.error(f"Error parsing LinkedIn HTML: {e}")
        
        return jobs

class SimpleGoogleCareersScraper(SimpleJobScraper):
    """Simplified Google Careers scraper"""
    
    def __init__(self):
        super().__init__("Google Careers")
        self.base_url = "https://careers.google.com/jobs/results"
    
    async def scrape_jobs(self, search_params: Dict[str, Any] = None) -> List[Job]:
        """Scrape jobs from Google Careers"""
        jobs = []
        
        if not search_params:
            search_params = {}
        
        try:
            keywords = search_params.get('keywords', 'software engineer')
            location = search_params.get('location', '')
            limit = min(search_params.get('limit', 10), 20)
            
            # Create search URL
            params = {
                'q': keywords,
                'location': location
            }
            
            url = f"{self.base_url}?{self._build_params(params)}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers, timeout=10) as response:
                    if response.status == 200:
                        html = await response.text()
                        jobs = self._parse_google_jobs(html, limit)
                        logger.info(f"Google Careers scraper found {len(jobs)} jobs")
                    else:
                        logger.error(f"Google Careers scraper failed with status {response.status}")
        
        except Exception as e:
            logger.error(f"Google Careers scraper error: {e}")
        
        return jobs
    
    def _build_params(self, params: Dict[str, Any]) -> str:
        """Build URL parameters"""
        return "&".join([f"{k}={v}" for k, v in params.items() if v])
    
    def _parse_google_jobs(self, html: str, limit: int) -> List[Job]:
        """Parse Google Careers job listings from HTML"""
        jobs = []
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Look for job cards
            job_cards = soup.find_all(['div'], class_=lambda x: x and 'job' in x.lower())
            
            for i, card in enumerate(job_cards[:limit]):
                try:
                    title_elem = card.find(['h3', 'h2', 'a'], class_=lambda x: x and 'title' in x.lower())
                    title = title_elem.get_text(strip=True) if title_elem else f"Google Job {i+1}"
                    
                    location_elem = card.find(['span', 'div'], class_=lambda x: x and 'location' in x.lower())
                    location = location_elem.get_text(strip=True) if location_elem else "Mountain View, CA"
                    
                    # Create job
                    job = self.create_job(
                        title=title,
                        company="Google",
                        location=location,
                        description=f"Software engineering position at Google",
                        apply_link=f"https://careers.google.com/jobs/results/{i}",
                        skills=["python", "java", "go", "kubernetes", "cloud"]
                    )
                    jobs.append(job)
                    
                except Exception as e:
                    logger.error(f"Error parsing Google job card {i}: {e}")
                    continue
        
        except Exception as e:
            logger.error(f"Error parsing Google Careers HTML: {e}")
        
        return jobs

class SimpleMicrosoftCareersScraper(SimpleJobScraper):
    """Simplified Microsoft Careers scraper"""
    
    def __init__(self):
        super().__init__("Microsoft Careers")
        self.base_url = "https://careers.microsoft.com/us/en/search-results"
    
    async def scrape_jobs(self, search_params: Dict[str, Any] = None) -> List[Job]:
        """Scrape jobs from Microsoft Careers"""
        jobs = []
        
        if not search_params:
            search_params = {}
        
        try:
            keywords = search_params.get('keywords', 'software engineer')
            location = search_params.get('location', '')
            limit = min(search_params.get('limit', 10), 20)
            
            # Create search URL
            params = {
                'q': keywords,
                'location': location
            }
            
            url = f"{self.base_url}?{self._build_params(params)}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers, timeout=10) as response:
                    if response.status == 200:
                        html = await response.text()
                        jobs = self._parse_microsoft_jobs(html, limit)
                        logger.info(f"Microsoft Careers scraper found {len(jobs)} jobs")
                    else:
                        logger.error(f"Microsoft Careers scraper failed with status {response.status}")
        
        except Exception as e:
            logger.error(f"Microsoft Careers scraper error: {e}")
        
        return jobs
    
    def _build_params(self, params: Dict[str, Any]) -> str:
        """Build URL parameters"""
        return "&".join([f"{k}={v}" for k, v in params.items() if v])
    
    def _parse_microsoft_jobs(self, html: str, limit: int) -> List[Job]:
        """Parse Microsoft Careers job listings from HTML"""
        jobs = []
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Look for job cards
            job_cards = soup.find_all(['div'], class_=lambda x: x and 'job' in x.lower())
            
            for i, card in enumerate(job_cards[:limit]):
                try:
                    title_elem = card.find(['h3', 'h2', 'a'], class_=lambda x: x and 'title' in x.lower())
                    title = title_elem.get_text(strip=True) if title_elem else f"Microsoft Job {i+1}"
                    
                    location_elem = card.find(['span', 'div'], class_=lambda x: x and 'location' in x.lower())
                    location = location_elem.get_text(strip=True) if location_elem else "Redmond, WA"
                    
                    # Create job
                    job = self.create_job(
                        title=title,
                        company="Microsoft",
                        location=location,
                        description=f"Software engineering position at Microsoft",
                        apply_link=f"https://careers.microsoft.com/us/en/jobs/{i}",
                        skills=["c#", "azure", "dotnet", "sql", "powershell"]
                    )
                    jobs.append(job)
                    
                except Exception as e:
                    logger.error(f"Error parsing Microsoft job card {i}: {e}")
                    continue
        
        except Exception as e:
            logger.error(f"Error parsing Microsoft Careers HTML: {e}")
        
        return jobs

class SimpleInternshalaScraper(SimpleJobScraper):
    """Simplified Internshala scraper"""
    
    def __init__(self):
        super().__init__("Internshala")
        self.base_url = "https://internshala.com/internships"
    
    async def scrape_jobs(self, search_params: Dict[str, Any] = None) -> List[Job]:
        """Scrape jobs from Internshala"""
        jobs = []
        
        if not search_params:
            search_params = {}
        
        try:
            keywords = search_params.get('keywords', 'software engineer')
            location = search_params.get('location', '')
            limit = min(search_params.get('limit', 10), 20)
            
            # Create search URL
            params = {
                'keywords': keywords,
                'location': location
            }
            
            url = f"{self.base_url}?{self._build_params(params)}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers, timeout=10) as response:
                    if response.status == 200:
                        html = await response.text()
                        jobs = self._parse_internshala_jobs(html, limit)
                        logger.info(f"Internshala scraper found {len(jobs)} jobs")
                    else:
                        logger.error(f"Internshala scraper failed with status {response.status}")
        
        except Exception as e:
            logger.error(f"Internshala scraper error: {e}")
        
        return jobs
    
    def _build_params(self, params: Dict[str, Any]) -> str:
        """Build URL parameters"""
        return "&".join([f"{k}={v}" for k, v in params.items() if v])
    
    def _parse_internshala_jobs(self, html: str, limit: int) -> List[Job]:
        """Parse Internshala job listings from HTML"""
        jobs = []
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Look for job cards
            job_cards = soup.find_all(['div'], class_=lambda x: x and 'internship' in x.lower())
            
            for i, card in enumerate(job_cards[:limit]):
                try:
                    title_elem = card.find(['h3', 'h2', 'a'], class_=lambda x: x and 'title' in x.lower())
                    title = title_elem.get_text(strip=True) if title_elem else f"Internship {i+1}"
                    
                    company_elem = card.find(['h4', 'a', 'span'], class_=lambda x: x and 'company' in x.lower())
                    company = company_elem.get_text(strip=True) if company_elem else "Company"
                    
                    location_elem = card.find(['span', 'div'], class_=lambda x: x and 'location' in x.lower())
                    location = location_elem.get_text(strip=True) if location_elem else "India"
                    
                    # Extract salary if available
                    salary_elem = card.find(['span', 'div'], class_=lambda x: x and 'salary' in x.lower())
                    salary = salary_elem.get_text(strip=True) if salary_elem else "Stipend available"
                    
                    # Create job
                    job = self.create_job(
                        title=title,
                        company=company,
                        location=location,
                        description=f"Internship opportunity at {company}",
                        apply_link=f"https://internshala.com/internship/detail/{i}",
                        salary=salary,
                        skills=["python", "web development", "data analysis", "machine learning"]
                    )
                    jobs.append(job)
                    
                except Exception as e:
                    logger.error(f"Error parsing Internshala job card {i}: {e}")
                    continue
        
        except Exception as e:
            logger.error(f"Error parsing Internshala HTML: {e}")
        
        return jobs

# Create instances
simple_linkedin_scraper = SimpleLinkedInScraper()
simple_google_scraper = SimpleGoogleCareersScraper()
simple_microsoft_scraper = SimpleMicrosoftCareersScraper()
simple_internshala_scraper = SimpleInternshalaScraper()
