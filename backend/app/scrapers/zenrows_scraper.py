import json
import os
from typing import List
from bs4 import BeautifulSoup
from .zenrows_client import ZenRowsClient
import logging

logger = logging.getLogger(__name__)

client = ZenRowsClient()

JOB_SEARCH_TEMPLATES = [
    "https://www.indeed.com/jobs?q={query}&l=India",
    "https://in.linkedin.com/jobs/search?keywords={query}",
    "https://www.glassdoor.co.in/Job/jobs.htm?sc.keyword={query}"
]

def build_search_urls(keywords: List[str], max_terms: int = 5) -> List[str]:
    """Build job search URLs from keywords"""
    max_terms = int(os.getenv('ZXR_MAX_TERMS', max_terms))
    
    # Clean and join keywords
    clean_keywords = []
    for k in keywords[:max_terms]:
        if k and isinstance(k, str):
            clean_keywords.append(k.replace(' ', '+'))
    
    if not clean_keywords:
        clean_keywords = ['software', 'developer']  # fallback
        
    q = "+".join(clean_keywords)
    urls = [tpl.format(query=q) for tpl in JOB_SEARCH_TEMPLATES]
    
    logger.info(f"Built {len(urls)} search URLs for keywords: {clean_keywords}")
    return urls

def parse_job_cards_from_html(html: str, source_domain: str = '') -> List[dict]:
    """Parse job cards from HTML using BeautifulSoup"""
    soup = BeautifulSoup(html, 'html.parser')
    jobs = []
    
    # Generic selectors that work across multiple job sites
    containers = soup.select('[data-jk], .job-card, .result, .jobsearch-SerpJobCard, .jl, .react-job-listing')
    if not containers:
        containers = soup.select('.job')
    
    logger.info(f"Found {len(containers)} job containers in HTML from {source_domain}")

    for c in containers:
        # Extract job title
        title_el = c.select_one('h2, h3, .jobTitle, .title, a')
        title = title_el.get_text(strip=True) if title_el else None
        
        # Extract company name
        company_el = c.select_one('.company, .companyName, .job-company')
        company = company_el.get_text(strip=True) if company_el else None
        
        # Extract location
        loc_el = c.select_one('.location, .companyLocation, .job-location')
        location = loc_el.get_text(strip=True) if loc_el else None
        
        # Extract apply link
        a = c.select_one('a[href]')
        link = None
        if a:
            link = a.get('href')
            if link and link.startswith('/'):
                # Convert relative URLs to absolute
                if 'indeed' in source_domain:
                    link = 'https://www.indeed.com' + link
                elif 'glassdoor' in source_domain:
                    link = 'https://www.glassdoor.co.in' + link
                elif 'linkedin' in source_domain:
                    link = 'https://www.linkedin.com' + link
        
        # Extract job description
        desc = c.get_text(separator=' ', strip=True)
        
        # Only add jobs with at least a title
        if title and title.lower() not in ['n/a', 'null', '']:
            jobs.append({
                'title': title,
                'company': company,
                'location': location,
                'description': desc[:500] if desc else None,  # Limit description length
                'apply_link': link
            })
    
    logger.info(f"Parsed {len(jobs)} valid jobs from {source_domain}")
    return jobs

def scrape_jobs_for_keywords(keywords: List[str], max_per_source: int = 10) -> List[dict]:
    """Scrape jobs for given keywords using ZenRows"""
    max_per_source = int(os.getenv('ZXR_MAX_SCRAPE_PER_SOURCE', max_per_source))
    
    urls = build_search_urls(keywords)
    collected = []
    
    for url in urls:
        try:
            logger.info(f"Scraping jobs from: {url}")
            
            # Use ZenRows to fetch the page
            resp = client.fetch(url, js_render=True)
            
            # Handle different response formats
            if isinstance(resp, dict):
                html = resp.get('html') or json.dumps(resp)
            else:
                html = resp
            
            # Extract domain for link processing
            domain = url.split('/')[2] if '://' in url else ''
            
            # Parse jobs from HTML
            jobs = parse_job_cards_from_html(html, source_domain=domain)
            
            if jobs:
                collected.extend(jobs[:max_per_source])
                logger.info(f"Collected {len(jobs[:max_per_source])} jobs from {domain}")
            else:
                logger.warning(f"No jobs found on {domain}")
                
        except Exception as e:
            logger.error(f"ZenRows error for {url}: {str(e)}")
            continue

    logger.info(f"Total jobs collected: {len(collected)}")
    
    # Deduplicate jobs based on title + company + location
    seen = set()
    final = []
    
    for j in collected:
        # Create a unique key for deduplication
        key = (
            (j.get('title') or '').lower().strip(),
            (j.get('company') or '').lower().strip(),
            (j.get('location') or '').lower().strip()
        )
        
        if key in seen or not j.get('title'):
            continue
            
        seen.add(key)
        final.append(j)
    
    logger.info(f"After deduplication: {len(final)} unique jobs")
    return final
