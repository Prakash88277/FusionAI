from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class JobType(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"
    FREELANCE = "freelance"
    REMOTE = "remote"

class ExperienceLevel(str, Enum):
    ENTRY = "entry"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    EXECUTIVE = "executive"

class Job(BaseModel):
    id: Optional[str] = None
    title: str
    company: str
    company_logo: Optional[str] = None
    location: str
    country: Optional[str] = None
    description: str
    requirements: Optional[str] = None
    responsibilities: Optional[str] = None
    benefits: Optional[str] = None
    skills: List[str]
    skills_required: List[str]
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    salary_currency: Optional[str] = "USD"
    salary_text: Optional[str] = None
    job_type: Optional[JobType] = None
    experience_level: Optional[ExperienceLevel] = None
    remote_allowed: Optional[bool] = None
    apply_link: str
    company_website: Optional[str] = None
    posted_date: Optional[datetime] = None
    scraped_date: Optional[datetime] = None
    source: str  # LinkedIn, Google Careers, etc.
    source_url: Optional[str] = None
    job_id: Optional[str] = None  # Internal job ID from the source
    is_active: Optional[bool] = True
    metadata: Optional[Dict[str, Any]] = None

class JobSearchFilters(BaseModel):
    keywords: Optional[List[str]] = None
    location: Optional[str] = None
    country: Optional[str] = None
    company: Optional[str] = None
    job_type: Optional[JobType] = None
    experience_level: Optional[ExperienceLevel] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    remote_only: Optional[bool] = None
    posted_within_days: Optional[int] = None

class JobMatch(BaseModel):
    job: Job
    match_score: float  # 0-100% match score
    matching_skills: List[str]
    missing_skills: Optional[List[str]] = None
    skill_match_percentage: Optional[float] = None
    experience_match: Optional[bool] = None
    location_match: Optional[bool] = None
    salary_match: Optional[bool] = None