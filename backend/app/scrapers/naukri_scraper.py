"""
Naukri.com job scraper
"""
from app.scrapers.base_scraper import BaseScraper
from typing import List, Dict
import logging
from datetime import datetime
import urllib.parse

logger = logging.getLogger(__name__)


class NaukriScraper(BaseScraper):
    """Scraper for Naukri.com jobs"""
    
    def __init__(self):
        super().__init__("naukri")
        self.base_url = "https://www.naukri.com"
    
    def scrape(self, keywords: List[str] = None, location: str = None, limit: int = 50) -> List[Dict]:
        """Scrape jobs from Naukri"""
        jobs = []
        
        try:
            # Build search URL
            search_term = " ".join(keywords) if keywords else "software engineer"
            encoded_term = urllib.parse.quote(search_term)
            
            url = f"{self.base_url}/{encoded_term}-jobs"
            
            if location:
                url += f"-in-{location.lower().replace(' ', '-')}"
            
            logger.info(f"Scraping Naukri: {url}")
            
            html = self.get_page(url)
            if not html:
                return jobs
            
            soup = self.parse_html(html)
            
            # Find job listings
            job_cards = soup.find_all('article', class_='jobTuple')
            
            for card in job_cards[:limit]:
                try:
                    job = self._parse_job_card(card)
                    if job:
                        jobs.append(self.normalize_job(job))
                except Exception as e:
                    logger.error(f"Error parsing Naukri job card: {str(e)}")
                    continue
            
            logger.info(f"[OK] Scraped {len(jobs)} jobs from Naukri")
            
        except Exception as e:
            logger.error(f"Error scraping Naukri: {str(e)}")
        
        return jobs
    
    def _parse_job_card(self, card) -> Dict:
        """Parse individual job card"""
        try:
            # Extract job details
            title_elem = card.find('a', class_='title')
            title = title_elem.text.strip() if title_elem else "N/A"
            
            company_elem = card.find('a', class_='subTitle')
            company = company_elem.text.strip() if company_elem else "N/A"
            
            location_elem = card.find('li', class_='location')
            location = location_elem.text.strip() if location_elem else "India"
            
            # Get job link
            job_link = title_elem['href'] if title_elem and 'href' in title_elem.attrs else ""
            if job_link and not job_link.startswith('http'):
                job_link = f"{self.base_url}{job_link}"
            
            # Extract job ID from link
            job_id = job_link.split('/')[-1] if job_link else f"naukri_{hash(title + company)}"
            
            # Get experience
            exp_elem = card.find('li', class_='experience')
            exp_text = exp_elem.text.strip() if exp_elem else ""
            experience = self.extract_experience(exp_text)
            
            # Get salary
            salary_elem = card.find('li', class_='salary')
            salary_text = salary_elem.text.strip() if salary_elem else None
            
            # Get description/skills
            desc_elem = card.find('ul', class_='tags')
            description = desc_elem.text.strip() if desc_elem else ""
            
            # Extract skills
            skills = self.extract_skills(description + " " + title)
            
            return {
                'job_id': f"naukri_{job_id}",
                'title': title,
                'company': company,
                'location': location,
                'description': description,
                'requirements': description,
                'skills': skills,
                'experience_min': experience,
                'experience_max': experience + 2 if experience else None,
                'job_type': 'full_time',
                'salary_text': salary_text,
                'apply_link': job_link,
                'posted_date': datetime.now(),
            }
        except Exception as e:
            logger.error(f"Error parsing Naukri job card: {str(e)}")
            return None
