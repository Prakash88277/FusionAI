"""
Internshala job scraper
"""
from app.scrapers.base_scraper import BaseScraper
from typing import List, Dict
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)


class IntershalaScraper(BaseScraper):
    """Scraper for Internshala jobs"""
    
    def __init__(self):
        super().__init__("internshala")
        self.base_url = "https://internshala.com"
    
    def scrape(self, keywords: List[str] = None, location: str = None, limit: int = 50) -> List[Dict]:
        """Scrape jobs from Internshala"""
        jobs = []
        
        try:
            # Build search URL
            search_term = "+".join(keywords) if keywords else "software"
            url = f"{self.base_url}/jobs/{search_term}-jobs"
            
            if location:
                url += f"-in-{location.lower().replace(' ', '-')}"
            
            logger.info(f"Scraping Internshala: {url}")
            
            html = self.get_page(url)
            if not html:
                return jobs
            
            soup = self.parse_html(html)
            
            # Find job listings
            job_cards = soup.find_all('div', class_='individual_internship')
            
            for card in job_cards[:limit]:
                try:
                    job = self._parse_job_card(card)
                    if job:
                        jobs.append(self.normalize_job(job))
                except Exception as e:
                    logger.error(f"Error parsing Internshala job card: {str(e)}")
                    continue
            
            logger.info(f"[OK] Scraped {len(jobs)} jobs from Internshala")
            
        except Exception as e:
            logger.error(f"Error scraping Internshala: {str(e)}")
        
        return jobs
    
    def _parse_job_card(self, card) -> Dict:
        """Parse individual job card"""
        try:
            # Extract job details
            title_elem = card.find('h3', class_='job-internship-name')
            title = title_elem.text.strip() if title_elem else "N/A"
            
            company_elem = card.find('p', class_='company-name')
            company = company_elem.text.strip() if company_elem else "N/A"
            
            location_elem = card.find('p', class_='location-link')
            location = location_elem.text.strip() if location_elem else "Remote"
            
            # Get job link
            link_elem = card.find('a', class_='view_detail_button')
            job_link = f"{self.base_url}{link_elem['href']}" if link_elem and 'href' in link_elem.attrs else ""
            
            # Extract job ID from link
            job_id = link_elem['href'].split('/')[-1] if link_elem and 'href' in link_elem.attrs else f"internshala_{hash(title + company)}"
            
            # Get description
            desc_elem = card.find('div', class_='internship_other_details_container')
            description = desc_elem.text.strip() if desc_elem else ""
            
            # Extract skills from description
            skills = self.extract_skills(description + " " + title)
            
            # Extract experience
            experience = self.extract_experience(description)
            
            # Determine job type
            job_type = "internship" if "intern" in title.lower() else "full_time"
            
            return {
                'job_id': f"internshala_{job_id}",
                'title': title,
                'company': company,
                'location': location,
                'description': description,
                'requirements': description,
                'skills': skills,
                'experience_min': experience,
                'experience_max': experience + 2 if experience else None,
                'job_type': job_type,
                'salary_text': None,
                'apply_link': job_link,
                'posted_date': datetime.now(),
            }
        except Exception as e:
            logger.error(f"Error parsing Internshala job card: {str(e)}")
            return None
