"""
Base scraper class with common functionality
"""
import requests
from bs4 import BeautifulSoup
import time
import random
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseScraper:
    """Base class for all job scrapers"""
    
    def __init__(self, source_name: str):
        self.source_name = source_name
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def get_page(self, url: str, retries: int = 3) -> Optional[str]:
        """Fetch page content with retries"""
        for attempt in range(retries):
            try:
                response = self.session.get(url, timeout=15)
                response.raise_for_status()
                time.sleep(random.uniform(1, 3))  # Random delay to avoid detection
                return response.text
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed for {url}: {str(e)}")
                if attempt < retries - 1:
                    time.sleep(random.uniform(2, 5))
                else:
                    logger.error(f"Failed to fetch {url} after {retries} attempts")
                    return None
    
    def parse_html(self, html: str) -> BeautifulSoup:
        """Parse HTML content"""
        return BeautifulSoup(html, 'html.parser')
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract common tech skills from text"""
        common_skills = [
            # Programming Languages
            'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin',
            'go', 'rust', 'typescript', 'scala', 'r', 'matlab',
            
            # Web Technologies
            'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django',
            'flask', 'spring', 'asp.net', 'laravel', 'jquery',
            
            # Databases
            'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sqlite',
            'cassandra', 'dynamodb', 'elasticsearch',
            
            # Cloud & DevOps
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'ci/cd',
            'terraform', 'ansible', 'git', 'github', 'gitlab',
            
            # Data Science & ML
            'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'keras',
            'pandas', 'numpy', 'scikit-learn', 'nlp', 'computer vision',
            
            # Other
            'rest api', 'graphql', 'microservices', 'agile', 'scrum', 'jira',
            'linux', 'unix', 'bash', 'powershell', 'excel', 'tableau', 'power bi'
        ]
        
        text_lower = text.lower()
        found_skills = []
        
        for skill in common_skills:
            if skill in text_lower:
                found_skills.append(skill.title())
        
        return list(set(found_skills))  # Remove duplicates
    
    def extract_experience(self, text: str) -> Optional[int]:
        """Extract years of experience from text"""
        import re
        
        # Patterns to match experience
        patterns = [
            r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience)?',
            r'experience\s*:?\s*(\d+)\+?\s*(?:years?|yrs?)',
            r'(\d+)\+?\s*(?:years?|yrs?)',
        ]
        
        text_lower = text.lower()
        
        for pattern in patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                try:
                    return int(matches[0])
                except:
                    continue
        
        return None
    
    def scrape(self, keywords: List[str] = None, location: str = None, limit: int = 50) -> List[Dict]:
        """
        Scrape jobs - to be implemented by child classes
        
        Args:
            keywords: List of search keywords
            location: Job location
            limit: Maximum number of jobs to scrape
            
        Returns:
            List of job dictionaries
        """
        raise NotImplementedError("Subclasses must implement scrape() method")
    
    def normalize_job(self, job_data: Dict) -> Dict:
        """Normalize job data to standard format"""
        return {
            'job_id': job_data.get('job_id', ''),
            'title': job_data.get('title', ''),
            'company': job_data.get('company', ''),
            'location': job_data.get('location', ''),
            'description': job_data.get('description', ''),
            'requirements': job_data.get('requirements', ''),
            'skills': job_data.get('skills', []),
            'experience_min': job_data.get('experience_min'),
            'experience_max': job_data.get('experience_max'),
            'job_type': job_data.get('job_type', 'full_time'),
            'salary_text': job_data.get('salary_text'),
            'source': self.source_name,
            'apply_link': job_data.get('apply_link', ''),
            'posted_date': job_data.get('posted_date'),
        }
